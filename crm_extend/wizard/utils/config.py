EXCEL_EXTENSIONS = ('.xlsx', '.xls')
REQUIRED_COLS = {'name', 'identity_id'}
OPTIONAL_COLS = {'mobile'}
COLUMN_MAPPING = {
    '身份证': 'identity_id',
    '身份证号': 'identity_id',
    '联系电话': 'mobile',
    '联系方式': 'mobile',
    '电话号码': 'mobile',
    '电话': 'mobile',
    '姓名': 'name',
    '客户': 'name'
}
