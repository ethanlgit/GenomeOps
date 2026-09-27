### GenomeOps

A data engineering pipeline for transforming, modeling, validating, and analyzing ClinVar genomic variant data using Python, pandas, PostgreSQL, and SQL.

## Overview

ClinVar is a public archive that aggregates information about the relationship between human genetic variants and their clinical significance.

This project takes the raw ClinVar variant_summary.txt dataset and transforms it into a normalized PostgreSQL data model for downstream analysis.

## Pipeline
```
ClinVar variant_summary.txt
            │
            ▼
     Python / pandas
            │
    Transform + validate
            │
            ▼
        PostgreSQL
            │
       ┌────┴────┐
       ▼         ▼
    ALLELE   ALLELE_LOCATION
       │         │
       └────┬────┘
            ▼
     SQL validation
       + analysis
```
##Dataset

The project uses ClinVar's variant_summary.txt dataset, containing approximately 9 million records across 43 source columns.

The raw dataset contains information about:

- Alleles and variant identifiers
- Genes
- Clinical significance
- Genomic coordinates
- Genome assemblies
- Reference and alternate alleles
- Clinical and oncogenicity classifications
- Review status
- Submitter information

The raw dataset is not included in this repository because of its size.

## Data Transformation

The Python transformation step prepares the raw dataset for relational storage by:

- Converting source-specific sentinel values such as -1, -, and na to missing values where appropriate
- Parsing date fields
- Standardizing numeric columns
- Converting TestedInGTR from Y/N to Boolean values
- Preserving biologically meaningful values such as - in allele sequence fields
- Separating allele-level attributes from genomic location attributes

The raw source file is left unchanged.

## Database Design

The raw ClinVar dataset is denormalized, with allele-level information repeated across multiple genomic location records.

The project separates these attributes into two related tables:
```
┌─────────────────────────┐
│         ALLELE          │
├─────────────────────────┤
│ PK  allele_id           │
│     allele_type         │
│     allele_name         │
│     gene_id             │
│     gene_symbol         │
│     ...                 │
└────────────┬────────────┘
             │
             │ 1-to-many
             │
             ▼
┌─────────────────────────┐
│    ALLELE_LOCATION      │
├─────────────────────────┤
│ PK  location_id         │
│ FK  allele_id           │
│     genome_assembly     │
│     chromosome_accession│
│     chromosome          │
│     start_position      │
│     stop_position       │
│     ...                 │
└─────────────────────────┘
```
# `allele`

Contains attributes that functionally describe an allele, including:

- Clinical significance
- Gene information
- Origin
- Review status
- Submitter count
- Oncogenicity
- Somatic clinical impact
- ClinVar identifiers

The table contains approximately 4.5 million unique alleles.

# `allele_location`

Contains genomic location information that can vary for an allele across genome assemblies and reference sequences, including:

- Genome assembly
- Chromosome accession
- Chromosome
- Start and stop coordinates
- Reference and alternate alleles
- VCF representation
- Cytogenetic location

The table contains approximately 9 million location records.

`location_id` is a surrogate primary key. `allele_id` is a foreign key referencing `allele(allele_id)`.

During schema design, combinations of allele identifiers, genome assemblies, and chromosome accessions were investigated as potential natural keys. The final schema uses a surrogate key for `allele_location` while retaining `allele_id` as the relationship to the parent allele.

## Data Validation

SQL validation queries are used to verify the integrity of the transformed data and database relationships.

Validation checks include:

- Row counts between source and target tables
- Allele uniqueness
- Foreign-key and orphaned-record checks
- Uniqueness of populated genomic location combinations
- Missing location information
- Consistency of nullable location fields
- Duplicate records

The source dataset contained no exact duplicate rows, and the loaded location records contained no orphaned allele_id values.

## Analysis

The project includes analytical SQL queries using:

- JOIN
- GROUP BY
- Aggregations
- Common Table Expressions (CTEs)

Example analyses include:

- Variants per gene
- Distribution of clinical significance classifications
- Records by genome assembly
- Records by chromosome
- Genomic locations by gene
- Alleles with multiple genomic locations
- Distribution of locations per allele
- ClinVar Terminology
- Term Meaning
- SCV	Single ClinVar submission from a laboratory, hospital, research group, or other submitter
- GTR	Genetic Testing Registry, a catalog of genetic tests
- VCF	Variant Call Format, a standard format for representing genomic variants
- nsv/esv	dbVar identifiers for structural variants
- RS#	dbSNP identifier, commonly represented as an rs... identifier

## Project Structure
GenomeOps/
├── data/
│   ├── raw/                  # Local ClinVar source data
│   └── processed/            # Generated data
├── notebooks/
│   └── exploration.ipynb     # Dataset exploration and schema investigation
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_load_data.sql
│   ├── 03_validation.sql
│   └── 04_analysis.sql
├── src/
│   ├── transform.py          # Data transformation
│   ├── load.py               # PostgreSQL loading
│   └── etl.py                # Pipeline entry point
├── .gitignore
├── README.md
└── requirements.txt

# Tech Stack
- Python
- pandas
- PostgreSQL
- SQL
- psycopg
- SQLAlchemy
- Jupyter
- Future Work

# Planned extensions to the pipeline include:

Loading raw data into Amazon S3
Orchestrating the pipeline with Apache Airflow
Extending the warehouse to Snowflake
Adding analytical transformations with dbt
Building a Tableau dashboard for downstream analysis