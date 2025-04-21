# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def post_init_hook(cr, registry):
    """
    Post-init hook to ensure the civil_id field is properly created in the database
    regardless of environment differences.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Force update of res.partner model to ensure civil_id field is created
    if 'res.partner' in env:
        # Check if field exists and create it if not
        partner_model = env['ir.model'].search([('model', '=', 'res.partner')], limit=1)
        if partner_model:
            field_exists = env['ir.model.fields'].search([
                ('model_id', '=', partner_model.id),
                ('name', '=', 'civil_id')
            ], limit=1)
            
            if not field_exists:
                # Create field if it doesn't exist
                env['ir.model.fields'].create({
                    'model_id': partner_model.id,
                    'name': 'civil_id',
                    'field_description': 'Civil ID',
                    'ttype': 'char',
                    'state': 'manual',
                    'required': False,
                    'store': True,
                    'index': True,
                })
                
    # Ensure the field is visible in the UI
    env.cr.execute("""
        UPDATE ir_model_fields 
        SET state='manual' 
        WHERE name='civil_id' AND model='res.partner'
    """)
    
    # Clear caches to ensure changes are visible
    env.registry.clear_caches()
