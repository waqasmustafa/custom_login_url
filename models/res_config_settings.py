# -*- coding: utf-8 -*-
from odoo import api, fields, models

def _slug_sanitize(slug: str) -> str:
    slug = (slug or "").strip().strip("/")
    import re
    slug = re.sub(r"[^A-Za-z0-9\-/]", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    return slug or "go/signin"

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    custom_login_enabled = fields.Boolean(
        string="Hide Default /web & /web/login",
        config_parameter="custom_login_url.enabled",
        default=False,
        help="If enabled, hide default login pages and use a custom path."
    )
    custom_login_slug = fields.Char(
        string="Custom Login Path (slug)",
        config_parameter="custom_login_url.slug",
        default="go/signin",
        help="Example: 'go/signin' -> https://yourdomain.com/go/signin. Changing this requires an Odoo restart."
    )
    custom_login_block_mode = fields.Selection(
        [("404", "Return 404 on /web & /web/login"), ("redirect", "Redirect to /")],
        string="Block Mode for /web & /web/login",
        config_parameter="custom_login_url.block_mode",
        default="404"
    )

    @api.onchange("custom_login_slug")
    def _onchange_custom_login_slug(self):
        if self.custom_login_slug:
            self.custom_login_slug = _slug_sanitize(self.custom_login_slug)
