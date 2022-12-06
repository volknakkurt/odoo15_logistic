from odoo import api, fields, models


class CargoManagement(models.Model):
    _name = "cargo.management.wizard"
    _description = "Cargo Management"
    _rec_name = 'tracking_number'

    cargo_id = fields.Many2one('cargo.information', string='Tracking Number', required=True)
    cargo_waybill_number = fields.Char(string='Cargo Waybill Number')
    tracking_number = fields.Char(related='cargo_id.tracking_number', string='Tracking Number',)
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle Informations', required=True)

    @api.onchange('cargo_id')
    def onchange_patient_id(self):
        self.tracking_number = self.cargo_id.tracking_number
        self.cargo_id.state = 'to_approve'
