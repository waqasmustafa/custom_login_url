# Login Cloak – Hide Web/Login & Custom URL (Odoo 18)

🛡️ **Secure your Odoo by hiding default login endpoints and exposing a private login URL of your choice.**

## 🚀 Key Features

- **Hide Default Routes**: Blocks `/web` and `/web/login` for public users (404 or redirect)
- **Custom Login Path**: Configurable slug (e.g., `/go/signin`) via Settings
- **Instant Changes**: URL changes apply immediately via Website Redirect (no restart required)
- **Built-in Template**: Uses Odoo's native `web.login` template
- **Secure Authentication**: Authenticates via `request.session.authenticate(...)`
- **Asset Protection**: Only exact `/web` and `/web/login` are blocked; assets like `/web/assets` remain intact

## 📋 Requirements

- Odoo 18.0
- Dependencies: `base`, `web`, `website`

## 🔧 Installation

1. **Copy Module**: Place `custom_login_url/` in your Odoo addons directory
2. **Update Apps**: Go to Apps → Update Apps List
3. **Install Module**: Search for "Login Cloak" and install
4. **Configure**: Go to Settings → General Settings → Custom Login URL

## ⚙️ Configuration

### Settings Options

| Setting | Description | Default |
|---------|-------------|---------|
| **Hide Default /web & /web/login** | Enable/disable the feature | ❌ Disabled |
| **Custom Login Path (slug)** | Your secret login path | Empty (user must set) |
| **Block Mode** | How to block default routes | `404` |
| **Login URL Preview** | Full generated URL | "Enter a custom path above" |

### Block Modes

- **404**: Returns "Page Not Found" for `/web` and `/web/login`
- **Redirect**: Redirects to `/` (homepage) instead

## 🎯 Usage

### 1. Basic Setup
1. Go to **Settings → General Settings → Custom Login URL**
2. **Enable the feature**: Check "Hide Default /web & /web/login"
3. **Set your custom path**: Enter your desired slug (e.g., `vault`, `admin-panel`, `secure-login`)
4. Click **Save**

### 2. Access Your Login
- **Your Login URL**: `https://yourdomain.com/your-slug`
- **Example**: If slug is `vault` → `https://yourdomain.com/vault`

### 3. What Happens After Enabling
- ✅ **Your custom URL**: Shows Odoo login form
- ❌ **`/web/login`**: Returns 404 (or redirects to `/`)
- ❌ **`/web`**: No login page exposed for public users
- ✅ **`/web/assets`**: Still works (static files untouched)

### 4. Default Behavior (When Disabled)
- ✅ **`/web/login`**: Works normally (default Odoo login)
- ✅ **`/web`**: Works normally
- ❌ **Custom URL**: Not active until you enable and set a path

## 🔄 Instant URL Changes

**No Restart Required!** When you change the slug in settings:

1. The system automatically creates a Website Redirect
2. Your new URL works immediately
3. Old redirects are cleaned up automatically

**Example Flow:**
- Change slug from `admin-panel` to `vault`
- Save settings
- `https://yourdomain.com/vault` works instantly
- `https://yourdomain.com/admin-panel` still works (redirects to `vault`)

## 🛡️ Security Best Practices

### Strong Slug Examples
```
✅ Good: vault-2024, admin-panel, secure-login, my-company-access, private-entry
❌ Avoid: login, admin, signin, portal, web, dashboard
```

### Additional Security
- **Nginx Rules**: Add edge rules to block common login paths
- **IP Restrictions**: Limit access to specific IP ranges
- **HTTPS Only**: Ensure SSL is enabled
- **Regular Updates**: Keep your slug secret and change periodically

## 🔍 Troubleshooting

### Common Issues

**Q: Module won't install**
- Ensure you have `website` module installed
- Check that all dependencies are met

**Q: Custom URL shows 404**
- Ensure the feature is enabled in Settings
- Verify the slug is set correctly in Settings
- Check that Website Redirects are working
- Try accessing the internal route `/_login_cloak` directly

**Q: `/web/login` still shows login form**
- Ensure the feature is enabled in Settings
- Check that the module is properly installed
- Clear browser cache

**Q: Assets (CSS/JS) not loading**
- This is normal - only `/web` and `/web/login` are blocked
- Assets under `/web/assets` should work fine

### Debug Mode
To temporarily disable the feature:
1. Go to Settings → Custom Login URL
2. Uncheck "Hide Default /web & /web/login"
3. Save - now `/web/login` works normally

### First-Time Setup
When you first install the module:
1. **Module is disabled by default** - `/web` and `/web/login` work normally
2. **No default path set** - you must choose your own custom path
3. **Enable when ready** - check the box and set your path when you want to activate the feature

## 📁 Module Structure

```
custom_login_url/
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── main.py              # Route handlers
├── models/
│   ├── __init__.py
│   └── res_config_settings.py  # Settings model
├── views/
│   └── res_config_settings_view.xml  # Settings UI
├── data/
│   └── ir_config_parameter.xml       # Default values
└── README.md
```

## 🤝 Support

- **Author**: Waqas Mustafa | Ezcodesolution
- **LinkedIn**: [Waqas Mustafa](https://www.linkedin.com/in/waqas-mustafa-ba5701209/)
- **Email**: mustafawaqas0@gmail.com
- **License**: LGPL-3

## 📝 Changelog

### Version 18.0.1.0.0
- Initial release for Odoo 18
- Custom login URL with instant changes
- Website redirect integration
- Settings UI with preview
- 404/redirect blocking modes

---

**🎉 Enjoy your secure, hidden login system!**