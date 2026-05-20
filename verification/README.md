# Public Certificate Verification

The public verification system lets anyone check a certificate without logging in.

## Public URLs

```text
/verify/
/verify/<certificate_id>/
```

Use `/verify/` to enter a certificate ID or upload a certificate PDF.

QR codes in generated certificates still point directly to `/verify/<certificate_id>/`.

## Verification Workflow

1. A user opens `/verify/`.
2. The user enters a certificate ID or uploads a certificate PDF.
3. If a PDF is uploaded, Django reads the PDF text and extracts the certificate ID.
4. Django looks up the certificate in the database.
5. Django regenerates the SHA256 data hash from the stored certificate fields.
6. If blockchain settings are configured, Django compares the regenerated hash with the hash stored in the smart contract.
7. The result page shows one of:

- Valid
- Tampered
- Not Found

## PDF Upload Checks

Uploaded PDFs are checked for these certificate details:

- certificate ID
- student name
- course name
- issue date

If any of those details are missing from the uploaded PDF text, the result is marked as tampered.

## Blockchain Behavior

When `BLOCKCHAIN_CONTRACT_ADDRESS` is configured, verification uses the `CertificateStore` smart contract.

If blockchain access fails, the page shows a warning and falls back to local database hash verification so the public page still returns a useful result.

## Testing

Run the public verification tests:

```text
venv/bin/python manage.py test verification
```

Run the project checks:

```text
venv/bin/python manage.py check
```

## Boundary

Included here:

- Public verification form.
- Certificate ID lookup.
- Certificate PDF upload.
- PDF certificate ID extraction.
- Local hash regeneration.
- Blockchain hash comparison when configured.
- Clear Valid, Tampered, and Not Found results.

Not included here:

- Visual redesign beyond the current Bootstrap layout.
- Production deployment.
- Advanced upload hardening such as file size limits or malware scanning.
