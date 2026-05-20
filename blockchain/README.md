# Phase 7 - Local Blockchain Setup

This phase sets up a local Ethereum blockchain for development. It does not connect Django to blockchain yet, and it does not add a Solidity smart contract. Those steps belong to later phases.

## Goal

Prepare the tools needed for local blockchain development:

- Ganache for a private local Ethereum network.
- MetaMask for a browser wallet.
- Remix IDE for writing, compiling, and deploying Solidity contracts later.

## Dependencies

No Python package is required for this phase, so `requirements.txt` does not change.

Install these external tools manually:

- Ganache: local Ethereum blockchain.
- MetaMask: browser wallet extension.
- Remix IDE: browser-based Solidity IDE at `https://remix.ethereum.org/`.

## Folder Structure

After this phase, the project has a blockchain documentation folder:

```text
bct-project/
├── blockchain/
│   └── README.md
├── certificates/
├── project/
├── templates/
├── users/
├── verification/
├── manage.py
├── pro.md
└── requirements.txt
```

## Step 1 - Install Ganache

Ganache creates a private blockchain on your computer. It gives you test accounts with fake ETH that can be used safely during development.

1. Download Ganache from the official Truffle/Ganache website.
2. Install and open Ganache.
3. Choose **Quickstart Ethereum**.
4. Keep Ganache running while you work with MetaMask or Remix.

Default Ganache values are usually:

```text
RPC Server: http://127.0.0.1:7545
Chain ID: 1337
Currency Symbol: ETH
```

If your Ganache screen shows a different RPC server or chain ID, use the values shown in your Ganache app.

## Step 2 - Understand Ganache Accounts

Ganache creates local test accounts. Each account has:

- Address: public wallet identifier, safe to share for local testing.
- Private key: secret key that controls the account.
- Balance: fake ETH used for local transactions.

Important:

- Ganache private keys are only for local development.
- Never use a real wallet private key in this project.
- Never commit real private keys to Git.
- If you restart or reset Ganache, account balances and deployed contract addresses may change.

## Step 3 - Install MetaMask

MetaMask lets the browser connect to Ethereum networks.

1. Install the MetaMask browser extension.
2. Create a wallet or use an existing test-only wallet.
3. Store the recovery phrase safely.
4. Do not use a wallet that holds real funds for local development.

## Step 4 - Connect MetaMask To Ganache

1. Open MetaMask.
2. Click the network selector.
3. Choose **Add a custom network**.
4. Enter the Ganache network details:

```text
Network Name: Ganache Local
New RPC URL: http://127.0.0.1:7545
Chain ID: 1337
Currency Symbol: ETH
Block Explorer URL: leave blank
```

5. Save the network.
6. Select **Ganache Local** in MetaMask.

If MetaMask says the chain ID is different, check the chain ID shown in Ganache and use that value.

## Step 5 - Import A Ganache Account Into MetaMask

1. In Ganache, click the key icon beside one account.
2. Copy the private key.
3. In MetaMask, open the account menu.
4. Choose **Import account**.
5. Paste the Ganache private key.
6. Confirm the import.

The imported account should show the same fake ETH balance as Ganache.

## Step 6 - Open Remix IDE

Remix will be used in later phases to create and deploy the Solidity smart contract.

1. Open `https://remix.ethereum.org/`.
2. In the left sidebar, open **Deploy & Run Transactions**.
3. Set **Environment** to **Injected Provider - MetaMask**.
4. MetaMask will ask for permission to connect.
5. Confirm the connection.
6. Remix should show the active Ganache account.

No contract should be created or deployed in Phase 7.

## Screenshot Guidance

Take screenshots for your report or submission after each major setup step:

- Ganache home screen showing the RPC server, chain ID, and accounts.
- MetaMask custom network form with Ganache values.
- MetaMask account screen showing the imported Ganache account balance.
- Remix **Deploy & Run Transactions** panel showing **Injected Provider - MetaMask**.

Avoid showing full private keys or recovery phrases in screenshots.

## Testing Instructions

Use this checklist to confirm Phase 7 is complete:

1. Ganache is running.
2. Ganache shows at least one account with fake ETH.
3. MetaMask has a **Ganache Local** network.
4. MetaMask is connected to the same RPC URL and chain ID shown in Ganache.
5. A Ganache account is imported into MetaMask.
6. The MetaMask balance matches the Ganache account balance.
7. Remix is connected through **Injected Provider - MetaMask**.
8. Remix shows the imported Ganache account.

## Common Errors And Fixes

### MetaMask cannot connect to Ganache

Check that Ganache is open and the RPC URL in MetaMask matches Ganache exactly.

### Chain ID mismatch

Use the chain ID shown in Ganache. Common values are `1337` and `5777`.

### MetaMask balance is zero

Make sure you imported a Ganache account private key, not only added the Ganache network.

### Remix does not show MetaMask

Refresh Remix, unlock MetaMask, select the Ganache network, and reconnect Remix to MetaMask.

### Contract deployment fails in Remix

Do not deploy contracts in Phase 7. Contract creation and deployment are covered in Phase 8 and Phase 9.

## Phase 7 Boundary

Completed in this phase:

- Local blockchain setup instructions.
- MetaMask to Ganache connection instructions.
- Account and private key explanation.
- Remix setup instructions.
- Screenshot and testing guidance.

Not included in this phase:

- Solidity smart contract code.
- Contract deployment.
- Django Web3 integration.
- Blockchain verification logic.
