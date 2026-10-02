"""
Configuration SMTP pour les fournisseurs de messagerie.
"""

PROVIDERS = {
    "bluewin.ch": {"smtp_host": "smtp.bluewin.ch", "smtp_port": 587, "use_tls": True, "description": "Bluewin"},
    "sunrise.ch": {"smtp_host": "smtp.sunrise.ch", "smtp_port": 587, "use_tls": True, "description": "Sunrise"},
    "gmail.com": {"smtp_host": "smtp.gmail.com", "smtp_port": 587, "use_tls": True, "description": "Gmail"},
    "googlemail.com": {"smtp_host": "smtp.gmail.com", "smtp_port": 587, "use_tls": True, "description": "GoogleMail"},
    "outlook.com": {"smtp_host": "smtp.office365.com", "smtp_port": 587, "use_tls": True, "description": "Outlook"},
    "outlook.ch": {"smtp_host": "smtp.office365.com", "smtp_port": 587, "use_tls": True, "description": "Outlook CH"},
    "hotmail.com": {"smtp_host": "smtp.office365.com", "smtp_port": 587, "use_tls": True, "description": "Hotmail"},
    "swisscom.com": {"smtp_host": "mail.swisscom.com", "smtp_port": 587, "use_tls": True, "description": "Swisscom"},
    "cablecom.ch": {"smtp_host": "smtp.bluewin.ch", "smtp_port": 587, "use_tls": True, "description": "Cablecom"},
    "swissonline.ch": {"smtp_host": "mail.swissonline.ch", "smtp_port": 587, "use_tls": True, "description": "SwissOnline"},
    "gmx.ch": {"smtp_host": "smtp.gmx.com", "smtp_port": 587, "use_tls": True, "description": "GMX CH"},
    "gmx.com": {"smtp_host": "smtp.gmx.com", "smtp_port": 587, "use_tls": True, "description": "GMX"},
    "net2000.ch": {"smtp_host": "mail.net2000.ch", "smtp_port": 587, "use_tls": True, "description": "Net2000"},
    "hispeed.ch": {"smtp_host": "mail.hispeed.ch", "smtp_port": 587, "use_tls": True, "description": "Hispeed"},
    "upc.ch": {"smtp_host": "smtp.bluewin.ch", "smtp_port": 587, "use_tls": True, "description": "UPC"},
    "netplus.ch": {"smtp_host": "mail.netplus.ch", "smtp_port": 587, "use_tls": True, "description": "NetPlus"},
    "vtxmail.ch": {"smtp_host": "mail.vtxmail.ch", "smtp_port": 587, "use_tls": True, "description": "VTXmail"},
    "vtx.ch": {"smtp_host": "mail.vtxmail.ch", "smtp_port": 587, "use_tls": True, "description": "VTX"},
    "quickline.ch": {"smtp_host": "mail.quickline.ch", "smtp_port": 587, "use_tls": True, "description": "Quickline"},
    "yahoo.com": {"smtp_host": "smtp.mail.yahoo.com", "smtp_port": 587, "use_tls": True, "description": "Yahoo"},
    "aol.com": {"smtp_host": "smtp.aol.com", "smtp_port": 587, "use_tls": True, "description": "AOL"},
    "fastmail.com": {"smtp_host": "smtp.fastmail.com", "smtp_port": 587, "use_tls": True, "description": "FastMail"},
    "posteo.de": {"smtp_host": "smtp.posteo.de", "smtp_port": 587, "use_tls": True, "description": "Posteo"},
    "mailbox.org": {"smtp_host": "smtp.mailbox.org", "smtp_port": 587, "use_tls": True, "description": "Mailbox.org"},
}

TIMEOUTS = {"connect": 10, "login": 15, "total": 30}
LOG_LEVEL = "INFO"
HIDE_PASSWORDS = True

def get_provider_config(domain):
    domain_lower = domain.lower().strip()
    if domain_lower in PROVIDERS:
        return PROVIDERS[domain_lower]
    if domain_lower.endswith('.ch'):
        return {"smtp_host": f"mail.{domain_lower}", "smtp_port": 587, "use_tls": True, "description": f"Domaine: {domain_lower}"}
    return None

def list_providers():
    print(f"\n{'DOMAINE':<25} {'SERVEUR SMTP':<30} {'PORT':<6}")
    print("=" * 70)
    for domain in sorted(PROVIDERS.keys()):
        config = PROVIDERS[domain]
        print(f"{domain:<25} {config['smtp_host']:<30} {config['smtp_port']:<6}")
    print(f"\nTotal: {len(PROVIDERS)} fournisseurs\n")
