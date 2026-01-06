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

    class_list = fields.One2many(
        "class.information", 
        "school_id", 
        string="Danh sách lớp học"
    )

    def action_view_classes(self):
        """Action to view all classes for this school"""
        self.ensure_one()
        return {
            'name': 'Danh sách lớp học',
            'type': 'ir.actions.act_window',
            'res_model': 'class.information',
            'view_mode': 'tree,form',
            'domain': [('school_id', '=', self.id)],
            'context': {'default_school_id': self.id},
        }

