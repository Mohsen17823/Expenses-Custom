

from odoo import fields, models

class RecallWizard(models.TransientModel):
    _name = 'hr.expense.recall.wizard'

    sheet_id = fields.Many2one('hr.expense.sheet')
    reason_recall = fields.Char(string='Reason')

    def action_recall(self):
        self.sheet_id.reason_recall = self.reason_recall
        self.sheet_id.write({
            'state':'draft'
        })