# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import models, fields, api, _


class ContractTariffChangeWizard(models.TransientModel):
    _name = 'contract.tariff.change.wizard'
    contract_id = fields.Many2one('contract.contract')

    product_category_id = fields.Many2one(
        'product.category',
        compute="_load_product_category_id"
    )
    start_date = fields.Date('Start Date', required=True)

    current_tariff_contract_line = fields.Many2one(
        'contract.line',
        related='contract_id.current_tariff_contract_line',
    )

    current_tariff_product = fields.Many2one(
        'product.product',
        related='current_tariff_contract_line.product_id',
        string="Current Tariff"
    )

    new_tariff_product_id = fields.Many2one(
        'product.product',
        string='New tariff',
    )

    discontinued = fields.Boolean(
        related='new_tariff_product_id.discontinued',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['contract_id'] = self.env.context['active_id']
        defaults['start_date'] = self._get_first_day_of_next_month(date.today())
        return defaults

    @api.depends("contract_id")
    def _load_product_category_id(self):
        if not self.contract_id:
            return False

        if self.contract_id.service_technology_id.id == self.env.ref(
                'somconnexio.service_technology_mobile').id:
            self.product_category_id = self.env.ref(
                'somconnexio.mobile_service')
        elif self.contract_id.service_technology_id.id == self.env.ref(
                'somconnexio.service_technology_fiber').id:
            self.product_category_id = self.env.ref(
                'somconnexio.broadband_fiber_service')
        else:
            self.product_category_id = self.env.ref(
                'somconnexio.broadband_adsl_service').id

    def button_change(self):
        self.ensure_one()

        current_tariff_line_dct = {
            "name": self.current_tariff_contract_line.product_id.name,
            "product_id": self.current_tariff_contract_line.product_id.id,
            "date_start": self.current_tariff_contract_line.date_start,
            "date_end": self.start_date - timedelta(days=1)
        }
        new_tariff_line_dct = {
            "name": self.new_tariff_product_id.name,
            "product_id": self.new_tariff_product_id.id,
            "date_start": self.start_date,
        }
        self.contract_id.write(
            {'contract_line_ids': [
                (0, 0, new_tariff_line_dct),
                (1, self.current_tariff_contract_line.id, current_tariff_line_dct)
            ]}
        )
        message = _("Contract tariff to be changed from '{}' to '{}' with start_date: {}")  # noqa
        self.contract_id.message_post(
            message.format(
                self.current_tariff_contract_line.product_id.showed_name,
                self.new_tariff_product_id.showed_name,
                self.start_date,
            )
        )
        return True

    def _get_first_day_of_next_month(self, request_date):
        if request_date.month == 12:
            return date(request_date.year+1, 1, 1)
        else:
            return date(request_date.year, request_date.month+1, 1)
