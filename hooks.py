# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    """Run after module installation.

    - Ensure the feature starts disabled
    - Clear any default slug so user must set their own
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    icp = env["ir.config_parameter"].sudo()
    # Set defaults only if not explicitly set yet
    if icp.get_param("custom_login_url.enabled") is None:
        icp.set_param("custom_login_url.enabled", "False")
    if icp.get_param("custom_login_url.slug") is None:
        icp.set_param("custom_login_url.slug", "")

