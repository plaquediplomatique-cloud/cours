# Exemples d'utilisation - IMAP Diagnostic Tool

## Exemples pratiques et cas d'usage

---

## 1. Test simple d'un compte Bluewin

```bash
# Préparer
echo "jean.dupont@bluewin.ch:MonPassword123!" > list.txt

# Lancer
python3 imap_diagnostic.py

# Résultat
cat results.txt
```

---

## 2. Test de 5 domaines différents

```bash
cat > list.txt << 'EOF'
user1@bluewin.ch:password1
user2@gmail.com:app-password-xyz
user3@swisscom.com:pass123
user4@outlook.com:outlook-pass
user5@fastmail.com:mail-pass
EOF

python3 imap_diagnostic.py
```

---

## 3. Automatiser avec un cron job (Linux/Mac)

```bash
#!/bin/bash
# test-imap-daily.sh

cd /chemin/vers/imap-diagnostic

# Copier la liste de comptes depuis un endroit sécurisé
cp /secure/location/accounts.txt list.txt

# Lancer le diagnostic
python3 imap_diagnostic.py

# Envoyer les résultats par email
mail -s "IMAP Diagnostic Results" admin@example.com < results.txt

# Nettoyer
rm list.txt

# Garder les résultats (optionnel)
# cp results.txt results-$(date +%Y-%m-%d).txt
```

Ajouter au crontab:
```bash
crontab -e
# Ajouter: 0 2 * * * /chemin/vers/test-imap-daily.sh
```

---

## 4. Script d'intégration Jenkins/CI-CD

```groovy
pipeline {
    agent any
    
    stages {
        stage('IMAP Diagnostic') {
            steps {
                script {
                    // Copier credentials depuis vault/secrets
                    withCredentials([file(credentialsId: 'imap-accounts', variable: 'ACCOUNTS_FILE')]) {
                        sh '''
                            cp $ACCOUNTS_FILE list.txt
                            python3 imap_diagnostic.py
                        '''
                    }
                    
                    // Archiver les résultats
                    archiveArtifacts artifacts: 'results.txt', fingerprint: true
                }
            }
        }
        
        stage('Analyze Results') {
            steps {
                script {
                    def results = readFile('results.txt')
                    
                    if (results.contains('ERROR')) {
                        currentBuild.result = 'UNSTABLE'
                        echo "⚠️ Erreurs détectées dans les résultats IMAP"
                    }
                    
                    if (!results.contains('VALID')) {
                        currentBuild.result = 'FAILURE'
                        echo "🔴 Aucun compte valide trouvé"
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'rm -f list.txt'
        }
    }
}
```

---

## 5. Intégration Python - Utiliser comme module

```python
import sys
sys.path.insert(0, '/chemin/vers/imap-diagnostic')

from imap_diagnostic import IMAPDiagnostic

# Utiliser comme module
tool = IMAPDiagnostic('mes-comptes.txt', 'mes-resultats.txt')
success = tool.run()

if success:
    # Analyser les résultats
    valid_accounts = [r for r in tool.results if r['status'] == 'VALID']
    invalid_accounts = [r for r in tool.results if r['status'] == 'INVALID']
    errors = [r for r in tool.results if r['status'] == 'ERROR']
    
    print(f"Résumé: {len(valid_accounts)} valides, {len(invalid_accounts)} invalides, {len(errors)} erreurs")
    
    for account in valid_accounts:
        print(f"✓ {account['email']} - {account['provider']}")
```

---

## 6. Batch test avec rapport HTML

```python
#!/usr/bin/env python3

import os
import json
from datetime import datetime
from imap_diagnostic import IMAPDiagnostic

def generate_html_report(results):
    """Génère un rapport HTML à partir des résultats."""
    
    valid = [r for r in results if r['status'] == 'VALID']
    invalid = [r for r in results if r['status'] == 'INVALID']
    error = [r for r in results if r['status'] == 'ERROR']
    
    html = f"""
    <html>
    <head>
        <title>IMAP Diagnostic Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .valid {{ background: #d4edda; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .invalid {{ background: #f8d7da; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            .error {{ background: #fff3cd; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>IMAP Diagnostic Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Summary</h2>
        <table>
            <tr>
                <th>Status</th>
                <th>Count</th>
            </tr>
            <tr>
                <td class="valid">✓ Valid</td>
                <td>{len(valid)}</td>
            </tr>
            <tr>
                <td class="invalid">✗ Invalid</td>
                <td>{len(invalid)}</td>
            </tr>
            <tr>
                <td class="error">? Error</td>
                <td>{len(error)}</td>
            </tr>
        </table>
        
        <h2>Valid Accounts</h2>
        {''.join([f"<div class='valid'>{r['email']} - {r.get('provider', 'Unknown')}</div>" for r in valid])}
        
        <h2>Invalid Accounts</h2>
        {''.join([f"<div class='invalid'>{r['email']} - {r.get('reason', 'Unknown')}</div>" for r in invalid])}
        
        <h2>Errors</h2>
        {''.join([f"<div class='error'>{r['email']} - {r.get('reason', 'Unknown')}</div>" for r in error])}
    </body>
    </html>
    """
    
    return html

# Utilisation
if __name__ == "__main__":
    tool = IMAPDiagnostic()
    tool.run()
    
    # Générer le rapport HTML
    html_report = generate_html_report(tool.results)
    with open('report.html', 'w') as f:
        f.write(html_report)
    
    print("Rapport HTML généré: report.html")
```

---

## 7. Vérifier les comptes compromis

```bash
#!/bin/bash
# check-compromised.sh

# Télécharger une liste de comptes depuis un fichier sécurisé
# Vérifier quels comptes sont toujours valides

cp /secure/accounts.txt list.txt

python3 imap_diagnostic.py

# Analyser les résultats
echo "Comptes TOUJOURS valides (à vérifier):"
grep "✓ VALID" results.txt

echo "\nComptes INVALID (peut-être compromise):"
grep "✗ INVALID" results.txt

# Alerter si des comptes sont invalides
if grep -q "✗ INVALID" results.txt; then
    echo "⚠️ ALERTE: Des comptes invalides détectés!" >&2
    exit 1
fi

rm list.txt
```

---

## 8. Test de récupération après changement de password

```bash
#!/bin/bash
# test-password-change.sh

# Avant changement
echo "user@domain.com:old-password" > list.txt
echo "Test AVANT changement:"
python3 imap_diagnostic.py | grep "VALID\|INVALID"

# Changer le password manuellement
echo "Changez le password maintenant (appuyez sur Entrée pour continuer)"
read -p "Fait? "

# Après changement
echo "user@domain.com:new-password" > list.txt
echo "Test APRÈS changement:"
python3 imap_diagnostic.py | grep "VALID\|INVALID"

rm list.txt
```

---

## 9. Tester des domaines personnalisés

```python
# Éditer config.py et ajouter:

PROVIDERS = {
    ...
    "monsociete.com": {
        "imap_host": "mail.monsociete.com",
        "imap_port": 993,
        "use_ssl": True,
        "auth_method": "plain",
        "description": "Ma Société"
    },
    "autre-domaine.ch": {
        "imap_host": "imap.autre-domaine.ch",
        "imap_port": 143,  # Port non-SSL
        "use_ssl": False,
        "auth_method": "plain",
        "description": "Autre domaine"
    },
}

# Puis tester:
# echo "admin@monsociete.com:password" > list.txt
# python3 imap_diagnostic.py
```

---

## 10. Monitoring continu avec alertes

```python
#!/usr/bin/env python3
import time
import json
from datetime import datetime
from imap_diagnostic import IMAPDiagnostic

def monitor_accounts(accounts_file, interval=3600, max_failures=3):
    """
    Monitor des comptes IMAP en continu.
    
    Args:
        accounts_file: Fichier avec les comptes
        interval: Intervalle entre les tests (secondes)
        max_failures: Nombre de failures avant alerte
    """
    
    failures = {}
    
    while True:
        print(f"\n[{datetime.now()}] Running diagnostic...")
        
        tool = IMAPDiagnostic(accounts_file, 'monitor-results.txt')
        tool.run()
        
        # Analyser les résultats
        for result in tool.results:
            email = result['email']
            
            if result['status'] != 'VALID':
                failures[email] = failures.get(email, 0) + 1
                
                if failures[email] >= max_failures:
                    print(f"🚨 ALERTE: {email} a échoué {failures[email]} fois!")
                    # Envoyer notification
                    # send_alert(email, failures[email])
            else:
                # Réinitialiser le compteur si succès
                failures[email] = 0
        
        # Attendre avant le prochain test
        print(f"Prochain test dans {interval} secondes...")
        time.sleep(interval)

if __name__ == "__main__":
    # Tester toutes les heures
    monitor_accounts('comptes.txt', interval=3600)
```

---

## Notes importantes

- ✅ Tous les exemples supposent des comptes **autorisés**
- ✅ Credentials doivent être **sécurisés** (nunse jamais commiter)
- ✅ Results peuvent être **conservés** pour audit/compliance
- ✅ Adapter les **timeouts** si besoin (réseau lent)
- ✅ Utiliser **app passwords** pour Gmail, Yahoo, etc.

---

Pour plus d'infos: voir [README.md](README.md) et [QUICKSTART.md](QUICKSTART.md)
