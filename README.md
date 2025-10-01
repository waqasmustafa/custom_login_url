# Custom Login URL (Odoo 18)

Hide default `/web` & `/web/login` for public users and use a private custom login path instead.

## Features
- Blocks `/web` and `/web/login` from public users (404 or redirect).
- Serves the normal Odoo login form at a **custom path** (default: `/go/signin`).
- Settings → General Settings section to enable/disable and set slug.
- On successful login, redirects to `/web` as usual.

> **Note on slug changes:** Odoo routes are declared at import time. Changing the slug in settings requires an Odoo restart to apply.  
> **Workaround (no restart):** If you use the Website app, add a redirect from your desired slug (e.g., `/vault`) to the active route (e.g., `/go/signin`).

## Install
1. Copy `custom_login_url/` to your addons path.
2. Update Apps list and install **Custom Login URL**.
3. Go to **Settings → General Settings → Custom Login URL**.
4. Enable, set the slug (e.g., `go/signin`), and save.
5. Access login at `https://yourdomain.com/go/signin`.
6. Visiting `/web` or `/web/login` as a public user will return 404 (or redirect).

## Security Tips
- Choose a non-obvious slug (e.g., `/vault-92`).
- Avoid exposing the URL publicly.
- Consider pairing with Nginx edge rules for extra safety.
