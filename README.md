# Blockchain Certificate Verification System

A Django web application for issuing, downloading, and publicly verifying digital certificates. The project uses SHA256 hashing and a local Ethereum smart contract to detect tampering.

## What It Does

- Admins can log in and manage certificates.
- Certificates are generated as downloadable PDFs.
- Each certificate gets a deterministic SHA256 data hash.
- QR codes link directly to public certificate verification pages.
- Certificate hashes can be stored on a local Ganache blockchain.
- Public users can verify a certificate by entering a certificate ID or uploading a PDF.
- Verification results are shown as Valid, Tampered, or Not Found.

## Tech Stack

- Python
- Django
- SQLite
- ReportLab for PDF generation
- qrcode for QR code generation
- pypdf for uploaded PDF reading
- Solidity
- Ganache
- MetaMask
- Remix IDE
- web3.py

## Project Structure

```text
bct-project/
├── blockchain/          # Blockchain setup docs and Django Web3 service layer
├── certificates/        # Certificate model, CRUD views, hashing, PDF generation
├── project/             # Django project settings and root URLs
├── smart_contract/      # Solidity contract, ABI, and deployment guide
├── static/              # App styling
├── templates/           # Django HTML templates
├── users/               # Admin login, logout, dashboard
├── verification/        # Public verification views, forms, PDF helpers, tests
├── manage.py
├── pro.md               # Phase-by-phase project plan
└── requirements.txt
```

## Setup

Create and activate a virtual environment, then install dependencies:

```text
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run migrations:

```text
python manage.py migrate
```

Create an admin user:

```text
python manage.py createsuperuser
```

Start the Django server:

```text
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Main URLs

```text
/                         Home
/login/                   Admin login
/dashboard/               Admin dashboard
/certificates/            Certificate management
/certificates/create/     Issue certificate
/verify/                  Public verification form
/verify/<certificate_id>/ QR/public direct verification
```

## Blockchain Setup

This project uses a local Ethereum blockchain for development.

Recommended local flow:

1. Start Ganache.
2. Connect MetaMask to Ganache.
3. Open Remix IDE.
4. Compile `smart_contract/CertificateStore.sol`.
5. Deploy the contract to Ganache through MetaMask.
6. Copy the deployed contract address.
7. Configure Django environment variables.

Relevant docs:

- `blockchain/README.md`
- `smart_contract/README.md`
- `smart_contract/DEPLOYMENT.md`
- `blockchain/DJANGO_INTEGRATION.md`

## Django Blockchain Environment Variables

Set these after deploying the smart contract locally:

```text
export BLOCKCHAIN_RPC_URL="http://127.0.0.1:7545"
export BLOCKCHAIN_CHAIN_ID="1337"
export BLOCKCHAIN_CONTRACT_ADDRESS="PASTE_DEPLOYED_CONTRACT_ADDRESS"
export BLOCKCHAIN_ABI_PATH="smart_contract/CertificateStore.abi.json"
export BLOCKCHAIN_ISSUER_ADDRESS="PASTE_GANACHE_ACCOUNT_ADDRESS"
```

For signed transactions, also set:

```text
export BLOCKCHAIN_ISSUER_PRIVATE_KEY="PASTE_GANACHE_PRIVATE_KEY"
```

Use only Ganache private keys. Never use a real wallet private key.

## Verification Workflow

1. Admin issues a certificate.
2. Django stores certificate data in SQLite.
3. Django generates a certificate hash.
4. Django generates a PDF with a QR verification link.
5. If blockchain is configured, Django stores the hash in the smart contract.
6. Public users verify by certificate ID or PDF upload.
7. Django recalculates the hash and compares it with the blockchain hash when available.

## Testing

Run all tests:

```text
python manage.py test
```

Run system checks:

```text
python manage.py check
```

## Notes

- The blockchain flow is designed for local development with Ganache.
- Contract addresses change when Ganache is reset or redeployed.
- `smart_contract/deployment.local.json` is intentionally ignored by Git.
- SQLite and local media storage are used for development.

## Current Scope

Implemented:

- Project setup
- Admin authentication
- Certificate CRUD
- PDF certificate generation
- SHA256 hashing
- QR code verification links
- Local blockchain setup docs
- Solidity smart contract
- Ganache deployment docs and ABI artifact
- Django Web3 integration
- Public verification by ID or PDF upload
- UI/UX improvements

Upcoming project phases from `pro.md` include security hardening, deployment, and final documentation/report material.
