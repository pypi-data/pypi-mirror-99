# -*- coding: utf-8 -*-

from ..sc_test_case import SCTestCase


class TestContractIBANChangeWizard(SCTestCase):

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.Contract = self.env['contract.contract']
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
            'bank_id': self.partner.bank_ids.id
        }
        self.contract = self.env['contract.contract'].create(vals_contract)
        vals_contract_same_partner = vals_contract.copy()
        vals_contract_same_partner.update({
            'name': 'Test Contract Broadband B'
        })
        self.contract_same_partner = self.env['contract.contract'].with_context(
            tracking_disable=True
        ).create(
            vals_contract_same_partner
        )
        self.bank_b = self.env['res.partner.bank'].create({
            'acc_number': 'ES1720852066623456789011',
            'partner_id': self.partner.id
        })
        self.banking_mandate = self.env['account.banking.mandate'].search(
            [('partner_bank_id', '=', self.bank_b.id)]
        )

    def test_wizard_iban_change_ok(self):
        wizard = self.env['contract.iban.change.wizard'].with_context(
            active_id=self.partner.id
        ).create({
            'contract_ids': [(6, 0, [
                self.contract_same_partner.id, self.contract.id
            ])],
            'account_banking_mandate_id': self.banking_mandate.id
        })
        wizard.button_change()
        self.assertEquals(self.contract_same_partner.mandate_id, self.banking_mandate)
        self.assertEquals(self.contract.mandate_id, self.banking_mandate)
