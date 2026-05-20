# Deploy CertificateStore To Ganache

This guide covers the local deployment workflow for `CertificateStore` using Ganache, MetaMask, and Remix.

This step produces two important values:

- Contract address: where the deployed contract lives on Ganache.
- ABI: the JSON interface used later by Django/Web3 to call the contract.

## Before You Start

Make sure Phase 7 setup is complete:

- Ganache is installed and running.
- MetaMask is connected to Ganache.
- A Ganache account is imported into MetaMask.
- Remix can connect to MetaMask.

## Files Used

```text
smart_contract/
├── CertificateStore.sol
├── CertificateStore.abi.json
├── deployment.example.json
└── DEPLOYMENT.md
```

## Step 1 - Start Ganache

1. Open Ganache.
2. Choose your local Ethereum workspace or **Quickstart Ethereum**.
3. Confirm the RPC server and chain ID.

Common local values:

```text
RPC Server: http://127.0.0.1:7545
Chain ID: 1337
```

Use the actual values shown in your Ganache app if they are different.

## Step 2 - Connect MetaMask To Ganache

1. Open MetaMask.
2. Select the Ganache local network.
3. Confirm the network RPC URL and chain ID match Ganache.
4. Select an imported Ganache account.

The selected account should show fake ETH from Ganache.

## Step 3 - Open The Contract In Remix

1. Open `https://remix.ethereum.org/`.
2. Create or open `CertificateStore.sol`.
3. Copy the full contents of `smart_contract/CertificateStore.sol` into Remix.

## Step 4 - Compile The Contract

1. Open the **Solidity Compiler** panel.
2. Select compiler version `0.8.20` or newer.
3. Click **Compile CertificateStore.sol**.
4. Confirm Remix shows no compiler errors.

If Remix shows a compiler warning only, read it carefully. Warnings do not always block deployment, but errors must be fixed before continuing.

## Step 5 - Deploy With MetaMask

1. Open the **Deploy & Run Transactions** panel.
2. Set **Environment** to **Injected Provider - MetaMask**.
3. MetaMask should ask for permission to connect if it is not already connected.
4. Confirm the connection.
5. Confirm Remix shows the Ganache account in the **Account** field.
6. Select `CertificateStore` in the contract dropdown.
7. Click **Deploy**.
8. MetaMask will open a transaction confirmation window.
9. Confirm the transaction.
10. Wait for Remix to show the deployed contract under **Deployed Contracts**.

## Step 6 - Copy The Contract Address

After deployment, Remix shows the deployed contract entry.

1. Expand **Deployed Contracts**.
2. Find the `CertificateStore` instance.
3. Copy the contract address shown by Remix.
4. Keep this address for Phase 10.

The address should look similar to this format:

```text
0x1234567890abcdef1234567890abcdef12345678
```

Do not copy this example address. Use the real address shown in your Remix deployment.

## Step 7 - Record Local Deployment Details

Create a local deployment file from the template:

```text
cp smart_contract/deployment.example.json smart_contract/deployment.local.json
```

Then update `deployment.local.json`:

```json
{
  "networkName": "Ganache Local",
  "rpcUrl": "http://127.0.0.1:7545",
  "chainId": 1337,
  "contractName": "CertificateStore",
  "contractAddress": "PASTE_YOUR_REAL_DEPLOYED_ADDRESS",
  "abiPath": "smart_contract/CertificateStore.abi.json",
  "deployedWith": "Remix IDE + MetaMask",
  "notes": "Local deployment values for this machine."
}
```

`deployment.local.json` should stay local because Ganache deployments are machine-specific and may change when Ganache is reset.

## Step 8 - Confirm The ABI

The ABI is saved in:

```text
smart_contract/CertificateStore.abi.json
```

In Remix, you can also copy the ABI manually:

1. Open the **Solidity Compiler** panel.
2. Compile `CertificateStore.sol`.
3. Click **Compilation Details**.
4. Copy the ABI section.
5. Compare it with `smart_contract/CertificateStore.abi.json`.

## Step 9 - Test The Deployed Contract

Use Remix under **Deployed Contracts**.

### Store A Hash

Call `storeCertificateHash` with:

```text
certificateId: CERT-001
certificateHash: 8a7f2c4b1d9e0f1234567890abcdef1234567890abcdef1234567890abcdef12
```

Confirm the transaction in MetaMask.

### Verify The Same Hash

Call `verifyCertificateHash` with the same values.

Expected result:

```text
true
```

### Verify A Different Hash

Call `verifyCertificateHash` with:

```text
certificateId: CERT-001
certificateHash: different-hash-value
```

Expected result:

```text
false
```

### Retrieve The Record

Call `getCertificate` with:

```text
certificateId: CERT-001
```

Expected result:

- Stored hash.
- Issuer wallet address.
- Issued timestamp.
- `exists` as `true`.

## Screenshot Guidance

Capture these screenshots for documentation:

- Ganache running with accounts visible.
- MetaMask connected to Ganache.
- Remix compiler success screen.
- MetaMask deployment confirmation.
- Remix deployed contract address.
- Successful `verifyCertificateHash` result.

Hide recovery phrases and private keys in every screenshot.

## Common Errors And Fixes

### MetaMask opens on the wrong network

Switch MetaMask to the Ganache local network and redeploy.

### Remix does not show Injected Provider

Unlock MetaMask, refresh Remix, and reconnect the site from MetaMask.

### Deployment transaction fails

Confirm the selected MetaMask account has fake ETH in Ganache.

### Contract address changes

Ganache contract addresses can change after reset. Redeploy and update your local deployment record.

### Duplicate certificate error during testing

The contract blocks duplicate certificate IDs. Use a new ID such as `CERT-002`.

## Phase Boundary

Completed here:

- Ganache deployment walkthrough.
- Contract address recording instructions.
- ABI artifact location.
- Local deployment template.
- Manual testing steps after deployment.

Not included here:

- Django Web3 setup.
- Reading the contract address from Django settings.
- Storing certificate hashes from Django.
- Public blockchain verification in Django.
