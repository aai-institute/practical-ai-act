class CensusASECMetadata:
    """
    Metadata class that provides human-readable mappings for the Census ASEC dataset.

    This includes column names, feature categorizations, and the target variable
    for income prediction.
    """

    class Fields:
        """Mapping of original column names to human-readable names for Census ASEC data."""

        # Demographics
        AGE_YEARS = "A_AGE"
        GENDER = "A_SEX"
        EDUCATION_LEVEL = "A_HGA"
        ENROLLMENT_STATUS = "A_ENRLW"
        ENROLLMENT_TYPE = "A_FTPT"
        SCHOOL_ENROLLMENT = "A_HSCOL"
        MARITAL_STATUS = "A_MARITL"
        HOUSEHOLD_RELATIONSHIP = "P_STAT"
        HAS_CERTIFICATION = "PECERT1"
        HISPANIC_ORIGIN = "PEHSPNON"
        HISPANIC_ETHNICITY = "PRDTHSP"
        ASIAN_ETHNICITY = "PRDASIAN"
        RACE = "PRDTRACE"
        COUNTRY_OF_BIRTH = "PENATVTY"
        CITIZENSHIP_STATUS = "PRCITSHP"
        DISABILITY_STATUS = "PRDISFLG"

        # Employment & Work
        EMPLOYMENT_STATUS = "A_LFSR"
        EMPLOYMENT_CLASS = "A_CLSWKR"
        FULL_TIME_LABOR_FORCE = "A_FTLF"
        UNION_MEMBERSHIP = "A_UNMEM"
        UNEMPLOYMENT_TYPE = "A_UNTYPE"
        UNEMPLOYMENT_REASON = "PRUNTYPE"
        UNEMPLOYMENT_DURATION = "A_WKSLK"
        WORK_HOURS_CATEGORY = "A_WKSTAT"
        WORK_WEEKS = "WKSWORK"
        USUAL_HOURS_PER_WEEK = "A_USLHRS"
        HOURS_PER_WEEK = "HRSWK"
        EDITED_WORK_HOURS = "A_HRS1"
        EMPLOYEE_COUNT = "NOEMP"
        INDUSTRY = "INDUSTRY"
        LONGEST_JOB_CLASS = "CLWK"
        MAJOR_INDUSTRY = "A_MJIND"
        MAJOR_OCCUPATION = "A_MJOCC"
        MAJOR_LABOR_FORCE = "PEMLR"

        # Income & Earnings
        WEEKLY_EARNINGS = "A_GRSWK"
        HOURLY_WAGE = "A_HRSPAY"
        LONGEST_JOB_INCOME_SOURCE = "ERN_SRCE"
        LONGEST_JOB_EARNINGS = "ERN_VAL"
        ANNUAL_EARNINGS = "PEARNVAL"
        SELF_EMPLOYMENT_INCOME = "SEMP_VAL"
        SECOND_JOB_INCOME = "WAGEOTR"
        ANNUAL_INCOME = "PTOTVAL"
        SALARY_BAND = "SALARY_BAND"
        ADJUSTED_GROSS_INCOME = "AGI"

        # Health & Insurance
        HAS_HEALTH_INSURANCE = "COV"
        SELF_REPORTED_HEALTH = "HEA"

        # Weights
        FINAL_WEIGHT = "A_FNLWGT"

    # Target variable
    TARGET = Fields.SALARY_BAND

    # Feature categories
    CATEGORICAL_FEATURES = [
        Fields.GENDER,
        Fields.ENROLLMENT_STATUS,
        Fields.ENROLLMENT_TYPE,
        Fields.SCHOOL_ENROLLMENT,
        Fields.MARITAL_STATUS,
        Fields.HOUSEHOLD_RELATIONSHIP,
        Fields.HAS_CERTIFICATION,
        Fields.HISPANIC_ORIGIN,
        Fields.HISPANIC_ETHNICITY,
        Fields.ASIAN_ETHNICITY,
        Fields.RACE,
        Fields.COUNTRY_OF_BIRTH,
        Fields.CITIZENSHIP_STATUS,
        Fields.DISABILITY_STATUS,
        Fields.EMPLOYMENT_STATUS,
        Fields.EMPLOYMENT_CLASS,
        Fields.FULL_TIME_LABOR_FORCE,
        Fields.UNION_MEMBERSHIP,
        Fields.UNEMPLOYMENT_TYPE,
        Fields.UNEMPLOYMENT_REASON,
        Fields.WORK_HOURS_CATEGORY,
        Fields.INDUSTRY,
        Fields.LONGEST_JOB_CLASS,
        Fields.MAJOR_INDUSTRY,
        Fields.MAJOR_OCCUPATION,
        Fields.MAJOR_LABOR_FORCE,
        Fields.LONGEST_JOB_INCOME_SOURCE,
        Fields.HAS_HEALTH_INSURANCE,
        Fields.SELF_REPORTED_HEALTH,
    ]

    NUMERIC_FEATURES = [
        Fields.AGE_YEARS,
        Fields.UNEMPLOYMENT_DURATION,
        Fields.WORK_WEEKS,
        Fields.USUAL_HOURS_PER_WEEK,
        Fields.HOURS_PER_WEEK,
        Fields.EDITED_WORK_HOURS,
        Fields.EMPLOYEE_COUNT,
        Fields.WEEKLY_EARNINGS,
        Fields.HOURLY_WAGE,
        Fields.LONGEST_JOB_EARNINGS,
        Fields.SECOND_JOB_INCOME,
        Fields.ADJUSTED_GROSS_INCOME,
        Fields.FINAL_WEIGHT,
    ]

    ORDINAL_FEATURES = [
        Fields.EDUCATION_LEVEL,
    ]
