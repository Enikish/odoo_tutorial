from typing import Union

import pandas as pd
import os

from tqdm import tqdm
from multiprocessing import Pool, cpu_count
import logging

from .config import *

_logger = logging.getLogger(__name__)


def find_excel_files(dir_path: str):
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(dir_path)
        for file in files if file.endswith(EXCEL_EXTENSIONS)
    ]


def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    替换DataFrame的列名
    """
    df.columns = df.columns.astype(str).str.strip()
    df.rename(columns=COLUMN_MAPPING, inplace=True)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    清洗DataFrame的数据
    """
    df['name'] = df['name'].astype(str).str.strip().str.replace(r'[\s\xa0]+', '', regex=True)
    df['identity_id'] = df['identity_id'].astype(str).str.strip().str.upper().str.replace(r'[^0-9X]', '', regex=True)
    if 'mobile' in df.columns:
        df['mobile'] = df['mobile'].astype(str).str.strip().str.replace(r'[^0-9]', '', regex=True)
    return df


def extract_valid_rows(df: pd.DataFrame):
    """
    仅当姓名和身份证号码同时存在的信息验证为可用
    """
    expected_cols = list(REQUIRED_COLS | OPTIONAL_COLS)
    existing_cols = [col for col in expected_cols if col in df.columns]

    df = df[existing_cols].where(pd.notnull(df), None)

    return df[df['name'].notna() & df['identity_id'].notna() & (df['name'] != '') & (df['identity_id'] != '')]


def handle_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    solve repeated rows, deduplicate rows and return
    """
    group_size = len(set(df.columns))
    columns_per_group = list(df.columns[:group_size])

    num_groups = df.shape[1] // group_size

    groups_dfs = [
        df.iloc[:, i * group_size: (i + 1) * group_size].copy().set_axis(columns_per_group, axis=1)
        for i in range(num_groups)
    ]

    return pd.concat(groups_dfs, ignore_index=True)


def check_columns(df: pd.DataFrame) -> tuple[bool, bool]:
    """
    check if required columns are in DataFrame's columns
    """
    has_all = REQUIRED_COLS.issubset(df.columns)
    has_partial = any(column in df.columns for column in REQUIRED_COLS)
    return has_all, has_partial


def get_sheet_records(df: pd.DataFrame) -> Union[list, str]:
    """
    get records from sheet
    """
    df = clean_columns(df)

    has_all, has_partial = check_columns(df)
    if not has_partial:
        df.columns = df.iloc[0].astype(str).str.strip()
        df = df[1:].reset_index(drop=True)
        df = clean_columns(df)
        has_all, _ = check_columns(df)

    if df.columns.duplicated().any():
        df = handle_duplicate_rows(df)

    if df.empty:
        return []

    if has_all:
        df = clean_data(df)
        return extract_valid_rows(df).to_dict('records')
    return []


def get_sheets(file_path, row_skip=0):
    """
    read Excel files and return all the sheets
    """
    try:
        sheets = pd.read_excel(file_path, sheet_name=None, dtype=str, skiprows=row_skip)
        return sheets
    except Exception as e:
        _logger.error(e)


def process_excel_file(file_path: str):
    """
    read Excel files and return all the sheets
    """
    sheets = get_sheets(file_path)

    all_records = []
    fail_sheets = []
    for sheet_name, df in sheets.items():
        if df.empty:
            continue

        records = get_sheet_records(df)

        if records:
            all_records.extend(records)
        else:
            _, has_partial = check_columns(df)
            error_type = "列名不正确或不完整" if has_partial else "表头缺失"
            fail_sheets.append(f"{file_path}->{sheet_name} : {error_type}")

    return all_records, fail_sheets


def parallel_process(file_list):
    """
    parallel process
    """
    all_records = []
    all_failures = []
    for file in tqdm(file_list, desc='Processing'):
        records, failures = process_excel_file(file)
        all_records.extend(records)
        all_failures.extend(failures)

    return all_records, all_failures


def call_point(dir_path=r'D:\Desktop\港中旅'):
    """
    call functions
    """
    file_paths = find_excel_files(dir_path)
    all_records, all_failures = parallel_process(file_paths)
    return all_records, all_failures


def main():
    records, failures = call_point()
    print(records)
    print(failures)


if __name__ == '__main__':
    main()
