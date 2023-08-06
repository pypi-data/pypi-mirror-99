# -*- coding: utf-8 -*-

from datetime import date

from ..sc_test_case import SCTestCase


class TestContractHolderChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.vodafone_fiber_contract_service_info = self.env[
            'vodafone.fiber.service.contract.info'
        ].create({
            'phone_number': '654321123',
            'vodafone_id': '123',
            'vodafone_offer_code': '456',
        })
        self.partner = self.browse_ref('base.partner_demo')
        partner_id = self.partner.id
        service_partner = self.env['res.partner'].create({
            'parent_id': partner_id,
            'name': 'Partner service OK',
            'type': 'service'
        })
        contract_line = {
            "name": "Hola",
            "product_id": self.browse_ref('somconnexio.Fibra600Mb').id,
            "date_start": '2020-01-01'
        }
        vals_contract = {
            'name': 'Test Contract Broadband',
            'partner_id': partner_id,
            'service_partner_id': service_partner.id,
            'invoice_partner_id': partner_id,
            'service_technology_id': self.ref(
                "somconnexio.service_technology_fiber"
            ),
            'service_supplier_id': self.ref(
                "somconnexio.service_supplier_vodafone"
            ),
            'vodafone_fiber_service_contract_info_id': (
                self.vodafone_fiber_contract_service_info.id
            ),
            'bank_id': self.partner.bank_ids.id,
            'contract_line_ids': [(0, 0, contract_line)],
        }

        self.contract = self.env['contract.contract'].create(vals_contract)

        self.partner_b = self.browse_ref('base.res_partner_1')

    def test_wizard_holder_change_ok(self):
        group_can_terminate_contract = self.env.ref(
            "contract.can_terminate_contract"
        )
        group_can_terminate_contract.users |= self.env.user

        service_partner_b = self.env['res.partner'].create({
            'parent_id': self.partner_b.id,
            'name': 'Partner B service OK',
            'type': 'service'
        })

        wizard = self.env['contract.holder.change.wizard'].with_context(
            active_id=self.contract.id
        ).create({
            'change_date': date.today(),
            'partner_id': self.partner_b.id,
            'invoice_partner_id': self.partner_b.id,
            'service_partner_id': service_partner_b.id,
            'bank_id': self.partner_b.bank_ids.id
        })
        wizard.button_change()

        self.assertTrue(self.contract.is_terminated)

        new_contract = self.env['contract.contract'].search([
            ('partner_id', '=', self.partner_b.id)
        ])

        self.assertEqual(
            self.contract.service_supplier_id,
            new_contract.service_supplier_id
        )
        self.assertEqual(
            self.contract.service_technology_id,
            new_contract.service_technology_id
        )
        self.assertEqual(
            self.contract.vodafone_fiber_service_contract_info_id,
            new_contract.vodafone_fiber_service_contract_info_id
        )
        self.assertEqual(
            self.contract.contract_line_ids[0].date_end,
            date.today()
        )
        self.assertEqual(
            new_contract.contract_line_ids[0].date_start,
            date.today()
        )
