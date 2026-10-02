"""
Configuration centralisée des fournisseurs de messagerie et leurs serveurs IMAP.
Structure: domaine -> {serveur, port, ssl, authentification}
"""

PROVIDERS = {
    # === FOURNISSEURS SUISSES ===

    # Bluewin (groupe Sunrise/UPC)
    "bluewin.ch": {
        "imap_host": "imap.bluewin.ch",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Bluewin (Suisse)"
    },

    # Sunrise
    "sunrise.ch": {
        "imap_host": "imap.sunrise.ch",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Sunrise Communications (Suisse)"
    },

    # Hotmail/Outlook suisse (.ch)
    "hotmail.com": {
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Microsoft Outlook/Hotmail"
    },

    "outlook.com": {
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Microsoft Outlook"
    },

    "outlook.ch": {
        "imap_host": "outlook.office365.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Microsoft Outlook Suisse"
    },

    # Gmail / Google Workspace
    "gmail.com": {
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Gmail (nécessite app password ou 2FA)"
    },

    "googlemail.com": {
        "imap_host": "imap.gmail.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "GoogleMail"
    },

    # ProtonMail (officiel IMAP via ProtonMail Bridge requis)
    "protonmail.com": {
        "imap_host": "127.0.0.1",
        "imap_port": 1143,
        "use_ssl": False,
        "auth_method": "plain",
        "description": "ProtonMail (nécessite ProtonMail Bridge)"
    },

    "proton.me": {
        "imap_host": "127.0.0.1",
        "imap_port": 1143,
        "use_ssl": False,
        "auth_method": "plain",
        "description": "ProtonMail (nouveau domaine, nécessite Bridge)"
    },

    # === AUTRES FOURNISSEURS SUISSES POPULAIRES ===

    # Swisscom
    "swisscom.com": {
        "imap_host": "mail.swisscom.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Swisscom Mail"
    },

    # Cablecom (groupe UPC/Sunrise)
    "cablecom.ch": {
        "imap_host": "imap.bluewin.ch",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Cablecom (Sunrise group)"
    },

    # === FOURNISSEURS INTERNATIONAUX COURANTS ===

    # Yahoo Mail
    "yahoo.com": {
        "imap_host": "imap.mail.yahoo.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Yahoo Mail (app password recommandé)"
    },

    "yahoo.fr": {
        "imap_host": "imap.mail.yahoo.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Yahoo Mail France"
    },

    "yahoo.de": {
        "imap_host": "imap.mail.yahoo.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Yahoo Mail Germany"
    },

    # AOL
    "aol.com": {
        "imap_host": "imap.aol.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "AOL Mail"
    },

    # Fastmail
    "fastmail.com": {
        "imap_host": "imap.fastmail.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "FastMail"
    },

    # Posteo (allemand, populaire en CH)
    "posteo.de": {
        "imap_host": "imap.posteo.de",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Posteo (Allemagne)"
    },

    # Tutanota (encrypted)
    "tutanota.com": {
        "imap_host": "mail.tutanota.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Tutanota (inaccessible via IMAP standard)"
    },

    # Mailbox.org
    "mailbox.org": {
        "imap_host": "imap.mailbox.org",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Mailbox.org (Allemagne)"
    },

    # === CONFIGURATIONS PERSONNALISÉES/DOMAINES PERSONNELS ===
    # Ajouter ici les domaines personnalisés avec leurs serveurs spécifiques
}


# Timeouts (en secondes)
TIMEOUTS = {
    "connect": 10,      # Connexion TCP/SSL
    "login": 15,        # Authentification
    "total": 30,        # Timeout total par compte
}

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
HIDE_PASSWORDS = True  # Ne jamais afficher les mots de passe dans les logs


def get_provider_config(domain):
    """
    Récupère la configuration IMAP pour un domaine donné.

    Args:
        domain (str): Domaine de l'adresse email (ex: 'bluewin.ch')

    Returns:
        dict: Configuration du fournisseur ou None
    """
    domain_lower = domain.lower().strip()
    return PROVIDERS.get(domain_lower)


def list_providers():
    """Affiche tous les fournisseurs configurés."""
    print(f"\n{'DOMAINE':<25} {'SERVEUR IMAP':<30} {'PORT':<6} {'SSL':<5}")
    print("=" * 70)
    for domain in sorted(PROVIDERS.keys()):
        config = PROVIDERS[domain]
        print(f"{domain:<25} {config['imap_host']:<30} {config['imap_port']:<6} {'Yes' if config['use_ssl'] else 'No':<5}")
    print(f"\nTotal: {len(PROVIDERS)} fournisseurs configurés\n")
