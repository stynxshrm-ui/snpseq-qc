#!/usr/bin/env python3
"""Unit tests for genotype_qc.py"""

import unittest
import pandas as pd
import tempfile
import shutil
import os
from genotype_qc import (
    load_reference_data,
    load_lab_data,
    compare_genotypes,
    calculate_statistics
)


class TestGenotypeQC(unittest.TestCase):
    """Test suite for genotype QC functions"""
    
    def setUp(self):
        """Create temporary test files before each test"""
        self.test_dir = tempfile.mkdtemp()
        
        # Create test reference file
        ref_content = (
            "CEP_C13\trs4030303\tC/C\n"
            "CEP_C13\trs10399749\tA/A\n"
            "CEP_C14\trs48147398\tC/C\n"
        )
        self.ref_file = os.path.join(
            self.test_dir, 
            "HapMap_r23a_CEP_C13_AllSNPs.txt"
        )
        with open(self.ref_file, 'w') as f:
            f.write(ref_content)
        
        # Create test lab file
        lab_content = (
            "individual;marker;allele_result\n"
            "----------;------;-------------\n"
            "CEP_C13;rs4030303;A/A\n"
            "CEP_C13;rs10399749;A/A\n"
            "CEP_C14;rs48147398;C/C\n"
        )
        self.lab_file = os.path.join(self.test_dir, "genotype_inf.txt")
        with open(self.lab_file, 'w') as f:
            f.write(lab_content)
    
    def tearDown(self):
        """Clean up temporary files after each test"""
        shutil.rmtree(self.test_dir)
    
    def test_load_reference_data(self):
        """Test loading reference data"""
        df = load_reference_data(self.test_dir)
        
        self.assertEqual(len(df), 3)
        self.assertListEqual(
            list(df.columns), 
            ['individual', 'marker', 'allele_result']
        )
        # self.assertEqual(df.iloc[0]['marker'], 'rs4030303')
    
    def test_load_lab_data(self):
        """Test loading lab data"""
        df = load_lab_data(self.lab_file)
        
        self.assertEqual(len(df), 3)
        # self.assertEqual(df.iloc[0]['individual'], 'CEP_C13')
        # self.assertEqual(df.iloc[0]['marker'], 'rs4030303')
    
    def test_compare_genotypes(self):
        """Test genotype comparison"""
        ref_df = load_reference_data(self.test_dir)
        lab_df = load_lab_data(self.lab_file)
        result = compare_genotypes(ref_df, lab_df)
        
        # Should have 3 comparisons
        self.assertEqual(len(result), 3)
        self.assertIn('match', result.columns)
        
        # rs4030303: C/C vs A/A = mismatch
        # rs10399749: A/A vs A/A = match
        # rs48147398: C/C vs C/C = match
        self.assertEqual(result['match'].sum(), 2)
    
    def test_calculate_statistics(self):
        """Test statistics calculation"""
        ref_df = load_reference_data(self.test_dir)
        lab_df = load_lab_data(self.lab_file)
        comparison_df = compare_genotypes(ref_df, lab_df)
        stats = calculate_statistics(comparison_df)
        
        # Check mismatch count
        self.assertEqual(stats['mismatch_count'], 1)
        
        # Check unique error markers
        self.assertEqual(len(stats['unique_error_markers']), 1)
        # self.assertIn('rs4030303', stats['unique_error_markers'])
    
    def test_file_not_found(self):
        """Test error handling for missing files"""
        with self.assertRaises(FileNotFoundError):
            load_reference_data("/nonexistent/directory")
        
        with self.assertRaises(FileNotFoundError):
            load_lab_data("/nonexistent/file.txt")
    
    def test_empty_reference_directory(self):
        """Test handling of directory with no matching files"""
        empty_dir = tempfile.mkdtemp()
        try:
            with self.assertRaises(FileNotFoundError):
                load_reference_data(empty_dir)
        finally:
            shutil.rmtree(empty_dir)


if __name__ == '__main__':
    unittest.main()