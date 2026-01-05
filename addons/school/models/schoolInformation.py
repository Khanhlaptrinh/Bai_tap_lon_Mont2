# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SchoolInformation(models.Model):
    _name = 'school.information'
    _description = 'School Management'

    name = fields.Char(string='Tên trường')
    type = fields.Selection([('private', 'Dân lập'), ('public', 'Công lập')], default='public', string='Loại trường')
    email = fields.Text(string='Email')
    address = fields.Text(string='Dia chi')

    phone = fields.Char(string="Số điện thoại")
    hasOnlineClass = fields.Boolean(string="Có lớp online không?")
    rank = fields.Integer(string="Xếp hạng")
    establishDay = fields.Date(string="Ngày thành lập")
    document = fields.Binary(string="Tài liệu trường")
    document_name = fields.Char(string="Tên tài liệu")

