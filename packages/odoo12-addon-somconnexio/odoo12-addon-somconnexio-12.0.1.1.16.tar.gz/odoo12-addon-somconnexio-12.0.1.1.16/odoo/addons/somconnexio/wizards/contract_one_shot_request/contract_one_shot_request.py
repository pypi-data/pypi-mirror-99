# -*- coding: utf-8 -*-
from datetime import datetime, date
from calendar import monthrange

from odoo import models, fields, api, _


class ContractOneShotRequestWizard(models.TransientModel):
    _name = 'contract.one.shot.request.wizard'
    contract_id = fields.Many2one('contract.contract')

    product_category_id = fields.Many2one(
        'product.category',
        compute="_load_product_category_id"
    )
    start_date = fields.Date('Start Date', required=True)
    one_shot_product_id = fields.Many2one(
        'product.product',
        string='One Shot products',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults['contract_id'] = self.env.context['active_id']
        defaults['start_date'] = datetime.strftime(date.today(), "%Y-%m-%d")
        return defaults

    @api.depends("contract_id")
    def _load_product_category_id(self):
        if not self.contract_id:
            return False

        if self.contract_id.service_technology_id.id == self.env.ref(
                'somconnexio.service_technology_mobile').id:
            self.product_category_id = self.env.ref(
                'somconnexio.mobile_oneshot_service').id
        else:
            self.product_category_id = self.env.ref(
                'somconnexio.broadband_oneshot_service').id

    def button_add(self):
        self.ensure_one()

        one_shot_contract_line = {
            "name": self.one_shot_product_id.name,
            "product_id": self.one_shot_product_id.id,
            "date_start": self.start_date,
            "date_end": self._get_last_day_of_month(self.start_date)
        }

        self.contract_id.write(
            {'contract_line_ids': [(0, 0, one_shot_contract_line)]}
        )

        message = _("One shot product '{}' added on '{}'")
        self.contract_id.message_post(
            message.format(
                self.one_shot_product_id.showed_name,
                self.start_date,
            )
        )
        return True

    def _get_last_day_of_month(self, request_date):
        #  Touple with weekday (0-6) and number of days (28-31) for a given month
        month_range = monthrange(request_date.year, request_date.month)

        return date(request_date.year, request_date.month, month_range[1])
