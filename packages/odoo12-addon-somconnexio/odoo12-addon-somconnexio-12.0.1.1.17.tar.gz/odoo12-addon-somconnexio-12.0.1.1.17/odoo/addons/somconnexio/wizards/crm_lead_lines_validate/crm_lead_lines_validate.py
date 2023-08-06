from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CRMLeadLinesValidateWizard(models.TransientModel):
    _name = 'crm.lead.lines.validate.wizard'
    crm_lead_line_ids = fields.Many2many('crm.lead.line')

    @api.multi
    def button_validate(self):
        for line in self.crm_lead_line_ids:
            if len(line.lead_id.lead_line_ids) > 1:
                raise ValidationError(_(
                    "The CRMLead to validate has more than one CRMLeadLine associated."
                    " This shouldn't happen. Please contact the IP team."
                ))
            else:
                line.lead_id.action_set_won()

        return True

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        crm_lead_line_ids = self.env.context['active_ids']
        defaults['crm_lead_line_ids'] = crm_lead_line_ids
        return defaults
