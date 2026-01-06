# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClassInformation(models.Model):
    _name = 'class.information'
    _description = 'Class Management'

    name = fields.Char(string="Ten lop", required=True)
    grade = fields.Char(string="Khoi")
    mainTeacher = fields.Char(string="GVCN")
    #     Relation
    school_id = fields.Many2one(
        "school.information",
        string="Truong",
        ondelete="set null",
        required=False,
        check_company=False
    )

    def __getitem__(self, name):
        """Override to handle _unknown objects when accessing fields"""
        value = super(ClassInformation, self).__getitem__(name)
        if name == 'school_id' and value:
            try:
                # Check if value is _unknown object
                if hasattr(value, '_name') and getattr(value, '_name', None) == '_unknown':
                    # Return empty recordset instead
                    return self.env['school.information']
            except (AttributeError, Exception):
                pass
        return value

    def onchange(self, values, field_name, field_onchange):
        """Override onchange to handle _unknown objects"""
        # First, clean up any _unknown objects in the record itself
        try:
            if hasattr(self, 'school_id') and self.school_id:
                try:
                    if hasattr(self.school_id, '_name') and getattr(self.school_id, '_name', None) == '_unknown':
                        # Set to empty recordset
                        self.school_id = self.env['school.information']
                except Exception:
                    pass
        except Exception:
            pass
        
        # Check if school_id is in values and might be _unknown
        try:
            if 'school_id' in values and values.get('school_id'):
                school_id_value = values['school_id']
                # If it's a tuple/list, check the ID
                if isinstance(school_id_value, (list, tuple)) and len(school_id_value) >= 1:
                    school_id = school_id_value[0]
                    if school_id:
                        try:
                            school = self.env['school.information'].browse(school_id)
                            if not school.exists() or getattr(school, '_name', None) == '_unknown':
                                values['school_id'] = False
                        except Exception:
                            values['school_id'] = False
        except Exception:
            pass
        
        # Call parent onchange with error handling
        try:
            return super(ClassInformation, self).onchange(values, field_name, field_onchange)
        except AttributeError as e:
            if '_unknown' in str(e) or 'has no attribute \'id\'' in str(e):
                # If _unknown error, clean up school_id and retry
                try:
                    # Clean up in values
                    if 'school_id' in values:
                        values['school_id'] = False
                    # Clean up in record - try multiple ways
                    try:
                        if hasattr(self, 'school_id'):
                            self.school_id = self.env['school.information']
                    except Exception:
                        pass
                    # Also try to clean up via __setitem__
                    try:
                        self.__setitem__('school_id', self.env['school.information'])
                    except Exception:
                        pass
                except Exception:
                    pass
                # Retry with cleaned values
                try:
                    return super(ClassInformation, self).onchange(values, field_name, field_onchange)
                except Exception:
                    # If still fails, return empty result to prevent crash
                    return {'value': {}}
            raise
        except Exception as e:
            # If any other error related to _unknown, return empty result
            if '_unknown' in str(e) or 'has no attribute \'id\'' in str(e):
                return {'value': {}}
            raise

    def _read_format(self, fnames=None, load='_classic_read'):
        """Override _read_format to handle _unknown objects in school_id field"""
        try:
            result = super(ClassInformation, self)._read_format(fnames, load)
            for record in result:
                if 'school_id' in record:
                    try:
                        school_id_value = record.get('school_id')
                        if school_id_value:
                            # Check if it's a tuple/list format (id, name)
                            if isinstance(school_id_value, (list, tuple)) and len(school_id_value) >= 1:
                                school_id = school_id_value[0]
                                if school_id:
                                    # Try to browse and check if it's _unknown
                                    try:
                                        school = self.env['school.information'].browse(school_id)
                                        if not school.exists() or getattr(school, '_name', None) == '_unknown':
                                            record['school_id'] = False
                                    except Exception:
                                        # Only set to False if it's really _unknown, not if model doesn't exist yet
                                        pass
                    except (KeyError, ValueError, AttributeError, Exception):
                        # Don't modify if there's an error - let it pass through
                        pass
            return result
        except Exception:
            # If there's any error in _read_format, return original result
            return super(ClassInformation, self)._read_format(fnames, load)

    def read(self, fields=None, load='_classic_read'):
        """Override read to handle _unknown objects in school_id field"""
        try:
            result = super(ClassInformation, self).read(fields, load)
            for record in result:
                if 'school_id' in record and record.get('school_id'):
                    # Check if school_id points to _unknown object
                    try:
                        school_id_value = record['school_id']
                        if isinstance(school_id_value, (list, tuple)) and len(school_id_value) >= 1:
                            school_id = school_id_value[0]
                            if school_id:
                                # Try to browse the school to check if it exists
                                try:
                                    school = self.env['school.information'].browse(school_id)
                                    if not school.exists() or getattr(school, '_name', None) == '_unknown':
                                        record['school_id'] = False
                                except Exception:
                                    # Don't modify if there's an error
                                    pass
                    except (KeyError, ValueError, AttributeError, Exception):
                        # Don't modify if there's an error
                        pass
            return result
        except AttributeError as e:
            if '_unknown' in str(e) or 'has no attribute \'id\'' in str(e):
                # If we get _unknown error, try to read without school_id first
                if fields and 'school_id' in fields:
                    fields_without_school = [f for f in fields if f != 'school_id']
                    result = super(ClassInformation, self).read(fields_without_school, load)
                    # Add school_id as False for all records
                    for record in result:
                        record['school_id'] = False
                    return result
            raise
        except Exception:
            # If any other error, try to read normally
            return super(ClassInformation, self).read(fields, load)

    @api.model
    def _cleanup_orphaned_school_ids(self):
        """Clean up records with invalid school_id references"""
        records = self.search([('school_id', '!=', False)])
        orphaned = records.filtered(lambda r: not r.school_id.exists() or r.school_id._name == '_unknown')
        if orphaned:
            orphaned.write({'school_id': False})
            return len(orphaned)
        return 0

