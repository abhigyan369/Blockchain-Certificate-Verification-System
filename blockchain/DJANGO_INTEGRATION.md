# Django Blockchain Integration

This guide explains how to connect the Django backend to the locally deployed `CertificateStore` contract on Ganache.

## What This Integration Does

The Django app can now:

- Connect to Ganache using `web3.py`.
- Load the `CertificateStore` ABI.
- Connect to a deployed contract address.
- Store certificate hashes on-chain when certificates are issued.
- Verify certificate hashes against the blockchain during certificate verification.

## Install Dependencies

Install the Python dependencies from the project root:

```text
venv/bin/pip install -r requirements.txt
```

The blockchain integration needs:

```text
web3
```

## Required Local Setup

Before running Django blockchain calls:

1. Start Ganache.
2. Deploy `CertificateStore` from Remix.
3. Copy the deployed contract address.
4. Confirm the ABI exists at `smart_contract/CertificateStore.abi.json`.

## Environment Variables

Set these values before running Django:

```text
export BLOCKCHAIN_RPC_URL="http://127.0.0.1:7545"
export BLOCKCHAIN_CHAIN_ID="1337"
export BLOCKCHAIN_CONTRACT_ADDRESS="PASTE_DEPLOYED_CONTRACT_ADDRESS"
export BLOCKCHAIN_ABI_PATH="smart_contract/CertificateStore.abi.json"
```

For transactions, choose one account option.

Option 1: use an unlocked Ganache account:

```text
export BLOCKCHAIN_ISSUER_ADDRESS="PASTE_GANACHE_ACCOUNT_ADDRESS"
```

Option 2: sign transactions with a private key:

```text
export BLOCKCHAIN_ISSUER_ADDRESS="PASTE_GANACHE_ACCOUNT_ADDRESS"
export BLOCKCHAIN_ISSUER_PRIVATE_KEY="PASTE_GANACHE_PRIVATE_KEY"
```

Use only Ganache private keys. Never use a real wallet private key.

## Run The Server

```text
venv/bin/python manage.py runserver
```

## Test Hash Storage

1. Log in as an admin.
2. Issue a new certificate.
3. If the blockchain settings are correct, Django shows a success message with the transaction hash.
4. Open Remix and call `getCertificate` with the certificate ID.
5. Confirm the stored hash matches the Django certificate hash.

## Test Blockchain Verification

1. Open the public verification URL for a certificate.
2. Django recalculates the certificate hash.
3. Django asks the smart contract whether the recalculated hash matches the on-chain hash.
4. The verification page shows:

- local hash match
- blockchain hash match
- blockchain issuer address
- blockchain timestamp

## Fallback Behavior

If `BLOCKCHAIN_CONTRACT_ADDRESS` is empty, Django continues using local database hash verification and shows a message that blockchain verification is not configured.

If Ganache is not running or the contract cannot be reached, Django shows a warning and falls back to local database hash verification.

## Common Errors And Fixes

### `web3.py is not installed`

Run:

```text
venv/bin/pip install -r requirements.txt
```

### `Could not connect to Ganache`

Start Ganache and confirm `BLOCKCHAIN_RPC_URL` matches the Ganache RPC server.

### `Blockchain settings are incomplete`

Deploy the contract and set `BLOCKCHAIN_CONTRACT_ADDRESS`.

### `Contract ABI file was not found`

Confirm `BLOCKCHAIN_ABI_PATH` points to `smart_contract/CertificateStore.abi.json`.

### `Certificate already exists`

The smart contract blocks duplicate certificate IDs. Issue a new certificate or reset Ganache only in local development.

## Files Involved

```text
blockchain/
├── DJANGO_INTEGRATION.md
├── __init__.py
└── services.py

smart_contract/
├── CertificateStore.abi.json
└── CertificateStore.sol
```

## Phase Boundary

Included here:

- Django Web3 dependency.
- Blockchain settings.
- Reusable blockchain service module.
- Certificate hash storage calls.
- Blockchain hash verification calls.

Not included here:

- Uploading a PDF for public verification.
- Public search form for certificate IDs.
- Production deployment.
