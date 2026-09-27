import psycopg
import pandas as pd


def load(df: pd.DataFrame, pg_password: str):
    allele_df = df[
        [
            "#AlleleID",
            "Type",
            "Name",
            "GeneID",
            "GeneSymbol",
            "HGNC_ID",
            "ClinicalSignificance",
            "ClinSigSimple",
            "LastEvaluated",
            "RS# (dbSNP)",
            "nsv/esv (dbVar)",
            "Origin",
            "OriginSimple",
            "ReviewStatus",
            "NumberSubmitters",
            "TestedInGTR",
            "VariationID",
            "SomaticClinicalImpact",
            "SomaticClinicalImpactLastEvaluated",
            "ReviewStatusClinicalImpact",
            "Oncogenicity",
            "OncogenicityLastEvaluated",
            "ReviewStatusOncogenicity",
        ]
    ].copy()


    location_df = df[
        [
            "#AlleleID",
            "Assembly",
            "ChromosomeAccession",
            "Chromosome",
            "Start",
            "Stop",
            "ReferenceAllele",
            "AlternateAllele",
            "Cytogenetic",
            "PositionVCF",
            "ReferenceAlleleVCF",
            "AlternateAlleleVCF",
        ]
    ].copy()


    allele_df = allele_df.rename(columns={
        "#AlleleID": "allele_id",
        "Type": "allele_type",
        "Name": "allele_name",
        "GeneID": "gene_id",
        "GeneSymbol": "gene_symbol",
        "HGNC_ID": "hgnc_id",

        "ClinicalSignificance": "clinical_significance",
        "ClinSigSimple": "clin_sig_simple",
        "LastEvaluated": "last_evaluated",

        "RS# (dbSNP)": "rs_db_snp",
        "nsv/esv (dbVar)": "nsv_esv_dbvar",

        "Origin": "origin",
        "OriginSimple": "origin_simple",

        "ReviewStatus": "review_status",
        "NumberSubmitters": "number_submitters",
        "TestedInGTR": "tested_in_gtr",

        "VariationID": "variation_id",

        "SomaticClinicalImpact": "somatic_clinical_impact",
        "SomaticClinicalImpactLastEvaluated": "somatic_clinical_impact_last_evaluated",
        "ReviewStatusClinicalImpact": "review_status_clinical_impact",

        "Oncogenicity": "oncogenicity",
        "OncogenicityLastEvaluated": "oncogenicity_last_evaluated",
        "ReviewStatusOncogenicity": "review_status_oncogenicity"
    })



    location_df = location_df.rename(columns={
        "#AlleleID": "allele_id",
        "Assembly": "genome_assembly",
        "ChromosomeAccession": "chromosome_accession",
        "Chromosome": "chromosome",
        "Start": "start_position",
        "Stop": "stop_position",
        "ReferenceAllele": "reference_allele",
        "AlternateAllele": "alternate_allele",
        "Cytogenetic": "cytogenetic",
        "PositionVCF": "position_vcf",
        "ReferenceAlleleVCF": "reference_allele_vcf",
        "AlternateAlleleVCF": "alternate_allele_vcf"
    })


    allele_df = allele_df.drop_duplicates(subset="allele_id")


    with psycopg.connect(f"host=localhost dbname=clinvar user=postgres password={pg_password} port=5432") as conn:

        # load into allele table
        with conn.cursor() as cur:
            with cur.copy("""
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
                ) FROM STDIN
            """) as copy:
                for row in allele_df.itertuples(index=False, name=None):
                    row = tuple(None if pd.isna(value) else value for value in row)
                    copy.write_row(row)

        conn.commit()



        # load into allele_location table
        with conn.cursor() as cur:
            with cur.copy("""
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
                ) FROM STDIN
            """) as copy:
                for row in location_df.itertuples(index=False, name=None):
                    row = tuple(None if pd.isna(value) else value for value in row)
                    copy.write_row(row)

        conn.commit()