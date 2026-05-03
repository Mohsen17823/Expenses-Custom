from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ExpensesCategories(models.Model):
    _inherit = 'product.product'

    hr_approval = fields.Boolean(string='HR Approval')
    expense_limit = fields.Boolean(string='Expense Limit')
    amount = fields.Monetary(compute='_compute_expense_limit',
                             readonly=False,
                             store=True,
                             currency_field='currency_id')
    type_approval = fields.Selection([
        ('finance','Finance'),
        ('hr','HR')
    ])

    @api.depends('expense_limit')
    def _compute_expense_limit(self):
        for rec in self:
            if not rec.expense_limit:
                rec.write({
                    'amount':0
                })

    @api.constrains('amount')
    def _check_no_amount_no_expense_limit(self):
        for rec in self:
            rec.expense_limit = bool(rec.amount != 0)