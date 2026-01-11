#!/usr/bin/env python3
"""
Segment Classification Pipeline

PURPOSE:
Classify accounts into segments based on rules in analysis/segmentation/segment_rules.yaml

USAGE:
  python pipelines/segment.py \\
    --input source/crm/derived/accounts_enriched.parquet \\
    --output source/crm/derived/accounts_with_segments.parquet

THE WORKFLOW:
1. Load enriched account data
2. Load segment rules from YAML
3. Apply rules to classify each account
4. Save accounts with segment labels

OUTPUT:
Adds 'segment' column to account data with values like:
- "Mid-Market Fintech"
- "SMB SaaS"
- "Enterprise"
- "Unknown" (if no rules match)
"""

import argparse
import pandas as pd
import yaml
from pathlib import Path


def load_segment_rules(rules_path='analysis/segmentation/segment_rules.yaml'):
    """Load segment classification rules from YAML"""
    with open(rules_path) as f:
        return yaml.safe_load(f)


def classify_account(row, config):
    """
    Classify a single account based on segment rules

    Args:
        row: DataFrame row (account data)
        config: Segment rules from YAML

    Returns:
        Segment label (string)
    """
    # Try each segment in priority order
    for segment_key in config['segment_priority']:
        segment = config['segments'][segment_key]
        rules = segment['rules']

        # Check industry
        if 'industry' in rules:
            if row.get('industry') not in rules['industry']:
                continue

        # Check headcount range
        if 'headcount' in rules:
            if not (rules['headcount']['min'] <= row.get('headcount', 0) <= rules['headcount']['max']):
                continue

        # Check revenue range (if present)
        if 'revenue_arr' in rules:
            arr = row.get('arr', 0)
            if not (rules['revenue_arr']['min'] <= arr <= rules['revenue_arr']['max']):
                continue

        # If all rules match, return segment label
        return segment['label']

    # If no specific segment matches, try size buckets
    headcount = row.get('headcount', 0)
    for bucket_key, bucket in config.get('size_buckets', {}).items():
        if bucket['headcount']['min'] <= headcount <= bucket['headcount']['max']:
            return bucket['label']

    return 'Unknown'


def main():
    parser = argparse.ArgumentParser(description='Classify accounts into segments')
    parser.add_argument('--input', required=True, help='Input file (accounts with enrichment)')
    parser.add_argument('--output', required=True, help='Output file (accounts with segments)')
    parser.add_argument('--rules', default='analysis/segmentation/segment_rules.yaml',
                       help='Segment rules file')
    args = parser.parse_args()

    # Load data
    print(f"Loading accounts from {args.input}...")
    df = pd.read_parquet(args.input)
    print(f"Loaded {len(df)} accounts")

    # Load rules
    print(f"Loading segment rules from {args.rules}...")
    config = load_segment_rules(args.rules)

    # Classify accounts
    print("Classifying accounts into segments...")
    df['segment'] = df.apply(lambda row: classify_account(row, config), axis=1)

    # Print summary
    print("\nSegment distribution:")
    print(df['segment'].value_counts())

    # Save output
    print(f"\nSaving to {args.output}...")
    df.to_parquet(args.output, index=False)
    print("Done!")


if __name__ == '__main__':
    main()

# Example usage:
#
# python pipelines/segment.py \\
#   --input source/crm/derived/accounts_enriched.parquet \\
#   --output source/crm/derived/accounts_with_segments.parquet
#
# Then you can query by segment:
#
# import pandas as pd
# df = pd.read_parquet('source/crm/derived/accounts_with_segments.parquet')
# midmarket_fintech = df[df['segment'] == 'Mid-Market Fintech']
# print(f"Found {len(midmarket_fintech)} mid-market fintech accounts")
