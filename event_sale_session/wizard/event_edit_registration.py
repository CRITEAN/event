# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RegistrationEditor(models.TransientModel):
    _inherit = "registration.editor"

    @api.model
    def default_get(self, fields):
        res = super(RegistrationEditor, self).default_get(fields)
        vals = [(6, 0, [])]
        so_line = self.env['sale.order.line']
        for registration in res['event_registration_ids'][1:]:
            if so_line.id != registration[2]['sale_order_line_id']:
                so_line = self.env['sale.order.line'].browse(
                    registration[2]['sale_order_line_id']
                )
            vals.append((0, 0, dict(registration[2],
                                    session_id=so_line.session_id.id)),)
        return res


class RegistrationEditorLine(models.TransientModel):
    """Event Registration"""
    _inherit = "registration.editor.line"

    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
    )

    @api.multi
    def get_registration_data(self):
        res = super(RegistrationEditorLine, self).get_registration_data()
        res.update({
            'session_id': self.sale_order_line_id.session_id.id,
        })
        return res
