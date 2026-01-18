# Password Manager Vault

A secure command-line password manager that stores encrypted passwords in a MySQL database.

## Features

- **Generate**: Create secure random passwords with customizable length
- **Add**: Store passwords securely with site name, URL, username, and email
- **Extract**: Retrieve encrypted passwords from the vault
- **Master Password**: All passwords protected with a master password using SHA-256 hashing
- **Encryption**: AES encryption for stored passwords

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd password_m_vault
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start MySQL service:
```bash
sudo systemctl start mysql
```

## Usage

### Generate a password
```bash
python pass_m.py generate -l 16 --copy
```

### Add a password entry
```bash
python pass_m.py add -s "Gmail" -u "https://gmail.com" -n "user@gmail.com" -e "user@gmail.com"
```

### Extract/Retrieve a password
```bash
python pass_m.py extract -s "Gmail" --copy
```

## Arguments

- `option`: `(a)dd` / `(e)xtract` / `(g)enerate`
- `-s, --name`: Site name
- `-u, --url`: Site URL
- `-n, --login`: Username
- `-e, --email`: Email address
- `-l, --length`: Password length (for generate)
- `-c, --copy`: Copy generated password to clipboard

## Project Structure

```
password_m_vault/
├── pass_m.py              # Main entry point
├── requirements.txt       # Project dependencies
├── utils/
│   ├── add.py            # Add password entry
│   ├── retrieve.py       # Retrieve password
│   ├── generate.py       # Generate password
│   ├── aesutil.py        # AES encryption/decryption
│   └── dbconfig.py       # Database configuration
```

## Security Notes

- Master password is hashed with SHA-256
- All stored passwords are encrypted with AES
- Never commit database credentials
- Use strong master passwords
