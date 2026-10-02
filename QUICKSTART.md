# ⚡ Démarrage rapide (3 minutes)

## 1️⃣ Vérifier Python

```bash
python3 --version
```

Doit afficher `Python 3.7` ou supérieur.

---

## 2️⃣ Préparer vos comptes

Éditer `list.txt` et ajouter vos comptes (1 par ligne):

```bash
# Exemple:
user@bluewin.ch:mon-password
test@gmail.com:mon-app-password
admin@swisscom.com:secure-pass
```

**⚠️ IMPORTANT:** 
- Tester UNIQUEMENT vos propres comptes
- Avoir l'autorisation explicite
- Ce fichier contient vos mots de passe!

---

## 3️⃣ Lancer le test

```bash
python3 imap_diagnostic.py
```

La sortie ressemble à:
```
[2024-10-02 14:32:15] [INFO] IMAP Diagnostic Tool - Démarrage
[2024-10-02 14:32:15] [INFO] Trouvé 3 compte(s) à tester
[2024-10-02 14:32:16] [INFO] ✓ VALID - user@bluewin.ch - Authentification réussie (0.85s)
[2024-10-02 14:32:17] [INFO] ✗ INVALID - test@gmail.com - Authentification refusée
...
```

---

## 4️⃣ Consulter les résultats

```bash
cat results.txt
```

Affiche:
```
======================================================================
IMAP Diagnostic Tool - Résultats
...
✓ VALID (1 compte(s)):
  user@bluewin.ch
  
✗ INVALID (1 compte(s)):
  test@gmail.com
  
======================================================================
STATISTIQUES
Total: 2 compte(s)
  ✓ Valid: 1
  ✗ Invalid: 1
  ? Error: 0
Durée: 4.23s
```

---

## 5️⃣ Nettoyer

Après utilisation:
```bash
rm list.txt          # Supprimer les credentials
# Conserver results.txt pour l'audit
```

---

## 📊 Que signifient les résultats?

| Status | Signification |
|--------|---------------|
| ✓ VALID | Authentification réussie |
| ✗ INVALID | Mot de passe incorrect ou compte inexistant |
| ? ERROR | Erreur réseau, timeout, ou serveur non configuré |

---

## 🔍 Voir les fournisseurs disponibles

```bash
python3 imap_diagnostic.py --list-providers
```

Affiche la liste de tous les domaines/serveurs supportés.

---

## 💡 Astuces

### Pour tester rapidement un seul compte:

```bash
echo "mon-email@bluewin.ch:mon-password" > list.txt
python3 imap_diagnostic.py
```

### Avec noms de fichiers personnalisés:

```bash
python3 imap_diagnostic.py mes-comptes.txt mes-resultats.txt
```

### Pour plus de détails (debug):

Éditer `config.py`:
```python
LOG_LEVEL = "DEBUG"  # Au lieu de "INFO"
```

---

## ⚠️ Sécurité

- `list.txt` n'est JAMAIS commité sur Git
- Les mots de passe ne sont JAMAIS loggés
- `results.txt` peut être partagé (sans credentials)
- Supprimer `list.txt` après utilisation

---

## 🚨 Erreurs couantes

| Erreur | Solution |
|--------|----------|
| "Email format invalid" | Vérifier le format `email@domaine.com` |
| "Provider not configured" | Domaine non supporté - voir `--list-providers` |
| "Timeout" | Serveur lent - augmenter timeouts dans `config.py` |
| "Authentification refusée" | Vérifier le mot de passe ou MFA |

---

**C'est tout!** Pour la documentation complète, voir [README.md](README.md)
