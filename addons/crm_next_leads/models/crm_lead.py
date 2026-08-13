from datetime import timedelta

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    next_lead_partner_ids = fields.One2many(
        "res.partner",
        compute="_compute_next_lead_partner_ids",
        readonly=True,
    )

    @api.depends()
    def _compute_next_lead_partner_ids(self):
        Partner = self.env["res.partner"]
        Lead = self.env["crm.lead"]
        cutoff = fields.Datetime.now() - timedelta(days=28)

        partners = Partner.search([("user_ids", "=", False)])

        leads = Lead.search([("partner_id", "in", partners.ids)])
        latest_lead_by_partner = {}
        for lead in leads:
            partner_id = lead.partner_id.id
            if (
                partner_id not in latest_lead_by_partner
                or lead.create_date > latest_lead_by_partner[partner_id]
            ):
                latest_lead_by_partner[partner_id] = lead.create_date

        eligible_partners = partners.filtered(
            lambda partner: (
                partner.id not in latest_lead_by_partner
                or latest_lead_by_partner[partner.id] < cutoff
            )
        )

        for lead in self:
            lead.next_lead_partner_ids = eligible_partners
