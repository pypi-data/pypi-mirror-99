from ..sc_test_case import SCTestCase
from odoo.exceptions import ValidationError


class BroadbandISPInfoTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.broadband_isp_info_args = {
            'type': 'new'
        }

    def test_new_creation_ok(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()
        broadband_isp_info = self.env['broadband.isp.info'].create(
            broadband_isp_info_args_copy
        )
        self.assertTrue(broadband_isp_info.id)

    def test_portability_creation_ok(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()
        previous_provider_id = self.env['previous.provider'].browse(3)

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': previous_provider_id.id,
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        broadband_isp_info = self.env['broadband.isp.info'].create(
            broadband_isp_info_args_copy
        )
        self.assertTrue(previous_provider_id.broadband)
        self.assertTrue(broadband_isp_info.id)

    def test_portability_wrong_previous_provider(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()
        previous_provider_id = self.env['previous.provider'].browse(1)

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': previous_provider_id.id,
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertFalse(previous_provider_id.broadband)
        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_provider(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': None,
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'phone_number': '666335678',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_phone_number(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref('somconnexio.previousprovider3'),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
            'previous_service': 'adsl'
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )

    def test_portability_without_previous_service(self):
        broadband_isp_info_args_copy = self.broadband_isp_info_args.copy()

        broadband_isp_info_args_copy.update({
            'type': 'portability',
            'previous_provider': self.ref('somconnexio.previousprovider3'),
            'previous_owner_vat_number': '1234G',
            'previous_owner_name': 'Ford',
            'previous_owner_first_name': 'Windom',
        })

        self.assertRaises(
            ValidationError,
            self.env['broadband.isp.info'].create,
            [broadband_isp_info_args_copy]
        )
