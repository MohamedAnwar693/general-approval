from odoo import models, fields, api

class Approval(models.Model):
    _name = 'approval.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Approval Request'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    request_date = fields.Date(string='Request Date', default=fields.Date.today())
    requester_id = fields.Many2one('res.users', string='Requester', default=lambda self: self.env.user.id)
    approval_line_ids = fields.One2many('approval.line', 'approval_id', string='Approval Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', track_visibility='onchange')

    def action_draft(self):
        self.write({'state': 'Draft'})

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

class ApprovalLine(models.Model):
    _name = 'approval.line'
    _description = 'Approval Line'

    approval_id = fields.Many2one('approval.request', string='Approval Request')
    approver_id = fields.Many2one('res.users', string='Approver', required=True)
    approved_date = fields.Date(string='Approved Date')
    approval_decision = fields.Selection([
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ], string='Decision', track_visibility='onchange')

    @api.model
    def create(self, values):
        approval_line = super(ApprovalLine, self).create(values)
        if approval_line.approval_decision == 'approve':
            approval_line.approval_id.action_approve()
        elif approval_line.approval_decision == 'reject':
            approval_line.approval_id.action_reject()
        return approval_line
