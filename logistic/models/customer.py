from odoo import api, fields, models


class Customers(models.Model):
    _name = "customer"
    _description = "Customers"
    _rec_name = 'name'

    name = fields.Char(string='Name')
    surname = fields.Char(string='Surname')
    title = fields.Char(string='Title')
    phone = fields.Char(string='Phone Number')
    company_name = fields.Char(string='Company Name')
