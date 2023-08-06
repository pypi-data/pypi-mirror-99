from odoo import _, models, fields, api
from odoo.exceptions import ValidationError, UserError

from ..services.vat_normalizer import VATNormalizer

import logging
_logger = logging.getLogger(__name__)
try:
    from stdnum.es.nie import is_valid as valid_nie
except (ImportError, IOError) as err:
    _logger.debug(err)


class SubscriptionRequest(models.Model):
    _inherit = ['subscription.request', 'mail.thread']
    _name = "subscription.request"

    iban = fields.Char(required=True)

    type = fields.Selection(
        selection=[
            ("new", "New Cooperator"),
            ('sponsorship', 'Sponsorship'),
            ("sponsorship_coop_agreement", "Sponsorship Coop Agreement"),
        ],
    )

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
    nationality = fields.Many2one('res.country', 'Nationality')

    payment_type = fields.Selection([
        ('single', 'One single payment'),
        ('split', 'Ten payments')
    ])

    state_id = fields.Many2one('res.country.state', 'Province')
    discovery_channel_id = fields.Many2one('discovery.channel', 'Discovery Channel')

    verbose_name = fields.Char(compute='_get_verbose_name', store=True)
    _rec_name = 'verbose_name'

    @api.depends('firstname', 'lastname', 'type', 'company_name')
    def _get_verbose_name(self):
        for sr in self:
            if sr.is_company:
                sr.verbose_name = f'{sr.company_name} - {sr.type}'
            else:
                sr.verbose_name = "{} {} - {}".format(
                    sr.firstname, sr.lastname, sr.type
                )

    def get_journal(self):
        # Redefine the get_journal of EMC to get the SUBJ journal:
        # https://github.com/coopiteasy/vertical-cooperative/blob/12.0/easy_my_coop/models/coop.py#L522  # noqa
        return self.env.ref('somconnexio.subscription_journal')

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = VATNormalizer(self.vat).convert_spanish_vat()
        values["state_id"] = self.state_id.id
        values["phone"] = self.phone
        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = VATNormalizer(self.vat).convert_spanish_vat()
        values["nationality"] = self.nationality.id
        values["state_id"] = self.state_id.id
        return values

    @api.one
    def vinculate_partner_in_lead(self):
        leads = self.env['crm.lead'].search([
            ('subscription_request_id', '=', self.id)
        ])
        for lead in leads:
            lead.partner_id = self.partner_id

    @api.one
    @api.constrains('coop_agreement_id', 'type')
    def _check_coop_agreement_id(self):
        if self.type == 'sponsorship_coop_agreement' and not self.coop_agreement_id:
            raise ValidationError(
                "If it's a Coop Agreement sponsorship the Coop Agreement must be set."
            )

    @api.one
    @api.constrains('vat', 'nationality')
    def _check_nie_nationality(self):
        if valid_nie(self.vat) and not self.nationality:
            raise ValidationError('If a NIE is provided, nationality is mandatory.')

    def get_invoice_vals(self, partner):
        invoice_vals = super().get_invoice_vals(partner)
        if self.payment_type == 'split':
            invoice_vals['payment_term_id'] = self.env.ref(
                'somconnexio.account_payment_term_10months'
            ).id
        invoice_vals['payment_mode_id'] = self.env.ref(
            'somconnexio.payment_mode_inbound_sepa'
        ).id
        return invoice_vals

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            records = self.env['subscription.request'].search([
                '|', '|', '|', '|',
                ('vat', operator, name),
                ('email', operator, name),
                ('firstname', operator, name),
                ('lastname', operator, name),
                ('name', operator, name),
                ],
                limit=limit
            )
            return models.lazy_name_get(records)
        return []

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    @api.model
    def create(self, vals):
        subscr_request = super(models.Model, self).create(vals)

        if self._send_confirmation_email():
            mail_template_notif = subscr_request.get_mail_template_notif(False)
            mail_template_notif.send_mail(subscr_request.id)

        return subscr_request

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    @api.model
    def create_comp_sub_req(self, vals):
        subscr_request = super(models.Model, self).create(vals)

        if self._send_confirmation_email():
            confirmation_mail_template = subscr_request.get_mail_template_notif(
                True
            )
            confirmation_mail_template.send_mail(subscr_request.id)

        return subscr_request

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    def _send_confirmation_email(self):
        return self.company_id.send_confirmation_email

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    def send_capital_release_request(self, invoice):
        email_template = self.get_capital_release_mail_template()

        if self.company_id.send_capital_release_email:
            # we send the email with the capital release request in attachment
            # TODO remove sudo() and give necessary access right
            email_template.sudo().send_mail(invoice.id, True)
            invoice.sent = True

    @api.multi
    def validate_subscription_request(self):
        self.ensure_one()

        if self.ordered_parts == 0 and self.type in self.sponsorship_types():
            return self._validate_sponsorship_subscription_request()
        elif self.ordered_parts > 0:
            return self._validate_member_subscription_request()
        elif self.ordered_parts <= 0:
            raise UserError(_("Number of share must be greater than 0."))

    def _validate_member_subscription_request(self):
        self.ensure_one()
        # todo rename to validate (careful with iwp dependencies)

        self.partner = self.get_create_partner()

        self.write({"state": "done"})
        self.vinculate_partner_in_lead()

        # Create invoice for shares
        invoice = self.create_invoice(self.partner)
        self.set_membership()

        return invoice

    def _validate_sponsorship_subscription_request(self):
        self.ensure_one()
        # todo rename to validate (careful with iwp dependencies)

        self.partner = self.get_create_partner()

        self.write({"state": "done"})
        self.vinculate_partner_in_lead()

    def get_create_partner(self):
        if self.partner_id:
            partner = self.partner_id
        else:
            partner = None
            if self.already_cooperator:
                raise UserError(
                    _(
                        "The checkbox already cooperator is"
                        " checked please select a cooperator."
                    )
                )
            elif self.vat:
                domain = [("vat", "ilike", self.vat)]
                partner = self.env["res.partner"].search(domain)

            if not partner:
                partner = self.create_coop_partner()
                self.partner_id = partner
            else:
                raise UserError(
                    _(
                        "A partner with VAT %s already exists in our system"
                    ) % self.vat
                )

            partner.cooperator = True
        return partner

    def sponsorship_types(self):
        return ['sponsorship_coop_agreement', 'sponsorship']

    def set_membership(self):
        # Remove the sponsor_id relation
        self._remove_sponsor_relation()

    def _remove_sponsor_relation(self):
        if self.partner and self.partner.sponsor_id:
            sponsor = self.partner.sponsor_id
            self.partner.write({"sponsor_id": False})
            self.partner.message_post(
                _("Partner sponsored by {name} with VAT {vat} converted to cooperator.").format(  # noqa
                    name=sponsor.name,
                    vat=sponsor.vat,
                )
            )
