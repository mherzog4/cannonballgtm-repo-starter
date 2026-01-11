#!/usr/bin/env python3
"""
Campaign Pull Pipeline

PURPOSE:
Pull accounts matching campaign criteria into campaign working folder.
This creates the target list for outreach.

USAGE:
  python pipelines/campaign_pull.py \\
    --campaign campaigns/2026-01-15_midmarket_fintech_post_funding

THE WORKFLOW:
1. Load campaign segment definition (segment.yaml)
2. Filter source data (CRM + enrichment) based on criteria
3. Exclude accounts we shouldn't target (recent outreach, existing customers)
4. Enrich with research data (funding news, job postings)
5. Output to pulled_customers.csv in campaign folder

OUTPUT:
Creates campaigns/[campaign_name]/pulled_customers.csv with:
- account_id, account_name, industry, headcount
- Primary contact info
- Situational change data (funding date, news, etc.)
- Research notes
"""

import argparse
import pandas as pd
import yaml
from pathlib import Path
from datetime import datetime, timedelta


def load_campaign_segment(campaign_path):
    """Load segment definition from campaign folder"""
    segment_file = Path(campaign_path) / 'segment.yaml'
    with open(segment_file) as f:
        return yaml.safe_load(f)


def load_source_data():
    """Load CRM + enrichment data"""
    # Load accounts with segments
    accounts = pd.read_parquet('source/crm/derived/accounts_with_segments.parquet')

    # Load enrichment data
    # (This would typically join latest enrichment data)

    return accounts


def apply_filters(df, segment_config):
    """
    Apply campaign filters from segment.yaml

    Args:
        df: DataFrame of accounts
        segment_config: Campaign segment definition

    Returns:
        Filtered DataFrame
    """
    filters = segment_config['filters']

    # Filter by segment
    if 'base_segment' in segment_config:
        segment_label = segment_config['base_segment']['label']
        # Map from segment key to label if needed
        # df = df[df['segment'] == segment_label]

    # Filter by industry
    if 'industry' in filters:
        df = df[df['industry'].isin(filters['industry'])]

    # Filter by headcount range
    if 'headcount' in filters:
        df = df[
            (df['headcount'] >= filters['headcount']['min']) &
            (df['headcount'] <= filters['headcount']['max'])
        ]

    # Filter by geography
    if 'geography' in filters:
        df = df[df['region'].isin(filters['geography'])]

    # Filter by funding date
    if 'last_funding_date' in filters:
        after_date = pd.to_datetime(filters['last_funding_date']['after'])
        df = df[pd.to_datetime(df['last_funding_date']) >= after_date]

    # TODO: Add more filters as needed

    return df


def apply_exclusions(df, exclusions):
    """
    Apply exclusion rules

    Args:
        df: DataFrame of accounts
        exclusions: Exclusion rules from segment.yaml

    Returns:
        Filtered DataFrame
    """
    # Exclude existing customers
    if exclusions.get('is_customer', False) == False:
        df = df[df.get('is_customer', False) == False]

    # Exclude accounts with open opportunities
    if exclusions.get('has_open_opportunity', False) == False:
        df = df[df.get('has_open_opportunity', False) == False]

    # Exclude recent outreach (within N days)
    if 'recent_outreach_within_days' in exclusions:
        days = exclusions['recent_outreach_within_days']
        cutoff_date = datetime.now() - timedelta(days=days)
        # df = df[df['last_outreach_date'] < cutoff_date]
        # (You'd need to track outreach dates to implement this)

    return df


def enrich_with_research(df):
    """
    Add research data (funding news, job postings, etc.)

    This is where you'd call external APIs:
    - Crunchbase for funding
    - LinkedIn for job postings
    - News APIs for recent mentions

    For now, this is a placeholder.
    """
    # TODO: Implement research enrichment
    df['research_notes'] = 'TODO: Add research from APIs'
    return df


def main():
    parser = argparse.ArgumentParser(description='Pull accounts for campaign')
    parser.add_argument('--campaign', required=True, help='Campaign folder path')
    parser.add_argument('--limit', type=int, help='Max accounts to pull')
    args = parser.parse_args()

    campaign_path = Path(args.campaign)

    # Load campaign segment definition
    print(f"Loading campaign segment from {campaign_path}/segment.yaml...")
    segment_config = load_campaign_segment(campaign_path)

    # Load source data
    print("Loading source data (CRM + enrichment)...")
    df = load_source_data()
    print(f"Loaded {len(df)} accounts")

    # Apply filters
    print("Applying filters...")
    df = apply_filters(df, segment_config)
    print(f"After filters: {len(df)} accounts")

    # Apply exclusions
    print("Applying exclusions...")
    df = apply_exclusions(df, segment_config.get('exclusions', {}))
    print(f"After exclusions: {len(df)} accounts")

    # Enrich with research
    print("Enriching with research data...")
    df = enrich_with_research(df)

    # Limit if specified
    limit = args.limit or segment_config.get('output', {}).get('limit', len(df))
    df = df.head(limit)

    # Select output fields
    output_fields = segment_config.get('output', {}).get('fields', df.columns.tolist())
    df_output = df[output_fields]

    # Save to campaign folder
    output_file = campaign_path / 'pulled_customers.csv'
    print(f"\nSaving {len(df_output)} accounts to {output_file}...")
    df_output.to_csv(output_file, index=False)

    print("\n✓ Campaign pull complete!")
    print(f"  Target list: {len(df_output)} accounts")
    print(f"  Output file: {output_file}")


if __name__ == '__main__':
    main()

# Example usage:
#
# python pipelines/campaign_pull.py \\
#   --campaign campaigns/2026-01-15_midmarket_fintech_post_funding
#
# This will create:
# campaigns/2026-01-15_midmarket_fintech_post_funding/pulled_customers.csv
