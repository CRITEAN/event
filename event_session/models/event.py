# -*- coding: utf-8 -*-
# Copyright 2017 David Vidal<david.vidal@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = 'event.event'

    session_ids = fields.One2many(
        comodel_name='event.session',
        inverse_name='event_id',
        string='Sessions',
    )
    sessions_count = fields.Integer(
        compute='_compute_sessions_count',
        string='Total event sessions',
    )

    @api.multi
    def _compute_sessions_count(self):
        for event in self:
            event.sessions_count = len(event.session_ids)
    
    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        if not event.session_ids:
            event.session_ids = [(0, 0, {
                'seats_min': event.seats_min,
                'seats_availability': event.seats_availability,
                'seats_max': event.seats_max,
                'date_begin': event.date_begin,
                'date_end': event.date_end,
            })]
        return event


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    event_sessions_count = fields.Integer(
        related='event_id.sessions_count',
        readonly=True,
    )
    session_id = fields.Many2one(
        comodel_name='event.session',
        string='Session',
        ondelete='set null',
    )

    @api.multi
    @api.constrains('event_id', 'session_id', 'state')
    def _check_seats_limit(self):
        for registration in self:
            if (registration.session_id.seats_availability == 'limited' and
                    self.session_id.seats_max and
                    self.session_id.seats_available <
                    (1 if self.state == 'draft' else 0)):
                raise ValidationError(
                    _('No more seats available for this event.'))
