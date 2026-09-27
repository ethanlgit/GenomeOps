SELECT COUNT(*) AS allele_count
FROM allele;

SELECT COUNT(*) AS location_count
FROM allele_location;



-- No orphaned location records
SELECT COUNT(*) AS orphaned_locations
FROM allele_location AS al
LEFT JOIN allele AS a
ON al.allele_id = a.allele_id
WHERE a.allele_id IS NULL;



-- verify allele_id is unique
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT allele_id) AS unique_allele_ids
FROM allele;



-- Verify the populated natural key is unique
SELECT COUNT(*) AS populated_rows, COUNT(DISTINCT (allele_id, genome_assembly, chromosome_accession)) AS unique_location_keys
FROM allele_location
WHERE genome_assembly IS NOT NULL
AND chromosome_accession IS NOT NULL;



-- verify missing assembly/accession values occur together
SELECT COUNT(*) AS mixed_null_rows
FROM allele_location
WHERE (genome_assembly IS NULL)
<> (chromosome_accession IS NULL);



-- records with missing genomic location information
SELECT COUNT(*) AS missing_location_rows
FROM allele_location
WHERE genome_assembly IS NULL
OR chromosome_accession IS NULL;