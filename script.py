import pandas as pd

path_file="presales_data_sample.csv"
df=pd.read_csv(path_file)

print(df.head())
print(df.shape)
print(df.columns)
print(df.info())

nr_input=df["input_row_key"].nunique()
print("Nr of clients input", nr_input)

candidates_per_company=df.groupby("input_row_key").size()
print("Candidates per company",candidates_per_company)
print("Nr of companies by nr of candidates\n",candidates_per_company.value_counts())

first_company=df[df["input_row_key"]==0]
columns_to_show=[  "input_row_key",
    "input_company_name",
    "input_main_country",
    "input_main_city",
    "company_name",
    "main_country",
    "main_city",
    "website_url"]
print(first_company[columns_to_show])

missing_values=df.isnull().sum()
print("Missing values\n",missing_values)


important_columns=[  "input_company_name",
    "input_main_country",
    "input_main_city",
    "input_main_postcode",
    "input_main_street",
    "input_main_street_number",
    "company_name",
    "main_country",
    "main_city",
    "main_postcode",
    "main_street",
    "main_street_number",
    "website_url",
    "veridion_id"]

missing_values_important=df[important_columns].isnull().sum()
print("\n\nImportant missing values\n",missing_values_important)


def clean_text(value):
    if pd.isna(value):
        return ""

    value=str(value).lower()
    value=value.strip()
    value=value.replace(".", "")
    value=value.replace(",", "")
    value=value.replace("-", " ")
    value = " ".join(value.split())

    return value

df["input_company_name_clean"] = df["input_company_name"].apply(clean_text)
df["company_name_clean"] = df["company_name"].apply(clean_text)

df["input_country_clean"] = df["input_main_country"].apply(clean_text)
df["country_clean"] = df["main_country"].apply(clean_text)

df["input_city_clean"] = df["input_main_city"].apply(clean_text)
df["city_clean"] = df["main_city"].apply(clean_text)

df["input_postcode_clean"] = df["input_main_postcode"].apply(clean_text)
df["postcode_clean"] = df["main_postcode"].apply(clean_text)


candidate_review_columns = [
    "input_row_key",
    "input_company_name",
    "input_company_name_clean",
    "company_name",
    "company_name_clean",
    "input_main_country",
    "input_country_clean",
    "main_country",
    "country_clean",
    "input_main_city",
    "input_city_clean",
    "main_city",
    "city_clean",
    "input_main_postcode",
    "input_postcode_clean",
    "main_postcode",
    "postcode_clean",
    "input_main_street",
    "main_street",
    "website_url",
    "veridion_id"]

df[candidate_review_columns].to_excel("Analysis.xlsx",sheet_name="Candidates clean data",index=False)


df["same_name"] = (
    (df["input_company_name_clean"] != "")
    & (df["company_name_clean"] != "")
    & (df["input_company_name_clean"] == df["company_name_clean"])
)

df["same_country"] = (
    (df["input_country_clean"] != "")
    & (df["country_clean"] != "")
    & (df["input_country_clean"] == df["country_clean"])
)

df["same_city"] = (
    (df["input_city_clean"] != "")
    & (df["city_clean"] != "")
    & (df["input_city_clean"] == df["city_clean"])
)

df["same_postcode"] = (
    (df["input_postcode_clean"] != "")
    & (df["postcode_clean"] != "")
    & (df["input_postcode_clean"] == df["postcode_clean"])
)
def simplify_company_name(value):
    value = clean_text(value)

    value = value.replace("(", "")
    value = value.replace(")", "")

    legal_words = [
        "limited",
        "ltd",
        "llc",
        "inc",
        "incorporated",
        "corp",
        "corporation",
        "gmbh",
        "srl",
        "sa",
        "plc",
        "private",
        "pte",
        "pty"
    ]

    words = value.split()
    remaining_words = []

    for word in words:
        if word not in legal_words:
            remaining_words.append(word)

    return " ".join(remaining_words)

df["input_company_name_simple"] = ( df["input_company_name"].apply(simplify_company_name))

df["company_name_simple"] = (  df["company_name"].apply(simplify_company_name))

df["same_name_simple"] = (
    (df["input_company_name_simple"] != "")
    & (df["company_name_simple"] != "")
    & ( df["input_company_name_simple"] == df["company_name_simple"] )
)

df["name_match"] = (df["same_name"] | df["same_name_simple"])


print("\n name matches ")
print(df["same_name"].value_counts())

print("\nCountry matches ")
print(df["same_country"].value_counts())

print("\nCity matches ")
print(df["same_city"].value_counts())

print("\nPostcode matches ")
print(df["same_postcode"].value_counts())

comparison_columns = [
     "input_row_key",
    "input_company_name",
    "input_company_name_simple",
    "company_name",
    "company_name_simple",
    "same_name",
    "same_name_simple",
    "name_match",

    "input_main_country",
    "main_country",
    "same_country",

    "input_main_city",
    "main_city",
    "same_city",

    "input_main_postcode",
    "main_postcode",
    "same_postcode",

    "website_url",
    "veridion_id"
]


df[comparison_columns].to_excel("Comparison.xlsx",sheet_name="Comparisons",index=False)


def calculate_score(row):
    score = 0

    if row["name_match"] == True:
        score = score + 4

    if row["same_country"] == True:
        score = score + 2

    if row["same_city"] == True:
        score = score + 2

    if row["same_postcode"] == True:
        score = score + 2

    return score


df["match_score"] = df.apply(calculate_score, axis=1)

best_candidate_indexes = (
    df.groupby("input_row_key")["match_score"]
    .idxmax()
)

best_candidates = df.loc[best_candidate_indexes].copy()


final_columns = [
    "input_row_key",
    "input_company_name",
    "company_name",
    "veridion_id",
    "match_score",
    "name_match",
    "same_country",
    "same_city",
    "same_postcode",
    "input_main_country",
    "main_country",
    "input_main_city",
    "main_city",
    "input_main_postcode",
    "main_postcode",
    "website_url"
]

best_candidates[final_columns].to_excel("Final matches.xlsx",sheet_name="Selected matches",index=False)

print("\nNumber of selected matches:", len(best_candidates))


name_comparison_columns = [
    "input_row_key",
    "input_company_name",
    "input_company_name_clean",
    "input_company_name_simple",
    "company_name",
    "company_name_clean",
    "company_name_simple",
    "same_name",
    "same_name_simple",
    "name_match",
    "input_main_country",
    "main_country",
    "website_url"
]

df[name_comparison_columns].to_excel(
    "Name comparison.xlsx",
    sheet_name="Name comparison",
    index=False
)

print("\nExact name matches")
print(df["same_name"].value_counts())

print("\nSimplified name matches")
print(df["same_name_simple"].value_counts())

print("\nFinal name matches")
print(df["name_match"].value_counts())

df["input_street_clean"] = df["input_main_street"].apply(clean_text)
df["street_clean"] = df["main_street"].apply(clean_text)


df["same_street"] = (
    (df["input_street_clean"] != "")
    & (df["street_clean"] != "")
    & (df["input_street_clean"] == df["street_clean"])
)


def names_contain_each_other(row):
    input_name = row["input_company_name_simple"]
    candidate_name = row["company_name_simple"]

    if input_name == "" or candidate_name == "":
        return False

    if len(input_name) < 4 or len(candidate_name) < 4:
        return False

    if input_name in candidate_name:
        return True

    if candidate_name in input_name:
        return True

    return False


df["name_contains"] = df.apply(
    names_contain_each_other,
    axis=1
)


def calculate_improved_score(row):
    score = 0

    if row["name_match"] == True:
        score = score + 4

    elif row["name_contains"] == True:
        score = score + 3

    if row["same_country"] == True:
        score = score + 2

    if row["same_city"] == True:
        score = score + 1

    if row["same_postcode"] == True:
        score = score + 2

    if row["same_street"] == True:
        score = score + 1

    return score


df["improved_match_score"] = df.apply(
    calculate_improved_score,
    axis=1
)


maximum_scores = (
    df.groupby("input_row_key")["improved_match_score"]
    .transform("max")
)

df["has_top_score"] = (
    df["improved_match_score"] == maximum_scores
)


top_score_counts = (
    df.groupby("input_row_key")["has_top_score"]
    .sum()
)


best_candidate_indexes = (
    df.groupby("input_row_key")["improved_match_score"]
    .idxmax()
)

best_candidates_improved = df.loc[
    best_candidate_indexes
].copy()


best_candidates_improved["nr_candidates_with_top_score"] = (
    best_candidates_improved["input_row_key"]
    .map(top_score_counts)
)

best_candidates_improved["needs_manual_review"] = (
    (best_candidates_improved["nr_candidates_with_top_score"] > 1)
    | (best_candidates_improved["improved_match_score"] < 5)
    | (
        (best_candidates_improved["name_match"] == False)
        & (best_candidates_improved["name_contains"] == False)
    )
)


best_candidates_improved["selected_veridion_id_count"] = (
    best_candidates_improved.groupby("veridion_id")["veridion_id"]
    .transform("count")
)


best_candidates_improved["possible_duplicate_input"] = (
    best_candidates_improved["selected_veridion_id_count"] > 1
)


improved_final_columns = [
    "input_row_key",
    "input_company_name",
    "company_name",
    "veridion_id",
    "improved_match_score",
    "nr_candidates_with_top_score",
    "needs_manual_review",
    "name_match",
    "name_contains",
    "same_country",
    "same_city",
    "same_postcode",
    "same_street",
    "input_main_country",
    "main_country",
    "input_main_city",
    "main_city",
    "input_main_postcode",
    "main_postcode",
    "input_main_street",
    "main_street",
    "website_url",
    "selected_veridion_id_count",
    "possible_duplicate_input"
]


best_candidates_improved[improved_final_columns].to_excel(  "Final matches improved.xlsx", sheet_name="Selected matches", index=False)
manual_review = best_candidates_improved[ best_candidates_improved["needs_manual_review"] == True]
manual_review[improved_final_columns].to_excel( "Manual review.xlsx",  sheet_name="Manual review",  index=False)


print("\nNumber of selected matches", len(best_candidates_improved))

print( "\nNumber of matches for manual review",  best_candidates_improved["needs_manual_review"].sum())

print("\nImproved score distribution")

print(  best_candidates_improved["improved_match_score"]
    .value_counts()
    .sort_index())

