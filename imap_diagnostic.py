#!/usr/bin/env python3
"""
IMAP Diagnostic Tool - Test de connectivité et authentification IMAP
Traitement séquentiel (pas de threads)
Autorisation requise pour les comptes testés
"""

import sys
import re
import time
import imaplib
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Dict

from config import get_provider_config, TIMEOUTS, LOG_LEVEL, HIDE_PASSWORDS


class IMAPDiagnostic:
    """Outil de diagnostic IMAP."""

    def __init__(self, input_file: str = "list.txt", output_file: str = "results.txt"):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.results = []
        self.start_time = datetime.now()

    def log(self, level: str, message: str, hide_sensitive: bool = False):
        """Affiche un message de log avec timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Masquer les données sensibles si demandé
        if hide_sensitive and HIDE_PASSWORDS:
            message = self._mask_sensitive_data(message)

        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        if log_levels.index(level) >= log_levels.index(LOG_LEVEL):
            print(f"[{timestamp}] [{level}] {message}")

    @staticmethod
    def _mask_sensitive_data(text: str) -> str:
        """Masque les mots de passe et données sensibles."""
        # Masquer les mots de passe après ':'
        text = re.sub(r'(:[\w\.\-\+]+@)', ':***@', text)
        # Masquer les credentials complets
        text = re.sub(r'[\w\.\-\+]+@[\w\.\-]+:[\w\.\-\+\!\@\#\$\%\&]+', '***:***', text)
        return text

    @staticmethod
    def _generate_password_variants(password: str) -> list:
        """
        Génère les variantes de cas d'un mot de passe.
        Exemples: "Exemple1" → ["Exemple1", "exemple1", "EXEMPLE1"]
        """
        variants = [password]

        # Ajouter la variante en minuscules
        if password.lower() not in variants:
            variants.append(password.lower())

        # Ajouter la variante en majuscules
        if password.upper() not in variants:
            variants.append(password.upper())

        # Ajouter capitalize (première lettre majuscule, reste minuscule)
        if password.capitalize() not in variants:
            variants.append(password.capitalize())

        return variants

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Valide une adresse email et retourne (valide, domaine).
        Pattern simple mais suffisant pour la plupart des cas.
        """
        pattern = r'^[a-zA-Z0-9._\-+]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(pattern, email):
            return False, None

        domain = email.split('@')[1].lower().strip()
        return True, domain

    def test_imap_connection(self, email: str, password: str,
                            host: str, port: int, use_ssl: bool) -> str:
        """
        Teste la connexion IMAP et l'authentification.
        Retourne: 'VALID', 'INVALID', ou 'ERROR'
        """
        start = time.time()

        try:
            # Déterminer le type de connexion
            if use_ssl:
                imap = imaplib.IMAP4_SSL(
                    host,
                    port,
                    timeout=TIMEOUTS["connect"]
                )
            else:
                imap = imaplib.IMAP4(
                    host,
                    port,
                    timeout=TIMEOUTS["connect"]
                )

            self.log("DEBUG", f"Connexion établie à {host}:{port}")

            try:
                # Essayer les variantes du mot de passe
                password_variants = self._generate_password_variants(password)
                auth_success = False
                last_error = None

                for variant_idx, pwd_variant in enumerate(password_variants, 1):
                    try:
                        self.log("DEBUG", f"  Tentative {variant_idx}/{len(password_variants)}")
                        imap.login(email, pwd_variant)
                        auth_success = True
                        break
                    except imaplib.IMAP4.error as e:
                        last_error = str(e)
                        is_auth_error = ("authentication failed" in last_error.lower() or \
                                        "login failed" in last_error.lower() or \
                                        "invalid credentials" in last_error.lower() or \
                                        "[authenticationfailed]" in last_error.lower())

                        if is_auth_error:
                            self.log("DEBUG", f"  Variante {variant_idx} échouée")
                            continue
                        else:
                            self.log("ERROR",
                                f"? ERROR - {email} - Erreur IMAP: {self._mask_sensitive_data(last_error)}")
                            return "ERROR"

                if auth_success:
                    elapsed = time.time() - start
                    self.log("INFO",
                        f"✓ VALID - {email} - Authentification réussie ({elapsed:.2f}s)")

                    # Fermeture propre
                    try:
                        imap.close()
                    except:
                        pass
                    try:
                        imap.logout()
                    except:
                        pass

                    return "VALID"
                else:
                    self.log("WARNING",
                        f"✗ INVALID - {email} - Authentification refusée (toutes variantes)")
                    return "INVALID"

            except imaplib.IMAP4.error as e:
                error_msg = str(e)
                self.log("ERROR",
                    f"? ERROR - {email} - Erreur IMAP: {self._mask_sensitive_data(error_msg)}")
                return "ERROR"

            finally:
                try:
                    imap.close()
                except:
                    pass
                try:
                    imap.logout()
                except:
                    pass

        except imaplib.IMAP4.error as e:
            self.log("ERROR",
                f"? ERROR - {email} - Erreur de connexion IMAP: {str(e)}")
            return "ERROR"

        except ConnectionRefusedError:
            self.log("ERROR",
                f"? ERROR - {email} - Connexion refusée ({host}:{port})")
            return "ERROR"

        except ConnectionAbortedError:
            self.log("ERROR",
                f"? ERROR - {email} - Connexion interrompue ({host}:{port})")
            return "ERROR"

        except TimeoutError:
            self.log("ERROR",
                f"? ERROR - {email} - Timeout lors de la connexion à {host}:{port}")
            return "ERROR"

        except socket.timeout:
            self.log("ERROR",
                f"? ERROR - {email} - Timeout socket")
            return "ERROR"

        except ssl.SSLError as e:
            self.log("ERROR",
                f"? ERROR - {email} - Erreur SSL: {str(e)}")
            return "ERROR"

        except Exception as e:
            elapsed = time.time() - start
            self.log("ERROR",
                f"? ERROR - {email} - Exception non gérée: {type(e).__name__}: {str(e)}")
            return "ERROR"

    def parse_credentials(self, line: str) -> Optional[Tuple[str, str]]:
        """
        Parse une ligne 'email:password'.
        Retourne (email, password) ou None si format invalide.
        """
        line = line.strip()

        # Ignorer les lignes vides et commentaires
        if not line or line.startswith('#'):
            return None

        # Chercher la dernière occurrence de ':' (le password peut contenir des ':')
        if ':' not in line:
            self.log("WARNING", f"Format invalide (pas de ':'): {line}")
            return None

        parts = line.rsplit(':', 1)  # Split from the right, max 1 split
        if len(parts) != 2:
            self.log("WARNING", f"Format invalide: {line}")
            return None

        email, password = parts
        email = email.strip()
        password = password.strip()

        if not email or not password:
            self.log("WARNING", f"Email ou mot de passe vide dans: {line}")
            return None

        return email, password

    def process_account(self, email: str, password: str) -> Dict[str, str]:
        """Traite un compte: validation -> lookup fournisseur -> test IMAP."""

        # Validation email
        is_valid, domain = self.validate_email(email)
        if not is_valid:
            self.log("WARNING", f"Email invalide: {email}")
            return {
                "email": email,
                "status": "ERROR",
                "reason": "Email format invalid"
            }

        self.log("INFO", f"\nTraitement: {email}")

        # Lookup du fournisseur
        provider_config = get_provider_config(domain)

        if not provider_config:
            self.log("WARNING",
                f"Fournisseur non configuré pour le domaine: {domain}")
            return {
                "email": email,
                "domain": domain,
                "status": "ERROR",
                "reason": "Provider not configured"
            }

        self.log("INFO",
            f"  Fournisseur: {provider_config['description']}")
        self.log("DEBUG",
            f"  Serveur: {provider_config['imap_host']}:{provider_config['imap_port']} "
            f"(SSL: {provider_config['use_ssl']})")

        # Test IMAP
        result = self.test_imap_connection(
            email,
            password,
            provider_config['imap_host'],
            provider_config['imap_port'],
            provider_config['use_ssl']
        )

        return {
            "email": email,
            "domain": domain,
            "provider": provider_config['description'],
            "status": result,
            "host": provider_config['imap_host'],
            "port": provider_config['imap_port']
        }

    def run(self):
        """Exécute le diagnostic complet."""

        self.log("INFO", "=" * 70)
        self.log("INFO", "IMAP Diagnostic Tool - Démarrage")
        self.log("INFO", "=" * 70)

        # Vérifier le fichier d'entrée
        if not self.input_file.exists():
            self.log("ERROR", f"Fichier d'entrée introuvable: {self.input_file}")
            return False

        # Lire les credentials
        credentials = []
        with open(self.input_file, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                parsed = self.parse_credentials(line)
                if parsed:
                    credentials.append(parsed)

        if not credentials:
            self.log("WARNING", "Aucun credential valide trouvé")
            return False

        self.log("INFO", f"Trouvé {len(credentials)} compte(s) à tester")

        # Traiter chaque compte séquentiellement
        for idx, (email, password) in enumerate(credentials, 1):
            self.log("INFO", f"\n[{idx}/{len(credentials)}] Test en cours...")
            result = self.process_account(email, password)
            self.results.append(result)

            # Petit délai pour éviter les rate limits (optionnel)
            if idx < len(credentials):
                time.sleep(0.5)

        # Écrire les résultats
        self.write_results()

        # Résumé
        self.print_summary()

        return True

    def write_results(self):
        """Écrit les résultats dans le fichier de sortie."""

        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("IMAP Diagnostic Tool - Résultats\n")
            f.write(f"Généré: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            # Tri par statut (VALID d'abord)
            valid = [r for r in self.results if r['status'] == 'VALID']
            invalid = [r for r in self.results if r['status'] == 'INVALID']
            error = [r for r in self.results if r['status'] == 'ERROR']

            # VALID
            if valid:
                f.write(f"\n✓ VALID ({len(valid)} compte(s)):\n")
                f.write("-" * 70 + "\n")
                for result in valid:
                    f.write(f"  {result['email']}\n")
                    f.write(f"    Domaine: {result.get('domain', 'N/A')}\n")
                    f.write(f"    Fournisseur: {result.get('provider', 'N/A')}\n\n")

            # INVALID
            if invalid:
                f.write(f"\n✗ INVALID ({len(invalid)} compte(s)):\n")
                f.write("-" * 70 + "\n")
                for result in invalid:
                    f.write(f"  {result['email']}\n")
                    f.write(f"    Raison: {result.get('reason', 'Authentication failed')}\n\n")

            # ERROR
            if error:
                f.write(f"\n? ERROR ({len(error)} compte(s)):\n")
                f.write("-" * 70 + "\n")
                for result in error:
                    f.write(f"  {result['email']}\n")
                    f.write(f"    Raison: {result.get('reason', 'Unknown error')}\n")
                    f.write(f"    Serveur: {result.get('host', 'N/A')}:{result.get('port', 'N/A')}\n\n")

            # Statistiques
            f.write("\n" + "=" * 70 + "\n")
            f.write("STATISTIQUES\n")
            f.write("=" * 70 + "\n")
            f.write(f"Total: {len(self.results)} compte(s)\n")
            f.write(f"  ✓ Valid: {len(valid)}\n")
            f.write(f"  ✗ Invalid: {len(invalid)}\n")
            f.write(f"  ? Error: {len(error)}\n")

            elapsed = datetime.now() - self.start_time
            f.write(f"\nDurée: {elapsed.total_seconds():.2f}s\n")

        self.log("INFO", f"Résultats écrits dans: {self.output_file}")

    def print_summary(self):
        """Affiche un résumé des résultats."""
        valid = len([r for r in self.results if r['status'] == 'VALID'])
        invalid = len([r for r in self.results if r['status'] == 'INVALID'])
        error = len([r for r in self.results if r['status'] == 'ERROR'])

        elapsed = datetime.now() - self.start_time

        print("\n" + "=" * 70)
        print("RÉSUMÉ")
        print("=" * 70)
        print(f"Total: {len(self.results)} compte(s)")
        print(f"  ✓ Valid:  {valid}")
        print(f"  ✗ Invalid: {invalid}")
        print(f"  ? Error:   {error}")
        print(f"\nDurée totale: {elapsed.total_seconds():.2f}s")
        print("=" * 70)


# Import socket et ssl après la classe pour la gestion des exceptions
import socket
import ssl


def main():
    """Fonction principale."""

    # Parser les arguments
    input_file = sys.argv[1] if len(sys.argv) > 1 else "list.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "results.txt"

    # Afficher les options disponibles
    if "--list-providers" in sys.argv or "-l" in sys.argv:
        from config import list_providers
        list_providers()
        return

    if "--help" in sys.argv or "-h" in sys.argv:
        print("""
IMAP Diagnostic Tool - Utilisation

Syntaxe:
    python imap_diagnostic.py [fichier_entrée] [fichier_sortie]

Options:
    -l, --list-providers    Affiche tous les fournisseurs configurés
    -h, --help             Affiche cette aide

Fichiers:
    Entrée:  Format 'email:password' (défaut: list.txt)
    Sortie:  Résultats du diagnostic (défaut: results.txt)

Exemple:
    python imap_diagnostic.py comptes.txt resultats.txt

Notes:
    - Les comptes doivent être autorisés pour être testés
    - Les mots de passe ne sont pas stockés
    - Le traitement est séquentiel (pas de parallélisation)
    - Les logs détaillés sont affichés en temps réel
        """)
        return

    # Exécuter le diagnostic
    tool = IMAPDiagnostic(input_file, output_file)
    success = tool.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
