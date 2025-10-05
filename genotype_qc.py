#!/usr/bin/env python3
"""Genotype Quality Control Program"""

import pandas as pd
import glob
import os
import argparse


def load_reference_data(reference_dir):
    """Load all HapMap reference files."""
    pattern = os.path.join(reference_dir, "HapMap_r23a_CEP_C*_AllSNPs.txt")
    files = glob.glob(pattern)
    
    if not files:
        raise FileNotFoundError(f"No reference files found in {reference_dir}")
    
    dfs = []
    for file_path in files:
        df = pd.read_csv(file_path, sep='\t', header=None,
                        names=['individual', 'marker', 'allele_result'])
        dfs.append(df)
    
    combined = pd.concat(dfs, ignore_index=True)
    
    # Strip whitespace
    for col in combined.columns:
        combined[col] = combined[col].str.strip()
    
    return combined


def load_lab_data(lab_file):
    """Load lab genotype data."""
    if not os.path.exists(lab_file):
        raise FileNotFoundError(f"Lab file not found: {lab_file}")
    
    df = pd.read_csv(lab_file, sep=';', skiprows=2,
                     names=['individual', 'marker', 'allele_result'])
    
    # Strip whitespace
    for col in df.columns:
        df[col] = df[col].str.strip()
    
    return df


def compare_genotypes(reference_df, lab_df):
    """Compare genotypes between reference and lab data."""
    merged = pd.merge(reference_df, lab_df,
                     on=['individual', 'marker'],
                     suffixes=('_ref', '_lab'))
    
    merged['match'] = merged['allele_result_ref'] == merged['allele_result_lab']
    return merged


def calculate_statistics(comparison_df):
    """Calculate QC statistics."""
    mismatches = ~comparison_df['match']
    
    stats = {
        'mismatch_count': mismatches.sum(),
        'unique_error_markers': sorted(
            comparison_df[mismatches]['marker'].unique().tolist()
        )
    }
    return stats


def main():
    parser = argparse.ArgumentParser(description='Genotype QC Analysis')
    parser = argparse.ArgumentParser(description='Genotype QC Analysis')
    parser = argparse.ArgumentParser(description='Genotype QC Analysis')
    parser.add_argument('reference_dir', help='Directory with HapMap files')
    parser.add_argument('lab_file', help='Lab genotype file')
    args = parser.parse_args()
    
    # Load and compare
    ref_df = load_reference_data(args.reference_dir)
    lab_df = load_lab_data(args.lab_file)
    comparison = compare_genotypes(ref_df, lab_df)
    stats = calculate_statistics(comparison)
    
    # Print results
    print(f"Mismatch count: {stats['mismatch_count']}")
    print(f"\nUnique error markers ({len(stats['unique_error_markers'])} total):")
    for marker in stats['unique_error_markers']:
        print(f"{marker}")


if __name__ == "__main__":
    main()
