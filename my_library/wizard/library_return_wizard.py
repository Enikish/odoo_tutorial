from odoo import models, api, fields, _


class LibraryReturnWizard(models.TransientModel):
    _name = 'library.return.wizard'

    borrower_id = fields.Many2one(comodel_name='res.partner', 
                                  string='Borrower',
                                  )

    book_ids = fields.Many2many(comodel_name='library.book',
                                string='Books')


    def books_returns(self):
        loanModel = self.env['library.book.rent']
        for rec in self:
            loans = loanModel.search([('state', '=', 'ongoing'),
                                      ('book_id', 'in', rec.book_ids.ids),
                                      ('borrower_id', '=', rec.borrower_id.id)])
            for loan in loans:
                loan.book_return()

    @api.onchange('borrower_id')
    def onchange_member(self):
        rentModel = self.env['library.book.rent']
        books_on_rent = rentModel.search([('state', '=', 'ongoing'),
                                          ('borrower_id', '=', self.borrower_id.id)]
                                          )
        self.book_ids = books_on_rent.mapped('book_id')
        result = {
            'domain':{
                'book_ids':[
                ('id', 'in', self.book_ids.ids)]
            }
        }
        late_domain = [
            ('id', 'in', books_on_rent.ids),
            ('expected_return_date', '<', fields.Date.today())
        ]
        if late_books := rentModel.search(late_domain):
            message = ('Warn the member that the following books are late:\n')
            titles = late_books.mapped('book_id.name')
            result['warning'] = {
                'title': 'Late Books',
                'message': message + '\n'.join(titles)
            }
        return result


    