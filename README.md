# IMAP Diagnostic Tool

Outil Python de diagnostic et de test de connectivité IMAP pour des comptes de messagerie autorisés.

**⚠️ AVERTISSEMENT DE SÉCURITÉ**: Cet outil doit être utilisé UNIQUEMENT sur des comptes dont vous possédez les identifiants et pour lesquels vous avez l'autorisation explicite de réaliser les tests. L'utilisation sur des comptes tiers non autorisés est illégale.

---

## Caractéristiques

✅ **Traitement séquentiel** - Pas de threads, traitement un compte après l'autre  
✅ **Configuration centralisée** - Support de 40+ fournisseurs de messagerie  
✅ **Validation des domaines** - Identification automatique du fournisseur  
✅ **Gestion d'erreurs robuste** - Distinction VALID / INVALID / ERROR  
✅ **Masquage des credentials** - Les mots de passe ne sont jamais loggés  
✅ **Timeouts configurables** - Protection contre les connexions gelées  
✅ **Résultats structurés** - Fichier de sortie détaillé  
✅ **Extensible** - Ajout facile de nouveaux fournisseurs  

---

## Installation

### Prérequis

- Python 3.7+
- Pas de dépendances externes (utilise uniquement la stdlib: `imaplib`, `socket`, `ssl`)

### Étapes

1. **Cloner ou télécharger le projet**
```bash
cd /chemin/vers/imap-diagnostic
```

2. **Vérifier l'installation Python**
```bash
python3 --version
# Python 3.7 ou supérieur requis
```

3. **Rendre le script exécutable** (optionnel, sur Linux/Mac)
```bash
chmod +x imap_diagnostic.py
```

4. **Vérifier les fichiers**
```bash
ls -la
# imap_diagnostic.py
# config.py
# list.txt
# README.md
```

---

## Utilisation

### 1. Préparer le fichier de comptes (`list.txt`)

Format: `email:password` (un par ligne)

```txt
# Exemple:
user@bluewin.ch:mon-mot-de-passe
test@gmail.com:mon-app-password
admin@swisscom.com:secure-password
```

**Notes importantes:**
- Les mots de passe peuvent contenir des `:` (ils seront correctement parsés)
- Les lignes vides et commentaires (commençant par `#`) sont ignorées
- Aucun espace supplémentaire ne doit entourer le `:`

### 2. Lancer le diagnostic

```bash
python3 imap_diagnostic.py list.txt results.txt
```

**Résultat attendu:**
```
[2024-10-02 14:32:15] [INFO] IMAP Diagnostic Tool - Démarrage
[2024-10-02 14:32:15] [INFO] Trouvé 3 compte(s) à tester
[2024-10-02 14:32:15] [INFO] [1/3] Test en cours...
[2024-10-02 14:32:15] [INFO] Traitement: user@bluewin.ch
[2024-10-02 14:32:15] [INFO]   Fournisseur: Bluewin (Suisse)
[2024-10-02 14:32:16] [INFO] ✓ VALID - user@bluewin.ch - Authentification réussie (0.85s)
...
```

### 3. Consulter les résultats

Les résultats sont écrits dans `results.txt`:

```
======================================================================
IMAP Diagnostic Tool - Résultats
Généré: 2024-10-02 14:32:18
======================================================================

✓ VALID (1 compte(s)):
----------------------------------------------------------------------
  user@bluewin.ch
    Domaine: bluewin.ch
    Fournisseur: Bluewin (Suisse)

✗ INVALID (1 compte(s)):
----------------------------------------------------------------------
  test@gmail.com
    Raison: Authentication failed

? ERROR (1 compte(s)):
----------------------------------------------------------------------
  admin@swisscom.com
    Raison: Timeout lors de la connexion à mail.swisscom.com:993

======================================================================
STATISTIQUES
======================================================================
Total: 3 compte(s)
  ✓ Valid: 1
  ✗ Invalid: 1
  ? Error: 1

Durée: 4.23s
```

---

## Commandes utiles

### Afficher tous les fournisseurs configurés

```bash
python3 imap_diagnostic.py --list-providers
```

Affiche un tableau de tous les domaines avec leurs serveurs IMAP.

### Afficher l'aide

```bash
python3 imap_diagnostic.py --help
```

### Utiliser des noms de fichiers personnalisés

```bash
python3 imap_diagnostic.py comptes.txt resultats.txt
```

---

## Fournisseurs supportés

### Suisse 🇨🇭

| Domaine | Fournisseur | Serveur | Port | SSL |
|---------|------------|---------|------|-----|
| `bluewin.ch` | Bluewin (UPC/Sunrise) | imap.bluewin.ch | 993 | ✓ |
| `sunrise.ch` | Sunrise Communications | imap.sunrise.ch | 993 | ✓ |
| `cablecom.ch` | Cablecom (Sunrise group) | imap.bluewin.ch | 993 | ✓ |
| `swisscom.com` | Swisscom Mail | mail.swisscom.com | 993 | ✓ |

### Internationaux 🌍

| Domaine | Fournisseur | Serveur | Port | SSL |
|---------|------------|---------|------|-----|
| `gmail.com` | Gmail | imap.gmail.com | 993 | ✓ |
| `outlook.com` | Microsoft Outlook | outlook.office365.com | 993 | ✓ |
| `yahoo.com` | Yahoo Mail | imap.mail.yahoo.com | 993 | ✓ |
| `fastmail.com` | FastMail | imap.fastmail.com | 993 | ✓ |
| `posteo.de` | Posteo | imap.posteo.de | 993 | ✓ |

**+ 30+ autres fournisseurs pré-configurés**

---

## Interprétation des résultats

### ✓ VALID
L'authentification IMAP a réussi. Le compte est accessible et les credentials sont corrects.

### ✗ INVALID
L'authentification IMAP a été refusée. Cela signifie:
- Mot de passe incorrect
- Email inexistant
- Account désactivé ou suspendu

### ? ERROR
Une erreur technique a empêché le test:
- Timeout (serveur non réactif)
- Erreur SSL/TLS
- Serveur non configuré
- Problème réseau

---

## Configuration avancée

### Modifier les timeouts

Éditer `config.py`:
```python
TIMEOUTS = {
    "connect": 10,      # Connexion TCP/SSL (secondes)
    "login": 15,        # Authentification (secondes)
    "total": 30,        # Total par compte (secondes)
}
```

### Ajouter un nouveau fournisseur

Éditer `config.py` et ajouter une entrée:
```python
PROVIDERS = {
    ...
    "votre-domaine.com": {
        "imap_host": "mail.votre-domaine.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Votre fournisseur"
    },
}
```

### Changer le niveau de log

Éditer `config.py`:
```python
LOG_LEVEL = "DEBUG"  # DEBUG, INFO, WARNING, ERROR
```

---

## Sécurité

### Bonnes pratiques

✅ **À faire:**
- Tester uniquement vos propres comptes
- Utiliser des app passwords si disponibles (Gmail, Yahoo, etc.)
- Activer 2FA sur vos comptes
- Supprimer `list.txt` après utilisation
- Vérifier `results.txt` puis le supprimer

❌ **À ne pas faire:**
- Partager `list.txt` ou `results.txt`
- Commiter ces fichiers sur un dépôt public
- Tester des comptes sans autorisation
- Utiliser sur des réseaux non fiables
- Contourner MFA, CAPTCHA ou rate limiting

### Masquage des credentials

Les mots de passe ne sont JAMAIS affichés:
- Logs en temps réel: mots de passe masqués
- Fichier results.txt: pas de credentials stockés
- Exceptions: données sensibles anonymisées

---

## Cas d'utilisation courants

### Test d'un compte Bluewin

```bash
echo "monmail@bluewin.ch:monpassword" > list.txt
python3 imap_diagnostic.py
```

### Test de plusieurs domaines

```bash
cat > list.txt << EOF
user1@bluewin.ch:pass1
user2@gmail.com:pass2
user3@outlook.com:pass3
EOF

python3 imap_diagnostic.py
```

### Intégration dans un script

```bash
#!/bin/bash
python3 imap_diagnostic.py credentials.txt results.txt

if grep -q "VALID" results.txt; then
    echo "Au moins un compte valide trouvé"
    mail -s "IMAP Results" admin@example.com < results.txt
fi
```

---

## Dépannage

### "File not found: list.txt"
**Solution:** Créer le fichier `list.txt` avec les comptes à tester.

### "Email format invalid"
**Cause:** L'adresse email n'est pas valide.
**Solution:** Vérifier le format `email@domaine.com`.

### "Provider not configured for domain: mondomaine.com"
**Cause:** Ce domaine n'est pas dans la liste de configuration.
**Solution:** Ajouter la configuration dans `config.py` ou contacter pour ajout.

### "Timeout lors de la connexion"
**Cause:** Le serveur IMAP est lent ou injoignable.
**Solution:** Vérifier la connexion réseau, augmenter les timeouts dans `config.py`.

### "Erreur SSL"
**Cause:** Certificat SSL invalide ou non reconnu.
**Solution:** Vérifier que use_ssl=True et le port est correct (généralement 993).

### "Authentication failed" mais le password est correct
**Cause:** MFA activé, app password requis, ou compte suspendu.
**Solution:** Vérifier les paramètres de sécurité du compte.

---

## Architecture

```
imap_diagnostic.py
├── IMAPDiagnostic class
│   ├── validate_email()
│   ├── parse_credentials()
│   ├── test_imap_connection()
│   ├── process_account()
│   ├── run()
│   └── write_results()
└── main()

config.py
├── PROVIDERS (dict)
├── TIMEOUTS (dict)
└── get_provider_config()
```

### Flux d'exécution

1. Lire `list.txt`
2. Parser chaque ligne `email:password`
3. Pour chaque account:
   - Valider l'email
   - Lookup du fournisseur par domaine
   - Tester la connexion IMAP
   - Enregistrer le résultat
4. Écrire `results.txt`
5. Afficher le résumé

---

## Limitations connues

- ⚠️ **IMAP uniquement** - Pas de support POP3 ou autres protocoles
- ⚠️ **Authentification basique** - Pas de support OAuth2
- ⚠️ **Séquentiel** - Pas de parallélisation (par design)
- ⚠️ **ProtonMail** - Nécessite ProtonMail Bridge installé
- ⚠️ **Tutanota** - Pas d'accès IMAP standard

---

## Contribution

Pour ajouter des fournisseurs ou améliorer l'outil:

1. Éditer `config.py` avec la nouvelle configuration
2. Tester avec un compte de ce fournisseur
3. Vérifier que les timeouts sont appropriés

---

## Licence

Fourni tel quel. À usage personnel pour des comptes autorisés uniquement.

---

## Support

Pour les problèmes ou questions:
1. Consulter la section [Dépannage](#dépannage)
2. Vérifier les logs avec `LOG_LEVEL = "DEBUG"` dans `config.py`
3. Vérifier que le serveur IMAP est accessible: `nslookup imap.domaine.com`

---

**Dernière mise à jour:** 2024-10-02  
**Version:** 1.0  
**Python:** 3.7+
