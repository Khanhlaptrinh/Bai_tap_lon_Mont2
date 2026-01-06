# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StudentInformation(models.Model):
    _name = 'student.information'
    _description = 'Student Information'

    name = fields.Char(string="Họ và Tên", required=True)
    birthday = fields.Date(string="Ngày sinh", required=True)
    class_id = fields.Many2one(comodel_name='class.information', required=True)


