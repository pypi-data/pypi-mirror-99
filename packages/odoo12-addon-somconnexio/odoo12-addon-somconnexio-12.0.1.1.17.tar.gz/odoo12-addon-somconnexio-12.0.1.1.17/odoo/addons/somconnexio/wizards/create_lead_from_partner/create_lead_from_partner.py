# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CreateLeadFromPartnerWizard(models.TransientModel):
    _name = "partner.create.lead.wizard"

    partner_id = fields.Many2one("res.partner")
    title = fields.Char(
        readonly=True,
        translate=True,
    )
    opportunity = fields.Char(required=True)
    bank_id = fields.Many2one(
        "res.partner.bank",
        string="Bank Account",
        required=True,
    )
    available_email_ids = fields.Many2many(
        "res.partner",
        compute="_load_available_email_ids",
        required=True,
    )
    email_id = fields.Many2one(
        "res.partner",
        string="Email",
        required=True,
    )
    phone_contact = fields.Char(
        string="Contact phone number",
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        string="Requested product",
        required=True,
    )
    service_type = fields.Char(default="",)
    icc = fields.Char(string="ICC")
    type = fields.Selection(
        [("portability", "Portability"), ("new", "New")],
        string="Type",
        required=True,
    )
    previous_contract_type = fields.Selection(
        [("contract", "Contract"), ("prepaid", "Prepaid")],
        string="Previous Contract Type",
    )
    phone_number = fields.Char(string="Phone number")
    donor_icc = fields.Char(string="ICC Donor")
    previous_mobile_provider = fields.Many2one(
        "previous.provider",
        string="Previous Provider"
    )
    previous_BA_provider = fields.Many2one(
        "previous.provider",
        string="Previous Provider"
    )
    previous_owner_vat_number = fields.Char(string="Previous Owner VatNumber")
    previous_owner_first_name = fields.Char(string="Previous Owner First Name")
    previous_owner_name = fields.Char(string="Previous Owner Name")
    keep_landline = fields.Boolean(string="Keep Phone Number", default=False,)
    landline = fields.Char(string="Landline Phone Number")
    previous_BA_service = fields.Selection(
        selection=[
            ("fiber", "Fiber"),
            ("adsl", "ADSL")
        ],
        string="Previous Service"
    )

    # Addresses
    delivery_street = fields.Char(string="Delivery Street", required=True)
    delivery_zip_code = fields.Char(string="Delivery ZIP", required=True)
    delivery_city = fields.Char(string="Delivery City", required=True)
    delivery_state_id = fields.Many2one(
        "res.country.state",
        string="Delivery State",
        required=True
    )
    delivery_country_id = fields.Many2one(
        "res.country",
        string="Delivery Country",
        required=True
    )
    invoice_street = fields.Char(string="Invoice Street")
    invoice_zip_code = fields.Char(string="Invoice ZIP")
    invoice_city = fields.Char(string="Invoice City")
    invoice_state_id = fields.Many2one(
        "res.country.state",
        string="Invoice State"
    )
    invoice_country_id = fields.Many2one(
        "res.country",
        string="Invoice Country"
    )
    service_street = fields.Char(string="Service Street")
    service_zip_code = fields.Char(string="Service ZIP")
    service_city = fields.Char(string="Service City")
    service_state_id = fields.Many2one(
        "res.country.state",
        string="Service State"
    )
    service_country_id = fields.Many2one(
        "res.country",
        string="Service Country"
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        defaults["partner_id"] = self.env.context["active_id"]
        spain_country_id = self.env["res.country"].search([("code", "=", "ES")]).id
        defaults["service_country_id"] = spain_country_id
        defaults["delivery_country_id"] = spain_country_id
        defaults["invoice_country_id"] = spain_country_id
        defaults["title"] = _("Manual CRMLead creation from partner")
        return defaults

    @api.multi
    @api.depends("partner_id")
    def _load_available_email_ids(self):
        if self.partner_id:
            self.available_email_ids = [
                (6, 0, self.partner_id.get_available_email_ids())
            ]

    @api.onchange("product_id")
    def onchange_product_id(self):
        if not self.product_id:
            pass
        else:
            if self.product_id.product_tmpl_id.categ_id == self.env.ref(
                    "somconnexio.mobile_service"):
                self.service_type = "mobile"
            else:
                # available products for selection are only mobile/BA services
                self.service_type = "BA"

    def create_lead(self):
        self.ensure_one()

        line_params = {
            "name": self.product_id.name,
            "product_id": self.product_id.id,
            "product_tmpl_id": self.product_id.product_tmpl_id.id,
            "category_id": self.product_id.product_tmpl_id.categ_id.id,
        }

        isp_info_args = {
            "type": self.type,
            "delivery_street": self.delivery_street,
            "delivery_zip_code": self.delivery_zip_code,
            "delivery_city": self.delivery_city,
            "delivery_state_id": self.delivery_state_id.id,
            "delivery_country_id": self.delivery_country_id.id,
            "invoice_street": self.invoice_street,
            "invoice_zip_code": self.invoice_zip_code,
            "invoice_city": self.invoice_city,
            "invoice_state_id": self.invoice_state_id.id,
            "invoice_country_id": self.invoice_country_id.id,
            "previous_owner_vat_number": self.previous_owner_vat_number,
            "previous_owner_name": self.previous_owner_name,
            "previous_owner_first_name": self.previous_owner_first_name,
        }

        if self.service_type == "mobile":
            isp_info_args.update({
                "icc": self.icc,
                "icc_donor": self.donor_icc,
                "phone_number": self.phone_number,
                "previous_contract_type": self.previous_contract_type,
                "previous_provider": self.previous_mobile_provider.id,
            })

            mobile_isp_info = self.env["mobile.isp.info"].create(isp_info_args)

            line_params.update({"mobile_isp_info": mobile_isp_info.id, })

        elif self.service_type == "BA":
            isp_info_args.update({
                "keep_phone_number": self.keep_landline,
                "phone_number": self.landline,
                "previous_service": self.previous_BA_service,
                "previous_provider": self.previous_BA_provider.id,
                "service_street": self.service_street,
                "service_zip_code": self.service_zip_code,
                "service_city": self.service_city,
                "service_state_id": self.service_state_id.id,
                "service_country_id": self.service_country_id.id,
            })

            broadband_isp_info = self.env["broadband.isp.info"].create(isp_info_args)

            line_params.update({"broadband_isp_info": broadband_isp_info.id, })

        crm_lead_line = self.env["crm.lead.line"].create(line_params)

        crm_lead = self.env["crm.lead"].create({
            "name": self.opportunity,
            "description": "",
            "partner_id": self.partner_id.id,
            "iban": self.bank_id.sanitized_acc_number,
            "email": self.email_id.email,
            "lead_line_ids": [(6, 0, [crm_lead_line.id])]
        })

        action = self.env["ir.actions.act_window"].for_xml_id(
            "crm",
            "crm_lead_all_leads")

        action.update({
            "views": [[
                self.env.ref("somconnexio.crm_case_form_view_oppor_inherit").id,
                "form"
            ]],
            "res_id": crm_lead.id,
        })

        return action
