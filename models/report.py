from email.policy import default

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Report(models.Model):
    _inherit = 'hr.expense.sheet'

    state = fields.Selection([
        ('draft','Draft'),
        ('submit','Awaiting Line manager Approval'),
        ('hr','Awaiting HR Approval'),
        ('review','Awaiting Finance Review'),
        ('approve','Awaiting Finance Approve'),
        ('post','Awaiting Payment Approve'),
        ('done','Done'),
        ('cancel','Reject'),
    ], tracking=True)

    payment_mode = fields.Selection(readonly=False)

    recall_ids = fields.Many2many('hr.expense.recall.wizard')
    reason_recall = fields.Char()
    product_id = fields.Many2one('product.product')
    can_click = fields.Boolean(compute='_compute_can_click', store=False)


    def _compute_can_click(self):
        for rec in self:
            rec.can_click = self.env.user.has_group('expenses.expenses_model_group')


    user_in_paid_group = fields.Boolean(compute='_compute_user_in_paid_group')
    def _compute_user_in_paid_group(self):
        user = self.env.user
        in_group = user.has_group('expenses.paid_by_group')
        for rec in self:
            rec.user_in_paid_group = in_group

    #char here for every state, draft->D, line manager -> L ...
    flag_buttons = fields.Char(compute='_compute_buttons_visibility',invisible=True, store=False)
    @api.depends('state')
    def _compute_buttons_visibility(self):
        for rec in self:
            if rec.state=='submit' and self.env.user.has_group('expenses.line_manger_approval_group'):
                rec.flag_buttons = 'line_manager'
            elif rec.state=='hr' and self.env.user.has_group('expenses.hr_approval_group'):
                rec.flag_buttons = 'hr'
            elif rec.state == 'review' and self.env.user.has_group('expenses.finance_review_group'):
                rec.flag_buttons = 'review'
            elif rec.state=='approve' and self.env.user.has_group('expenses.finance_approval_group'):
                rec.flag_buttons = 'finance_approve'
            elif rec.state=='post' and self.env.user.has_group('expenses.payment_approval_group'):
                rec.flag_buttons = 'payment'
            else:
                rec.flag_buttons = '*'


    def action_submit_sheet_validation(self):
        for rec in self:
            if rec.employee_id != self.env.user.employee_id:
                raise ValidationError('You are not the creation employee')
            if self.env.user.has_group('expenses.c_level_group'):
                rec.write({
                    'state':'review'
                })
            else:
                return super().action_submit_sheet()

    def action_open_recall_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('expenses.recall_wizard_action')
        action['context'] = {'default_sheet_id':self.id}
        return action

    def action_approve_expense_sheets(self):
        for rec in self:
            if rec.user_id != self.env.user:
                raise ValidationError('You are not the line manager')
            hr_approval_check = all(line.product_id.hr_approval for line in rec.expense_line_ids)
            if hr_approval_check or self.env.user.has_group('expenses.cfo_cycle_approval_group'):
                rec.write({
                    'state': 'review'
                })
                self.message_post(
                    body="Notification has been sent to Finance Reviewers",
                    subject="Review",
                    message_type='notification',
                    subtype_xmlid='mail.mt_activities',
                    partner_ids=self.env.ref('expenses.finance_review_group').users.mapped('partner_id.id')
                )
            else:
                rec.write({
                    'state':'hr'
                })
                self.message_post(
                    body="Notification has been sent to HRs",
                    subject="HR Approval",
                    message_type='notification',
                    subtype_xmlid='mail.mt_activities',
                    partner_ids=self.env.ref('expenses.hr_approval_group').users.mapped('partner_id.id')
                )

    def action_hr_approve_expense_sheets(self):
        for rec in self:
            rec.write({
                'state':'review'
            })
        self.message_post(
            body="Notification has been sent to Finance Reviewers",
            subject="Review",
            message_type='notification',
            subtype_xmlid='mail.mt_activities',
            partner_ids=self.env.ref('expenses.finance_review_group').users.mapped('partner_id.id')
        )
    def action_finance_review_expense_sheets(self):
        for rec in self:
            rec.write({
                'state':'approve'
            })
        self.message_post(
            body="Notification has been sent to Finance Approval",
            subject="Finance Approval",
            message_type='notification',
            subtype_xmlid='mail.mt_activities',
            partner_ids=self.env.ref('expenses.finance_approval_group').users.mapped('partner_id.id')
        )
    @api.constrains('expense_line_ids')
    def _check_type_approval(self):
        for rec in self:
            type_list = []
            if rec.expense_line_ids:
                for line in rec.expense_line_ids:
                    type_list.append(line.product_id.type_approval)
                if len(set(type_list)) != 1:
                    raise ValidationError('The Categories must have the same type of approval')

    @api.constrains('expense_line_ids')
    def _check_expense_limit(self):
        for rec in self:
            for product in self.env['product.product'].search([]):
                product_total_amount = 0
                if product.expense_limit:
                    for line in rec.expense_line_ids.filtered(lambda l: l.date.year == fields.Date.today().year):
                        if line.product_id.id == product.id:
                            product_total_amount += line.total_amount
                    if product_total_amount > product.amount:
                        raise ValidationError(
                            f'You have exceeded the Expense Limit of {product.name} '
                            f'(${product.amount}).'
                        )



