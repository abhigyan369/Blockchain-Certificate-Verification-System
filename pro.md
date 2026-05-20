# Blockchain Certificate Verification System — Master Development Prompt

You are a senior full-stack + blockchain engineer.

Help me build a complete “Blockchain Certificate Verification System” step-by-step in carefully separated phases.

IMPORTANT RULES:

* Only work on ONE phase at a time.
* Never jump ahead to future phases unless asked.
* Keep architecture clean and modular.
* Explain code in beginner-friendly language.
* Use simple and maintainable code.
* Avoid unnecessary complexity.
* Prefer readability over optimization.
* After every phase, provide:

  * folder structure
  * setup instructions
  * dependencies
  * full code
  * explanation
  * testing steps
* Never rewrite previously completed modules unless necessary.
* Always preserve backward compatibility.
* Use comments in code.
* Follow production-style project organization.

# PROJECT OVERVIEW

Project Name:
Blockchain Certificate Verification System

Goal:
Create a web application where colleges/admins can issue tamper-proof certificates. Certificates are verified using blockchain-based hash storage.

Main Features:

* Admin authentication
* Certificate generation
* PDF certificate creation
* SHA256 hashing
* Blockchain hash storage
* Public certificate verification
* QR code verification
* Tamper detection

# TECH STACK

Frontend:

* HTML
* CSS
* JavaScript
* Bootstrap (optional)

Backend:

* Django (Python)

Database:

* SQLite initially
* Keep architecture scalable for PostgreSQL/MySQL

Blockchain:

* Solidity
* Ganache
* MetaMask

Blockchain Interaction:

* web3.py

PDF Generation:

* reportlab or fpdf

QR Generation:

* qrcode library

# PROJECT STRUCTURE REQUIREMENTS

Use clean modular architecture.

Suggested structure:

project/
│
├── blockchain/
├── certificates/
├── templates/
├── static/
├── media/
├── users/
├── verification/
├── smart_contract/
└── manage.py

# PHASE 1 — PROJECT SETUP

Goal:
Initialize Django project and create clean base architecture.

Tasks:

* Create Django project
* Create apps:

  * users
  * certificates
  * verification
* Configure templates/static/media
* Configure SQLite
* Create base layout
* Create homepage
* Setup Bootstrap styling
* Create reusable navbar/footer

Requirements:

* Clean UI
* Responsive design
* Modular templates

Deliverables:

* Folder structure
* Installation commands
* Full code
* Run instructions

Do NOT implement blockchain yet.

# PHASE 2 — AUTHENTICATION SYSTEM

Goal:
Build admin authentication system.

Tasks:

* Admin login
* Logout
* Session handling
* Protected dashboard
* User roles (admin only for now)

Requirements:

* Use Django authentication
* Secure routes
* Redirect unauthorized users

Deliverables:

* Full code
* URL setup
* Templates
* Authentication flow explanation

Do NOT implement certificates yet.

# PHASE 3 — CERTIFICATE DATABASE SYSTEM

Goal:
Create certificate data management system.

Tasks:

* Certificate model
* Student details storage
* Course details
* Issue date
* Unique certificate ID
* Admin CRUD operations

Requirements:

* Use Django ORM
* Admin dashboard integration
* Validation
* Clean forms

Deliverables:

* Models
* Views
* Forms
* Templates
* Migration commands

Do NOT implement blockchain yet.

# PHASE 4 — PDF CERTIFICATE GENERATION

Goal:
Generate downloadable certificates.

Tasks:

* Generate PDF certificate dynamically
* Include:

  * student name
  * course
  * issue date
  * certificate ID
* Create downloadable certificate

Requirements:

* Professional certificate layout
* Dynamic data rendering
* Store generated PDF

Deliverables:

* PDF generation logic
* Templates
* Download functionality

Do NOT implement blockchain yet.

# PHASE 5 — SHA256 HASHING SYSTEM

Goal:
Create tamper-detection logic.

Tasks:

* Generate SHA256 hash for certificate data/PDF
* Store hash in database
* Recalculate hash during verification

Requirements:

* Use Python hashlib
* Deterministic hashing
* Clean utility functions

Deliverables:

* Hash utility module
* Hash generation logic
* Verification logic

Do NOT implement blockchain yet.

# PHASE 6 — QR CODE VERIFICATION

Goal:
Add QR verification support.

Tasks:

* Generate QR code for each certificate
* QR should contain verification URL
* Embed QR in certificate PDF

Requirements:

* Use qrcode library
* Public verification link

Deliverables:

* QR generation logic
* Updated certificate template
* Verification page

Do NOT implement blockchain yet.

# PHASE 7 — BLOCKCHAIN SETUP

Goal:
Setup local Ethereum environment.

Tasks:

* Install Ganache
* Setup MetaMask
* Connect MetaMask to Ganache
* Explain accounts/private keys
* Setup Remix IDE

Requirements:

* Beginner-friendly explanation
* Local blockchain only

Deliverables:

* Setup steps
* Screenshots guidance
* Testing instructions

No Django integration yet.

# PHASE 8 — SMART CONTRACT DEVELOPMENT

Goal:
Create Solidity smart contract.

Tasks:

* Create CertificateStore contract
* Store certificate hash
* Verify certificate hash
* Retrieve stored data

Requirements:

* Simple Solidity code
* Proper comments
* Beginner-friendly explanation

Deliverables:

* Solidity contract
* Compilation steps
* Deployment steps

# PHASE 9 — DEPLOY CONTRACT TO GANACHE

Goal:
Deploy smart contract locally.

Tasks:

* Compile contract
* Deploy using Remix
* Connect MetaMask
* Use Ganache accounts
* Obtain:

  * contract address
  * ABI

Requirements:

* Explain deployment clearly

Deliverables:

* Deployment walkthrough
* ABI export
* Contract address usage

# PHASE 10 — DJANGO + BLOCKCHAIN INTEGRATION

Goal:
Connect Django backend with blockchain.

Tasks:

* Install web3.py
* Connect Django to Ganache
* Load ABI
* Connect deployed contract
* Store hashes on blockchain
* Verify hashes from blockchain

Requirements:

* Clean service layer
* Reusable blockchain utilities

Deliverables:

* web3 connection code
* Blockchain service module
* Smart contract interaction logic

# PHASE 11 — PUBLIC VERIFICATION SYSTEM

Goal:
Allow anyone to verify certificates.

Tasks:

* Public verification page
* Upload PDF or enter certificate ID
* Regenerate hash
* Compare with blockchain
* Show result:

  * Valid
  * Tampered
  * Not Found

Requirements:

* User-friendly UI
* Clear status messages

Deliverables:

* Verification workflow
* Templates
* Views
* Blockchain verification logic

# PHASE 12 — UI/UX IMPROVEMENTS

Goal:
Make project professional.

Tasks:

* Dashboard styling
* Better certificate design
* Animations
* Verification success/failure UI
* Responsive design improvements

Requirements:

* Modern UI
* Clean layout
* Professional appearance

# PHASE 13 — SECURITY & OPTIMIZATION

Goal:
Improve application quality.

Tasks:

* Secure routes
* Validate uploads
* Prevent duplicate certificates
* Improve error handling
* Environment variables
* Logging

Requirements:

* Production-style practices

# PHASE 14 — DEPLOYMENT

Goal:
Deploy project.

Tasks:

* Deploy Django app
* Configure static/media
* Setup production settings
* Optional:

  * deploy to Render
  * deploy frontend
  * use PostgreSQL

Requirements:

* Step-by-step deployment guide

# PHASE 15 — DOCUMENTATION & REPORT

Goal:
Prepare project submission material.

Tasks:

* README.md
* Architecture diagram
* Workflow explanation
* Tech stack explanation
* Project report
* Viva questions
* Future scope

Requirements:

* Beginner-friendly language
* Professional formatting

# IMPORTANT DEVELOPMENT RULES

* NEVER combine multiple phases.
* Complete current phase fully before continuing.
* Keep code modular.
* Use reusable functions.
* Maintain clean naming conventions.
* Explain every major concept simply.
* Prefer simple implementations first.
* Avoid advanced optimizations unless requested.
* Always include:

  * requirements.txt updates
  * setup instructions
  * testing steps
  * common errors and fixes

Start with PHASE 1 only.
