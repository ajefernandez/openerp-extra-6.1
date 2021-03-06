# -*- encoding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     
#
##############################################################################
from mx.DateTime import now

import wizard
import netsvc
import ir
import pooler

from tools.translate import _

case_form = """<?xml version="1.0"?>
<form string="Planify Meeting">
    <field name="date"/>
    <field name="duration" widget="float_time"/>
    <field name="section_id"/>
    <field name="categ_id" domain="[('section_id','=',section_id)]"/>
</form>"""

case_fields = {
    'date': {'string': 'Meeting date', 'type': 'datetime', 'required': 1},
    'duration': {'string': 'Duration (Hours)', 'type': 'float', 'required': 1},
    'section_id': {'string': 'Section', 'type': 'many2one', 'relation': 'crm.case.section', 'required': True},
    'categ_id': {'string': 'Category', 'type': 'many2one', 'relation': 'crm.case.categ', 'required': True}
}


class make_meeting(wizard.interface):
    def _selectPartner(self, cr, uid, data, context):
        case_obj = pooler.get_pool(cr.dbname).get('crm.case')
        case = case_obj.browse(cr, uid, data['id'])
        return {'date': case.date, 'duration': case.duration or 2.0}

    def _makeMeeting(self, cr, uid, data, context):
        pool = pooler.get_pool(cr.dbname)

        case_obj = pool.get('crm.case')
        new_id = case_obj.copy(cr, uid, data['id'], {
            'date': data['form']['date'],
            'duration': data['form']['duration'],
            'section_id': data['form']['section_id'],
            'categ_id': data['form']['categ_id'],
        }, context=context)

        # Link new case with current case
        current = case_obj.write(cr, uid, data['id'], {'case_id': new_id}, context=context)
        return {}

    states = {
        'init': {
            'actions': [_selectPartner],
            'result': {'type': 'form', 'arch': case_form, 'fields': case_fields,
                'state' : [('end', 'Cancel','gtk-cancel'),('order', 'Set Meeting','gtk-go-forward')]}
        },
        'order': {
            'actions': [],
            'result': {'type': 'action', 'action': _makeMeeting, 'state': 'end'}
        }
    }

make_meeting('market.meeting')

