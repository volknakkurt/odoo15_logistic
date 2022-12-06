# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EmployeeInheritence(models.Model):
    _inherit = 'hr.employee'

    postcode_id = fields.Integer(string="Post Code", default=1)

    def action_test(self):
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click Successfull',
                'type': 'rainbow_man'
            }
        }

