CREATE TABLE allele (
    allele_id BIGINT PRIMARY KEY,
    allele_type TEXT,
    allele_name TEXT,
    gene_id BIGINT,
    gene_symbol TEXT,
    hgnc_id TEXT,

    clinical_significance TEXT,
    clin_sig_simple INTEGER,
    last_evaluated TIMESTAMP,

    rs_db_snp BIGINT,
    nsv_esv_dbvar TEXT,

    origin TEXT,
    origin_simple TEXT,

    review_status TEXT,
    number_submitters INTEGER,
    tested_in_gtr BOOLEAN,

    variation_id BIGINT,

    somatic_clinical_impact TEXT,
    somatic_clinical_impact_last_evaluated TIMESTAMP,
    review_status_clinical_impact TEXT,

    oncogenicity TEXT,
    oncogenicity_last_evaluated TIMESTAMP,
    review_status_oncogenicity TEXT
);



CREATE TABLE allele_location (
    location_id BIGSERIAL PRIMARY KEY,

    allele_id BIGINT NOT NULL,
    genome_assembly TEXT,
    chromosome_accession TEXT,
    chromosome TEXT,
    start_position BIGINT,
    stop_position BIGINT,

    reference_allele TEXT,
    alternate_allele TEXT,
    cytogenetic TEXT,

    position_vcf BIGINT,
    reference_allele_vcf TEXT,
    alternate_allele_vcf TEXT,

    FOREIGN KEY (allele_id)
        REFERENCES allele(allele_id)
);
