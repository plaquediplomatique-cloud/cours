# Guide d'installation - IMAP Diagnostic Tool

## ⚡ Installation rapide (5 min)

### Étape 1: Vérifier Python

```bash
python3 --version
```

Résultat attendu: `Python 3.7` ou supérieur

Si Python 3 n'est pas installé:
- **Ubuntu/Debian:** `sudo apt-get install python3`
- **macOS:** `brew install python3`
- **Windows:** Télécharger depuis https://www.python.org/downloads/

### Étape 2: Créer un dossier de travail (optionnel)

```bash
mkdir -p ~/imap-diagnostic
cd ~/imap-diagnostic
```

### Étape 3: Télécharger les fichiers

Copier les fichiers du projet:
- `imap_diagnostic.py`
- `config.py`
- `list.txt`
- `README.md`

Vérifier:
```bash
ls -la
```

Doit afficher tous les fichiers mentionnés ci-dessus.

### Étape 4: Vérifier l'installation

```bash
python3 imap_diagnostic.py --help
```

Doit afficher l'aide du programme.

```bash
python3 imap_diagnostic.py --list-providers | head -20
```

Doit afficher la liste des fournisseurs.

### Étape 5: Test de fonctionnement

1. Éditer `list.txt` avec un compte de test:
```bash
nano list.txt
# ou
vi list.txt
```

Ajouter une ligne au format `email:password`

2. Lancer le diagnostic:
```bash
python3 imap_diagnostic.py
```

3. Consulter les résultats:
```bash
cat results.txt
```

✅ **Installation terminée!**

---

## 🔧 Configuration (optionnel)

### Modifier le niveau de debug

Éditer `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Pour plus de détails
LOG_LEVEL = "INFO"   # Pour une sortie standard (défaut)
LOG_LEVEL = "ERROR"  # Minimale
```

### Augmenter les timeouts

Si vous avez des problèmes de connexion, éditer `config.py`:
```python
TIMEOUTS = {
    "connect": 15,      # Augmenté de 10 à 15
    "login": 20,        # Augmenté de 15 à 20
    "total": 45,        # Augmenté de 30 à 45
}
```

### Ajouter un fournisseur personnalisé

Éditer `config.py` et ajouter dans `PROVIDERS`:
```python
"monsociete.com": {
    "imap_host": "mail.monsociete.com",
    "imap_port": 993,
    "use_ssl": True,
    "auth_method": "plain",
    "description": "Ma société"
},
```

---

## 📋 Structure des fichiers

```
.
├── imap_diagnostic.py    # Script principal
├── config.py             # Configuration des fournisseurs
├── list.txt             # Entrée (email:password)
├── results.txt          # Sortie (résultats)
├── README.md            # Documentation complète
└── INSTALLATION.md      # Ce fichier
```

---

## ✅ Checklist avant utilisation

- [ ] Python 3.7+ installé
- [ ] Tous les fichiers téléchargés
- [ ] `--help` fonctionne
- [ ] `--list-providers` fonctionne
- [ ] `list.txt` édité avec vos comptes
- [ ] Comptes testés sont autorisés
- [ ] Connexion réseau active

---

## 🚀 Utilisation courante

```bash
# Test simple
python3 imap_diagnostic.py

# Avec fichiers personnalisés
python3 imap_diagnostic.py mes-comptes.txt mes-resultats.txt

# Voir les fournisseurs disponibles
python3 imap_diagnostic.py -l

# Voir l'aide
python3 imap_diagnostic.py -h
```

---

## ⚠️ Notes de sécurité IMPORTANTES

1. **list.txt** contient vos mots de passe en clair
   - Ne jamais le partager
   - Ne jamais le commiter sur GitHub
   - Supprimer après utilisation

2. **results.txt** contient les résultats
   - Peut être partagé (sans credentials)
   - Conservez pour l'audit si besoin

3. **Authorisation**
   - Tester UNIQUEMENT vos propres comptes
   - Avoir l'permission explicite des propriétaires de compte

4. **Meilleure pratique**
   ```bash
   # Après utilisation
   rm list.txt      # Supprimer les credentials
   # Garder results.txt pour l'audit
   ```

---

## 🐛 Dépannage

### "command not found: python3"
```bash
# Vérifier l'installation
which python3
# Ou utiliser:
python imap_diagnostic.py
```

### "Module not found"
Normalement, aucun module externe n'est nécessaire. Si erreur:
```bash
# Réinstaller Python ou vérifier l'installation
python3 -m pip --version
```

### "list.txt: No such file or directory"
```bash
# Créer le fichier
touch list.txt
# Et l'éditer avec vos comptes
nano list.txt
```

### Les tests prennent trop de temps
```python
# Réduire les timeouts dans config.py
TIMEOUTS = {
    "connect": 5,
    "login": 10,
    "total": 15,
}
```

---

## 📞 Support

1. Consulter [README.md](README.md) section "Dépannage"
2. Vérifier `config.py` pour la configuration
3. Activer DEBUG: `LOG_LEVEL = "DEBUG"` dans `config.py`

---

**Prêt à utiliser!** Lancez:
```bash
python3 imap_diagnostic.py --help
```
