import json
from pathlib import Path

from django.conf import settings


class BlockchainError(Exception):
    """Base exception for blockchain service failures."""


class BlockchainConfigurationError(BlockchainError):
    """Raised when required blockchain settings are missing."""


class BlockchainConnectionError(BlockchainError):
    """Raised when Ganache cannot be reached."""


class BlockchainTransactionError(BlockchainError):
    """Raised when a blockchain transaction fails."""


def _get_web3_class():
    try:
        from web3 import Web3
    except ImportError as exc:
        raise BlockchainConfigurationError(
            "web3.py is not installed. Run `pip install -r requirements.txt`."
        ) from exc

    return Web3


def blockchain_is_configured():
    return all(
        [
            settings.BLOCKCHAIN_RPC_URL,
            settings.BLOCKCHAIN_CONTRACT_ADDRESS,
            settings.BLOCKCHAIN_ABI_PATH,
        ]
    )


def get_web3():
    Web3 = _get_web3_class()
    web3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))

    if not web3.is_connected():
        raise BlockchainConnectionError(
            f"Could not connect to Ganache at {settings.BLOCKCHAIN_RPC_URL}."
        )

    return web3


def load_contract_abi():
    abi_path = Path(settings.BLOCKCHAIN_ABI_PATH)

    if not abi_path.exists():
        raise BlockchainConfigurationError(
            f"Contract ABI file was not found at {abi_path}."
        )

    with abi_path.open("r", encoding="utf-8") as abi_file:
        return json.load(abi_file)


def get_contract(web3=None):
    if not blockchain_is_configured():
        raise BlockchainConfigurationError(
            "Blockchain settings are incomplete. Set BLOCKCHAIN_CONTRACT_ADDRESS "
            "after deploying the contract to Ganache."
        )

    web3 = web3 or get_web3()
    contract_address = web3.to_checksum_address(settings.BLOCKCHAIN_CONTRACT_ADDRESS)
    contract_abi = load_contract_abi()

    return web3.eth.contract(address=contract_address, abi=contract_abi)


def _get_issuer_address(web3):
    if settings.BLOCKCHAIN_ISSUER_ADDRESS:
        return web3.to_checksum_address(settings.BLOCKCHAIN_ISSUER_ADDRESS)

    if web3.eth.accounts:
        return web3.to_checksum_address(web3.eth.accounts[0])

    raise BlockchainConfigurationError(
        "No issuer account is available. Set BLOCKCHAIN_ISSUER_ADDRESS."
    )


def store_certificate_hash(certificate_id, certificate_hash):
    web3 = get_web3()
    contract = get_contract(web3)
    issuer_address = _get_issuer_address(web3)

    if settings.BLOCKCHAIN_ISSUER_PRIVATE_KEY:
        return _store_with_signed_transaction(
            web3,
            contract,
            issuer_address,
            certificate_id,
            certificate_hash,
        )

    return _store_with_unlocked_account(
        web3,
        contract,
        issuer_address,
        certificate_id,
        certificate_hash,
    )


def _store_with_signed_transaction(
    web3,
    contract,
    issuer_address,
    certificate_id,
    certificate_hash,
):
    nonce = web3.eth.get_transaction_count(issuer_address)
    transaction = contract.functions.storeCertificateHash(
        certificate_id,
        certificate_hash,
    ).build_transaction(
        {
            "from": issuer_address,
            "nonce": nonce,
            "chainId": settings.BLOCKCHAIN_CHAIN_ID,
        }
    )

    signed_transaction = web3.eth.account.sign_transaction(
        transaction,
        private_key=settings.BLOCKCHAIN_ISSUER_PRIVATE_KEY,
    )
    if hasattr(signed_transaction, "raw_transaction"):
        raw_transaction = signed_transaction.raw_transaction
    else:
        raw_transaction = signed_transaction.rawTransaction
    transaction_hash = web3.eth.send_raw_transaction(raw_transaction)
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    if receipt.status != 1:
        raise BlockchainTransactionError("Certificate hash transaction failed.")

    return receipt.transactionHash.hex()


def _store_with_unlocked_account(
    web3,
    contract,
    issuer_address,
    certificate_id,
    certificate_hash,
):
    transaction_hash = contract.functions.storeCertificateHash(
        certificate_id,
        certificate_hash,
    ).transact({"from": issuer_address})
    receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    if receipt.status != 1:
        raise BlockchainTransactionError("Certificate hash transaction failed.")

    return receipt.transactionHash.hex()


def verify_certificate_hash(certificate_id, certificate_hash):
    web3 = get_web3()
    contract = get_contract(web3)

    return contract.functions.verifyCertificateHash(
        certificate_id,
        certificate_hash,
    ).call()


def get_certificate_record(certificate_id):
    web3 = get_web3()
    contract = get_contract(web3)
    certificate_hash, issuer, issued_at, exists = contract.functions.getCertificate(
        certificate_id
    ).call()

    return {
        "certificate_hash": certificate_hash,
        "issuer": issuer,
        "issued_at": issued_at,
        "exists": exists,
    }
