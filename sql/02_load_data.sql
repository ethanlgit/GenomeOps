-- Data is loaded using psycopg COPY from the Python ETL script.
-- The COPY statements below document the target table/column mapping.

-- Load allele data
COPY allele (
    allele_id,
    allele_type,
    allele_name,
    gene_id,
    gene_symbol,
    hgnc_id,
    clinical_significance,
    clin_sig_simple,
    last_evaluated,
    rs_db_snp,
    nsv_esv_dbvar,
    origin,
    origin_simple,
    review_status,
    number_submitters,
    tested_in_gtr,
    variation_id,
    somatic_clinical_impact,
    somatic_clinical_impact_last_evaluated,
    review_status_clinical_impact,
    oncogenicity,
    oncogenicity_last_evaluated,
    review_status_oncogenicity
)
FROM STDIN;


-- Load genomic location data
COPY allele_location (
    allele_id,
    genome_assembly,
    chromosome_accession,
    chromosome,
    start_position,
    stop_position,
    reference_allele,
    alternate_allele,
    cytogenetic,
    position_vcf,
    reference_allele_vcf,
    alternate_allele_vcf
)
FROM STDIN;