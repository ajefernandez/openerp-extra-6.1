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

from osv import fields, osv

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'
    
    def _complete_name_get_fnc(self, cr, uid, ids, prop, unknow_none, unknow_dict):
        table = self.name_get(cr, uid, ids, {'contact_display':'contact'})
        return dict(table)
    
    _columns = {
        'complete_address': fields.function(_complete_name_get_fnc, method=True, type="char", size=512, string='Complete Name'),
    }
    
res_partner_address()