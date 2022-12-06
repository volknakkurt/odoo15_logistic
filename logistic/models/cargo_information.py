from odoo import api, fields, models


class CargoInformation(models.Model):
    _name = "cargo.information"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Cargo Information"
    _rec_name = 'tracking_number'

    tracking_number = fields.Char(string='Tracking Number', required=True)
    cargo_waybill_number = fields.Integer(string='Cargo Waybill Number', required=True)
    sender_name = fields.Many2one('res.partner', string='Sender Name')
    recipient_name = fields.Many2one('res.partner', string='Recipient Name')
    product_line_ids = fields.One2many('cargo.product.lines', 'management_id', string='Product Lines', required=True)
    date_of_sending = fields.Date(string='Date Of Sending', default=fields.Date.context_today)
    datetime_of_sending = fields.Datetime(string='Datetime Of Sending', default=fields.Datetime.now)
    payment_type = fields.Selection(
        [('sender_pay', 'Sender pay'), ('recipient_pay', 'Recipient Name'), ('third_party_pay', 'Third Party Pay')],
        string='Payment Type')
    third_party = fields.Many2one('res.partner', string='Third Party')
    explanation = fields.Html(string='Explanation')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('invoiced', 'Invoiced'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('on_the_way', ' On The Way'),
        ('delivered', 'Delivered'),
        ('cancel', 'Canceled')], default='draft', string="Status", required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.onchange('payment_type')
    def onchange_payment_type(self):
        if self.payment_type == 'recipient_pay':
            self.third_party = self.recipient_name
        elif self.payment_type == 'sender_pay':
            self.third_party = self.sender_name
        else:
            self.third_party = fields.Many2one('customer', string='Third Party')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_to_approve(self):
        for rec in self:
            rec.state = 'to_approve'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_on_the_way(self):
        for rec in self:
            rec.state = 'on_the_way'

    def action_delivered(self):
        for rec in self:
            rec.state = 'delivered'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Cargo Creation Successfull',
                'type': 'rainbow_man'
            }
        }

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_cargo_archive(self):
        for rec in self:
            rec.active = False
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Archive Successfull',
                'type': 'rainbow_man'
            }
        }

    def action_invoiced(self):
        for rec in self:
            rec.state = 'invoiced'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_mode': 'form',
            'res_id': self.payment_id.id,
            'views': [(False, 'form')],
        }


class CargoProduct(models.Model):
    _name = "cargo.product.lines"
    _description = "Cargo Product Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related="product_id.list_price")
    qty = fields.Float(string='Quantity', default=0)
    tax = fields.Selection([
            ('kdv_18', 'KDV%18'),
            ('kdv_8', 'KDV%8'),
            ('kdv_1', 'KDV%1')], string="Tax")
    untaxed_price = fields.Float(string='Untaxed Price', compute='_compute_untaxed_price')
    management_id = fields.Many2one('cargo.information', string='Cargo Management')
    total_price = fields.Float(string='Total Price', compute='_compute_total_price')

    @api.depends('qty')
    def _compute_untaxed_price(self):
        for rec in self:
            if rec.qty:
                rec.untaxed_price = rec.price_unit * rec.qty
            else:
                rec.untaxed_price = 0

    @api.depends('tax', 'total_price', 'untaxed_price')
    def _compute_total_price(self):
        for rec in self:
            if rec.tax == 'kdv_18':
                rec.total_price = (rec.untaxed_price * 18 / 100) + rec.untaxed_price
            elif rec.tax == 'kdv_8':
                rec.total_price = (rec.untaxed_price * 8 / 100) + rec.untaxed_price
            elif rec.tax == 'kdv_1':
                rec.total_price = (rec.untaxed_price * 1 / 100) + rec.untaxed_price
            else:
                rec.total_price = rec.untaxed_price


# def action_invoiced(self):
#     for activity_type in self.plan_id.plan_activity_type_ids:
#         responsible = activity_type.get_responsible_id(self.employee_id)
#
#         if self.env['hr.employee'].with_user(responsible).check_access_rights('read', raise_exception=False):
#             date_deadline = self.env['mail.activity']._calculate_date_deadline(activity_type.activity_type_id)
#             self.employee_id.activity_schedule(
#                 activity_type_id=activity_type.activity_type_id.id,
#                 summary=activity_type.summary,
#                 note=activity_type.note,
#                 user_id=responsible.id,
#                 date_deadline=date_deadline
#             )
#
#     return {
#         'type': 'ir.actions.act_window',
#         'res_model': 'hr.employee',
#         'res_id': self.employee_id.id,
#         'name': self.employee_id.display_name,
#         'view_mode': 'form',
#         'views': [(False, "form")],
#     }
#