import pandas as pd



def transform(file_path: str):
    df = pd.read_csv(file_path, sep="\t")

    df.loc[df["Oncogenicity"] == "-", "Oncogenicity"] = pd.NA


    df.loc[df["ReviewStatusOncogenicity"] == "-", "ReviewStatusOncogenicity"] = pd.NA
    df.loc[df["SomaticClinicalImpact"] == "-", "SomaticClinicalImpact"] = pd.NA


    df.loc[df["SCVsForAggregateOncogenicityClassification"] == "-", "SCVsForAggregateOncogenicityClassification"] = pd.NA

    df.loc[df["SCVsForAggregateSomaticClinicalImpact"] == "-", "SCVsForAggregateSomaticClinicalImpact"] = pd.NA

    df.loc[df["SCVsForAggregateGermlineClassification"] == "-", "SCVsForAggregateGermlineClassification"] = pd.NA


    df.loc[df["ReviewStatusClinicalImpact"] == "-", "ReviewStatusClinicalImpact"] = pd.NA


    df.loc[df["LastEvaluated"] == "-", "LastEvaluated"] = pd.NA

    df.loc[df["SomaticClinicalImpactLastEvaluated"] == "-", "SomaticClinicalImpactLastEvaluated"] = pd.NA

    df.loc[df["OncogenicityLastEvaluated"] == "-", "OncogenicityLastEvaluated"] = pd.NA

    df.loc[df["Start"] == "-", "Start"] = pd.NA
    df.loc[df["OtherIDs"] == "-", "OtherIDs"] = pd.NA


    df.loc[df["ReferenceAlleleVCF"] == "na", "ReferenceAlleleVCF"] = pd.NA
    df.loc[df["ReferenceAlleleVCF"] == "", "ReferenceAlleleVCF"] = pd.NA

    df.loc[df["AlternateAlleleVCF"] == "na", "AlternateAlleleVCF"] = pd.NA
    df.loc[df["AlternateAlleleVCF"] == "", "AlternateAlleleVCF"] = pd.NA



    df.loc[df["HGNC_ID"] == "-", "HGNC_ID"] = pd.NA
    df.loc[df["ClinicalSignificance"] == "-", "ClinicalSignificance"] = pd.NA
    df.loc[df["RCVaccession"] == "-", "RCVaccession"] = pd.NA
    df.loc[df["PhenotypeIDS"] == "-", "PhenotypeIDS"] = pd.NA



    # Convert to datetime
    df["LastEvaluated"] = pd.to_datetime(df["LastEvaluated"], format="%b %d, %Y")

    df["SomaticClinicalImpactLastEvaluated"] = pd.to_datetime(df["SomaticClinicalImpactLastEvaluated"], format="%b %d, %Y")

    df["OncogenicityLastEvaluated"] = pd.to_datetime(df["OncogenicityLastEvaluated"], format="%b %d, %Y")


    df.loc[df["nsv/esv (dbVar)"] == "-", "nsv/esv (dbVar)"] = pd.NA

    df.loc[df["Start"] == -1, "Start"] = pd.NA
    df.loc[df["Stop"] == -1, "Stop"] = pd.NA
    df.loc[df["RS# (dbSNP)"] == -1, "RS# (dbSNP)"] = pd.NA
    df.loc[df["PositionVCF"] == -1, "PositionVCF"] = pd.NA
    df.loc[df["GeneID"] == -1, "GeneID"] = pd.NA

    df["GeneID"] = df["GeneID"].astype("Int64")
    df["Start"] = df["Start"].astype("Int64")
    df["Stop"] = df["Stop"].astype("Int64")
    df["PositionVCF"] = df["PositionVCF"].astype("Int64")
    df["RS# (dbSNP)"] = df["RS# (dbSNP)"].astype("Int64")
    df["Chromosome"] = df["Chromosome"].astype(str)


    df.loc[df["Cytogenetic"] == "-", "Cytogenetic"] = pd.NA
    df.loc[df["GeneSymbol"] == "-", "GeneSymbol"] = pd.NA
    df.loc[df["ReferenceAllele"] == "na", "ReferenceAllele"] = pd.NA
    df.loc[df["AlternateAllele"] == "na", "AlternateAllele"] = pd.NA
    df.loc[df["Chromosome"] == "na", "Chromosome"] = pd.NA
    df.loc[df["ChromosomeAccession"] == "na", "ChromosomeAccession"] = pd.NA
    df.loc[df["Assembly"] == "na", "Assembly"] = pd.NA

    df["TestedInGTR"] = df["TestedInGTR"].map({"Y": True, "N": False})

    return df

