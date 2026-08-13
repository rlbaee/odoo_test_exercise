from datetime import timedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    next_lead_status = fields.Selection(
        [
            ("never", "Never had a lead"),
            ("stale", "No lead in the past 28 days"),
        ],
        compute="_compute_next_lead_status",
    )

    @api.depends("user_ids")
    def _compute_next_lead_status(self):
        Lead = self.env["crm.lead"]
        cutoff = fields.Datetime.now() - timedelta(days=28)

        for partner in self:
            latest_lead = Lead.search(
                [("partner_id", "=", partner.id)],
                order="create_date desc",
                limit=1,
            )
            if not latest_lead:
                partner.next_lead_status = "never"
            elif latest_lead.create_date < cutoff:
                partner.next_lead_status = "stale"
            else:
                partner.next_lead_status = False

    def action_create_next_lead(self):
        self.ensure_one()

        lead = self.env["crm.lead"].create(
            {
                "name": self.name,
                "partner_id": self.id,
            }
        )

        return lead.get_formview_action()
