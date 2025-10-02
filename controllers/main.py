# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo import api, SUPERUSER_ID
from odoo.tools import config as odoo_config
from odoo.sql_db import db_connect
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect

def _cfg_bool(key, default=False):
    val = request.env["ir.config_parameter"].sudo().get_param(key, "True" if default else "False")
    return str(val) == "True"

def _cfg_str(key, default=""):
    return (request.env["ir.config_parameter"].sudo().get_param(key) or default).strip()

# Fixed internal route used for instant changes via Website Redirect
INTERNAL_LOGIN_PATH = "/_login_cloak"

class CustomLoginURLController(http.Controller):

    # 1) Custom GET: show login form at INTERNAL_LOGIN_PATH (always available)
    @http.route(INTERNAL_LOGIN_PATH, type="http", auth="public", website=True, methods=["GET"])
    def login_form_get(self, **kw):
        if not _cfg_bool("custom_login_url.enabled", False):
            # Feature disabled: fall back to the normal login
            return redirect("/web/login")
        if request.session.uid:
            return redirect("/web")
        # Prepare context similar to Odoo login
        qcontext = request.env["ir.http"].sudo().get_frontend_menu_qcontext()
        qcontext.update({
            "error": kw.get("error"),
            "login": kw.get("login"),
            "redirect": kw.get("redirect") or request.params.get("redirect") or "/web",
            "databases": [],
        })
        return request.render("web.login", qcontext)

    # 2) Custom POST: authenticate then redirect
    @http.route(INTERNAL_LOGIN_PATH, type="http", auth="public", website=True, methods=["POST"], csrf=True)
    def login_form_post(self, **post):
        if not _cfg_bool("custom_login_url.enabled", False):
            return redirect("/web/login")
        login = post.get("login")
        password = post.get("password")
        db = request.session.db or http.db_monodb()
        redirect_to = post.get("redirect") or "/web"
        try:
            uid = request.session.authenticate(db, login, password)
            if uid:
                return redirect(redirect_to)
        except Exception:
            pass
        return self.login_form_get(error=_("Wrong login/password"), login=login, redirect=redirect_to)

    # 3) Block the default /web/login (GET & POST)
    @http.route("/web/login", type="http", auth="public", website=True, methods=["GET", "POST"])
    def block_default_login(self, **kw):
        if not _cfg_bool("custom_login_url.enabled", False):
            # If feature off, render normal login
            q = request.env["ir.http"].sudo().get_frontend_menu_qcontext()
            q.update({"databases": []})
            return request.render("web.login", q)

        mode = _cfg_str("custom_login_url.block_mode", "404")
        if mode == "redirect":
            return redirect("/")
        raise NotFound()
