# -*- coding: utf-8 -*-
{
    'name': 'Custom Login URL',
    'summary': 'Hide default /web & /web/login and use a custom, secret login path.',
    'version': '18.0.2.0.0',
    'description': '''
Secure your Odoo by hiding the default login endpoints and exposing a private login URL of your choice.

Key Features:
- Hide default /web and /web/login for public users (404 or redirect)
- Custom login path (e.g., /go/signin) configurable in Settings
- Uses Odoo built-in login template (web.login)
- Authenticates via request.session.authenticate(...) and redirects to /web
- Instant slug changes via Website Redirect to an internal route (no restart)

Notes:
- Only exact /web and /web/login are blocked; assets like /web/assets remain intact
    ''',
    'author': 'Waqas Mustafa | Ezcodesolution',
    'website': 'https://www.linkedin.com/in/waqas-mustafa-ba5701209/',
    'support': 'mustafawaqas0@gmail.com',
    'license': 'LGPL-3',
    'category': 'Tools',
    'depends': ['web'],
    'data': [
        'data/ir_config_parameter.xml',
        'views/res_config_settings_view.xml',
    ],
    'assets': {},
    'installable': True,
    'application': False,
    'auto_install': False,
}
