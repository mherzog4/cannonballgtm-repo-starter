#!/usr/bin/env python3
"""
CRM Data Ingestion Pipeline

PURPOSE:
Import CRM data (accounts, opportunities, contacts) and prepare for analysis.
This is typically the first step in your data pipeline.

USAGE:
  python pipelines/ingest_crm.py \\
    --accounts source/crm/exports/crm_accounts_2026-01-15.csv \\
    --opportunities source/crm/exports/crm_deals_2026-01-15.csv \\
    --contacts source/crm/exports/crm_contacts_2026-01-15.csv \\
    --output source/crm/derived/

THE WORKFLOW:
1. Load raw CRM exports (from Salesforce, HubSpot, etc.)
2. Validate schemas against source/crm/schemas/crm_schema.json
3. Clean data (normalize dates, handle nulls)
4. Create derived datasets (deals_with_arr, accounts_enriched)
5. Save to derived folder as parquet (efficient format)

PRIVACY:
- If data contains PII, run pipelines/redact_emails.py BEFORE committing to git
- See docs/privacy_and_redaction.md for guidelines
"""

import argparse
import pandas as pd
import hashlib
from pathlib import Path
from datetime import datetime


def hash_email(email):
    """Hash email for privacy-safe joins"""
    if pd.isna(email):
        return None
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()


def load_and_validate_accounts(accounts_file):
    """Load accounts CSV and validate"""
    print(f"Loading accounts from {accounts_file}...")
    df = pd.read_csv(accounts_file)

    # Validate required columns
    required_cols = ['account_id', 'account_name']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    print(f"  Loaded {len(df)} accounts")
    return df


def load_and_validate_opportunities(opps_file):
    """Load opportunities CSV and validate"""
    print(f"Loading opportunities from {opps_file}...")
    df = pd.read_csv(opps_file)

    # Validate required columns
    required_cols = ['opportunity_id', 'account_id', 'stage', 'amount']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Parse dates
    if 'close_date' in df.columns:
        df['close_date'] = pd.to_datetime(df['close_date'], errors='coerce')

    print(f"  Loaded {len(df)} opportunities")
    return df


def load_and_validate_contacts(contacts_file):
    """Load contacts CSV and validate"""
    print(f"Loading contacts from {contacts_file}...")
    df = pd.read_csv(contacts_file)

    # Validate required columns
    required_cols = ['contact_id', 'account_id']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # Hash emails for privacy
    if 'email' in df.columns:
        print("  Hashing emails for privacy...")
        df['email_hash'] = df['email'].apply(hash_email)
        # Optionally drop the raw email column
        # df = df.drop(columns=['email'])

    print(f"  Loaded {len(df)} contacts")
    return df


def create_deals_with_arr(opportunities):
    """
    Create derived dataset: deals with ARR calculation

    For subscription businesses, ARR = amount
    Adjust this logic for your business model
    """
    print("Creating deals_with_arr derived dataset...")
    df = opportunities.copy()

    # Calculate ARR (adjust for your business model)
    df['arr'] = df['amount']  # Simple: amount = ARR

    # Add deal outcome flags
    df['is_won'] = df['stage'] == 'Closed Won'
    df['is_lost'] = df['stage'] == 'Closed Lost'
    df['is_closed'] = df['is_won'] | df['is_lost']

    return df


def main():
    parser = argparse.ArgumentParser(description='Ingest CRM data')
    parser.add_argument('--accounts', required=True, help='Accounts CSV file')
    parser.add_argument('--opportunities', required=True, help='Opportunities CSV file')
    parser.add_argument('--contacts', required=True, help='Contacts CSV file')
    parser.add_argument('--output', default='source/crm/derived/', help='Output directory')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and validate
    accounts = load_and_validate_accounts(args.accounts)
    opportunities = load_and_validate_opportunities(args.opportunities)
    contacts = load_and_validate_contacts(args.contacts)

    # Create derived datasets
    deals_with_arr = create_deals_with_arr(opportunities)

    # TODO: Create accounts_enriched by joining with enrichment data
    # For now, just copy accounts
    accounts_enriched = accounts.copy()

    # Save to parquet (efficient format)
    print("\nSaving derived datasets...")

    accounts_file = output_dir / 'accounts.parquet'
    print(f"  {accounts_file}")
    accounts_enriched.to_parquet(accounts_file, index=False)

    deals_file = output_dir / 'deals_with_arr.parquet'
    print(f"  {deals_file}")
    deals_with_arr.to_parquet(deals_file, index=False)

    contacts_file = output_dir / 'contacts.parquet'
    print(f"  {contacts_file}")
    contacts.to_parquet(contacts_file, index=False)

    print("\n✓ CRM ingestion complete!")
    print(f"  Accounts: {len(accounts)}")
    print(f"  Opportunities: {len(opportunities)}")
    print(f"  Contacts: {len(contacts)}")
    print(f"\nNext steps:")
    print(f"  1. Run enrichment: python pipelines/enrich_accounts.py")
    print(f"  2. Run segmentation: python pipelines/segment.py")


if __name__ == '__main__':
    main()

# Example usage:
#
# python pipelines/ingest_crm.py \\
#   --accounts source/crm/exports/crm_accounts_2026-01-15.csv \\
#   --opportunities source/crm/exports/crm_deals_2026-01-15.csv \\
#   --contacts source/crm/exports/crm_contacts_2026-01-15.csv \\
#   --output source/crm/derived/
#
# This creates:
#   source/crm/derived/accounts.parquet
#   source/crm/derived/deals_with_arr.parquet
#   source/crm/derived/contacts.parquet
