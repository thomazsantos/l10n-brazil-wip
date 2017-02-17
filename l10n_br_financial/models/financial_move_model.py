# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

FINANCIAL_MOVE = [
    ('r', u'Account Receivable'),
    ('p', u'Account Payable'),
]

FINANCIAL_IN_OUT = [
    ('rr', u'Receipt'),
    ('pp', u'Payment'),
]

FINANCIAL_TYPE = FINANCIAL_MOVE + FINANCIAL_IN_OUT

FINANCIAL_STATE = [
    ('draft', u'Draft'),
    ('open', u'Open'),
    ('paid', u'Paid'),
    ('cancel', u'Cancel'),
]


class FinancialMoveModel(models.AbstractModel):

    _name = 'financial.move.model'

    state = fields.Selection(
        selection=FINANCIAL_STATE,
        string='Status',
        index=True,
        readonly=True,
        default='draft',
        track_visibility='onchange',
        copy=False,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string=u'Company',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    document_number = fields.Char(
        string=u"Document Nº",
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    document_date = fields.Date(
        string=u"Data Emissão",
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    amount_document = fields.Monetary(
        string=u"Document amount",
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    due_date = fields.Date(
        string=u"Due date",
        # required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        track_visibility='onchange',
    )
    move_type = fields.Selection(
        selection=FINANCIAL_TYPE,
    )
    business_due_date = fields.Date(
        string='Business due date',
        compute='_compute_business_due_date',
        store=True,
        index=True,
        track_visibility='onchange',
    )

    @api.multi
    @api.constrains('amount_document')
    def _check_amount_document(self):
        for record in self:
            if record.amount_document <= 0:
                raise UserError(_(
                    "The amount document must be higher then ZERO!"))

    @api.multi
    @api.constrains('due_date')
    def _check_due_date(self):
        for record in self:
            if not record.due_date and record.move_type in ('p', 'r'):
                raise UserError(_(
                    "The finacial move must have a due date!"))

    @api.multi
    @api.depends('due_date')
    def _compute_business_due_date(self):
        for record in self:
            if record.due_date:
                record.business_due_date = self.env[
                    'resource.calendar'].proximo_dia_util(
                    fields.Date.from_string(record.due_date))

    def _prepare_financial_move(self, ref, ref_item, company_id, currency_id,
                                partner_id, document_number, document_date,
                                amount_document, due_date):
        return {}











@api.model
def _default_currency(self):
    journal = self._default_journal()
    return journal.currency_id or journal.company_id.currency_id