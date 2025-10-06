# Genotype Quality Control Analysis

A Python tool for comparing SNP genotyping data between reference datasets (HapMap) and laboratory results to identify discrepancies and generate quality control statistics.

## Overview

This program performs quality control validation by:
- Comparing allele results between reference and lab data for matching individual/marker pairs
- Counting mismatches to assess data quality
- Identifying unique markers with errors

## Features

- Handles multiple reference files automatically
- Supports different file formats (tab-separated for reference, semicolon-separated for lab)
- Provides a basic summary statistics
- Includes comprehensive unit tests
- Automated testing via GitHub Actions

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

## Project Structure

```
snpseq-qc/
├── genotype_qc.py           # Main program
├── requirements.txt         # Python dependencies
├── test_genotype_qc.py      # Unit tests
├── README.md               # This file
└── .github/
    └── workflows/
        └── test.yml        # GitHub Actions configuration
```

## Technical Details

### Dependencies

- `pandas >= 1.5.0` - Data manipulation and analysis

### Python Version

- Tested on Python 3.8, 3.9, 3.10, 3.11

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/genotype-qc.git
cd genotype-qc
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python genotype_qc.py <reference_directory> <lab_file>
```

### Examples

**Compare lab data against reference files:**
```bash
python genotype_qc.py ./data/ ./data/genotype_inf.txt
```

## Data Format

### Reference Data Files

Tab-separated values with three columns (no header):

```
individual    marker       allele_result
CEP_C13       rs4030303    C/C
CEP_C13       rs10399749   A/A
CEP_C13       rs4030300    G/G
```

- **Column 1:** Individual identifier
- **Column 2:** SNP marker (rs number)
- **Column 3:** Allele result (e.g., C/C, A/T, G/G)

### Lab Data File

Semicolon-separated values with header:

```
individual;marker;allele_result
----------;------;-------------
CEP_C13;rs4030303;A/A
CEP_C14;rs48147398;C/C
CEP_C15;rs13328714;C/T
```

- **Line 1:** Header row
- **Line 2:** Separator line (ignored)
- **Line 3+:** Data rows

### Example Output

```
Mismatch count: 42

Unique error markers (15 total):
  rs4030303
  rs10399749
  rs940550
  ...
```

## Testing

### Run Unit Tests

```bash
python -m unittest test_genotype_qc.py -v
```

### Test Coverage

The test suite includes:
- Reference data loading
- Lab data loading
- Genotype comparison logic
- Statistics calculation
- Error handling for missing files

### Continuous Integration

Tests run automatically on every push via GitHub Actions. Check the Actions tab to see test results.

## License

MIT License - feel free to use and modify as needed.



