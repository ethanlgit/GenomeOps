-- variants per gene
SELECT gene_symbol, COUNT(*) as variant_count
FROM allele
WHERE gene_symbol IS NOT NULL
GROUP BY gene_symbol
ORDER BY variant_count DESC
LIMIT 20;



-- number of alleles per clinical significance category
SELECT clinical_significance, COUNT(*) as variant_count
FROM allele
WHERE clinical_significance IS NOT NULL
GROUP BY clinical_significance
ORDER BY variant_count DESC
LIMIT 20;



-- records per genome assembly
SELECT genome_assembly, COUNT(*) as location_count
FROM allele_location
WHERE genome_assembly IS NOT NULL
GROUP BY genome_assembly
ORDER BY location_count DESC
LIMIT 20;



-- location records per chromosome
SELECT chromosome, COUNT(*) as location_count
FROM allele_location
WHERE chromosome IS NOT NULL
GROUP BY chromosome
ORDER BY location_count DESC
LIMIT 20;



-- location records per gene
SELECT a.gene_symbol, COUNT(*) as location_count
FROM allele as a
JOIN allele_location as l
ON a.allele_id = l.allele_id
WHERE a.gene_symbol IS NOT NULL
GROUP BY a.gene_symbol
ORDER BY location_count DESC
LIMIT 20;



-- alleles with the most locations
SELECT allele_id, COUNT(*) as location_count
FROM allele_location
GROUP BY allele_id
ORDER BY location_count DESC
LIMIT 20;




-- Distribution of the number of location records (1-4) per allele
WITH allele_count as (SELECT allele_id, COUNT(*) as location_count
	FROM allele_location
	GROUP BY allele_id
)

SELECT location_count, COUNT(allele_id)
FROM allele_count
GROUP BY location_count
ORDER BY location_count DESC;



-- records per clinical significance category
SELECT a.clinical_significance, COUNT(*) as location_records
FROM allele as a
JOIN allele_location as l
ON a.allele_id = l.allele_id
WHERE clinical_significance IS NOT NULL
GROUP BY clinical_significance
ORDER BY location_records DESC;
