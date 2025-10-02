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
        help="Enter your custom login path (e.g., 'vault', 'admin-panel'). Changes apply instantly."
    )
    custom_login_block_mode = fields.Selection(
        [("404", "Return 404 on /web & /web/login"), ("redirect", "Redirect to /")],
        string="Block Mode for /web & /web/login",
        config_parameter="custom_login_url.block_mode",
        default="404"
    )

    custom_login_preview_url = fields.Char(
        string="Login URL",
        compute="_compute_custom_login_preview_url",
        readonly=True
    )

    custom_login_base_url = fields.Char(
        string="Base URL",
        compute="_compute_custom_login_base_url",
        readonly=True
    )

    @api.onchange("custom_login_slug")
    def _onchange_custom_login_slug(self):
        if self.custom_login_slug:
            self.custom_login_slug = _slug_sanitize(self.custom_login_slug)

    @api.depends("custom_login_slug")
    def _compute_custom_login_preview_url(self):
        base = self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        for rec in self:
            if rec.custom_login_slug:
                slug = _slug_sanitize(rec.custom_login_slug)
                rec.custom_login_preview_url = (base.rstrip("/") + "/" + slug) if base else "/" + slug
            else:
                rec.custom_login_preview_url = "Enter a custom path above"

    def _compute_custom_login_base_url(self):
        base = self.env["ir.config_parameter"].sudo().get_param("web.base.url") or ""
        base = base.rstrip("/") + "/" if base else "/"
        for rec in self:
            rec.custom_login_base_url = base

    def set_values(self):
        res = super().set_values()
        # Create or update Website Redirect to allow instant slug change without restart
        if self.custom_login_enabled and self.custom_login_slug:
            try:
                WebsiteRedirect = self.env["website.redirect"].sudo()
                website = self.env["website"].sudo().get_current_website()
                source = "/" + _slug_sanitize(self.custom_login_slug)
                target = "/_login_cloak"
                # Look for existing redirect for login cloak
                existing = WebsiteRedirect.search([
                    ("website_id", "=", website.id if website else False),
                    ("redirect_type", "=", "301"),
                    ("url_from", "=", source),
                ], limit=1)
                # Remove any old redirects pointing to target but with different source
                WebsiteRedirect.search([
                    ("website_id", "=", website.id if website else False),
                    ("url_to", "=", target),
                    ("url_from", "!=", source),
                ]).unlink()
                if existing:
                    existing.write({"url_to": target})
                else:
                    WebsiteRedirect.create({
                        "website_id": website.id if website else False,
                        "url_from": source,
                        "url_to": target,
                        "redirect_type": "301",
                        "active": True,
                    })
            except Exception:
                # If website module is not installed, ignore silently
                pass
        return res
