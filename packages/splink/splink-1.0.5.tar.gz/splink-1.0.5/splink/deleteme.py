{
    "link_type": "dedupe_only",
    "blocking_rules": ["l.surname = r.surname"],
    "comparison_columns": [
        {
            "col_name": "first_name",
            "num_levels": 3,
            "term_frequency_adjustments": True,
            "u_probabilities": [
                0.9908120130708656,
                0.0036188357389467453,
                0.005569151190187595,
            ],
            "fix_u_probabilities": True,
            "gamma_index": 0,
            "data_type": "string",
            "fix_m_probabilities": False,
            "case_expression": "case\n    when first_name_l is null or first_name_r is null then -1\n    when jaro_winkler_sim(first_name_l, first_name_r) >= 1.0 then 2\n    when jaro_winkler_sim(first_name_l, first_name_r) >= 0.88 then 1\n    else 0 end as gamma_first_name",
            "m_probabilities": [
                0.15479041635990143,
                0.17001093924045563,
                0.6751986742019653,
            ],
        },
        {
            "col_name": "dob",
            "u_probabilities": [0.9962962963256157, 0.003703703674384289],
            "fix_u_probabilities": True,
            "gamma_index": 1,
            "num_levels": 2,
            "data_type": "string",
            "term_frequency_adjustments": False,
            "fix_m_probabilities": False,
            "case_expression": "case\n    when dob_l is null or dob_r is null then -1\n    when dob_l = dob_r then 1\n    else 0 end as gamma_dob",
            "m_probabilities": [0.36263617873191833, 0.637363851070404],
        },
        {
            "col_name": "city",
            "term_frequency_adjustments": True,
            "u_probabilities": [0.9069219028892688, 0.09307809711073121],
            "fix_u_probabilities": True,
            "gamma_index": 2,
            "num_levels": 2,
            "data_type": "string",
            "fix_m_probabilities": False,
            "case_expression": "case\n    when city_l is null or city_r is null then -1\n    when city_l = city_r then 1\n    else 0 end as gamma_city",
            "m_probabilities": [0.31230080127716064, 0.6876991987228394],
        },
        {
            "col_name": "email",
            "u_probabilities": [0.9959296952930489, 0.00407030470695117],
            "fix_u_probabilities": True,
            "gamma_index": 3,
            "num_levels": 2,
            "data_type": "string",
            "term_frequency_adjustments": False,
            "fix_m_probabilities": False,
            "case_expression": "case\n    when email_l is null or email_r is null then -1\n    when email_l = email_r then 1\n    else 0 end as gamma_email",
            "m_probabilities": [0.3454569876194, 0.6545429825782776],
        },
    ],
    "additional_columns_to_retain": ["group"],
    "em_convergence": 0.01,
    "source_dataset_column_name": "source_dataset",
    "unique_id_column_name": "unique_id",
    "retain_matching_columns": True,
    "retain_intermediate_calculation_columns": False,
    "max_iterations": 25,
    "proportion_of_matches": 0.35034021735191345,
}


{
    "link_type": "dedupe_only",
    "blocking_rules": [
        "l.first_name = r.first_name",
        "l.surname = r.surname",
        "l.dob = r.dob",
        "l.email=r.email",
        "l.city=r.city",
    ],
    "comparison_columns": [
        {
            "col_name": "surname",
            "num_levels": 3,
            "term_frequency_adjustments": True,
            "u_probabilities": [
                0.9897063001993837,
                0.0028507437735149047,
                0.00744295602710143,
            ],
            "fix_u_probabilities": True,
            "gamma_index": 0,
            "data_type": "string",
            "fix_m_probabilities": False,
            "case_expression": "case\n    when surname_l is null or surname_r is null then -1\n    when jaro_winkler_sim(surname_l, surname_r) >= 1.0 then 2\n    when jaro_winkler_sim(surname_l, surname_r) >= 0.88 then 1\n    else 0 end as gamma_surname",
            "m_probabilities": [
                0.2328722513244618,
                0.11981253760685301,
                0.5697402298459208,
            ],
        },
        {
            "col_name": "dob",
            "u_probabilities": [0.9962962963256157, 0.003703703674384289],
            "fix_u_probabilities": True,
            "gamma_index": 1,
            "num_levels": 2,
            "data_type": "string",
            "term_frequency_adjustments": False,
            "fix_m_probabilities": False,
            "case_expression": "case\n    when dob_l is null or dob_r is null then -1\n    when dob_l = dob_r then 1\n    else 0 end as gamma_dob",
            "m_probabilities": [0.38688689610605903, 0.6102704424491996],
        },
        {
            "col_name": "city",
            "term_frequency_adjustments": True,
            "u_probabilities": [0.9069219028892688, 0.09307809711073121],
            "fix_u_probabilities": True,
            "gamma_index": 2,
            "num_levels": 2,
            "data_type": "string",
            "fix_m_probabilities": False,
            "case_expression": "case\n    when city_l is null or city_r is null then -1\n    when city_l = city_r then 1\n    else 0 end as gamma_city",
            "m_probabilities": [0.32984029768985335, 0.6673547894880234],
        },
        {
            "col_name": "email",
            "u_probabilities": [0.9959296952930488, 0.00407030470695117],
            "fix_u_probabilities": True,
            "gamma_index": 3,
            "num_levels": 2,
            "data_type": "string",
            "term_frequency_adjustments": False,
            "fix_m_probabilities": False,
            "case_expression": "case\n    when email_l is null or email_r is null then -1\n    when email_l = email_r then 1\n    else 0 end as gamma_email",
            "m_probabilities": [0.32866372382284414, 0.66901344832428],
        },
        {
            "col_name": "first_name",
            "num_levels": 3,
            "term_frequency_adjustments": True,
            "u_probabilities": [
                0.9908120130708656,
                0.003618835738946745,
                0.005569151190187595,
            ],
            "fix_u_probabilities": True,
            "gamma_index": 0,
            "data_type": "string",
            "fix_m_probabilities": False,
            "case_expression": "case\n    when first_name_l is null or first_name_r is null then -1\n    when jaro_winkler_sim(first_name_l, first_name_r) >= 1.0 then 2\n    when jaro_winkler_sim(first_name_l, first_name_r) >= 0.88 then 1\n    else 0 end as gamma_first_name",
            "m_probabilities": [
                0.22677486490268212,
                0.15713624882047705,
                0.5254085858112877,
            ],
        },
    ],
    "additional_columns_to_retain": ["group"],
    "em_convergence": 0.01,
    "source_dataset_column_name": "source_dataset",
    "unique_id_column_name": "unique_id",
    "retain_matching_columns": True,
    "retain_intermediate_calculation_columns": False,
    "max_iterations": 25,
    "proportion_of_matches": 0.01121798826501255,
}

from pyspark.context import SparkContext
from pyspark.sql import SparkSession

sc = SparkContext.getOrCreate()
spark = SparkSession(sc)
from pyspark.sql import Row

data_list = [
    {"comp_l": ["robin", "john"], "comp_r": ["robyn", "james"]},
]

df = spark.createDataFrame(Row(**x) for x in data_list)
df.createOrReplaceTempView("df")
df.show()