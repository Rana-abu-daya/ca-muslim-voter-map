import pandas as pd
import re

# Load your dataset
df = pd.read_csv("MuslimsDistrict.csv")

# Clean the 'School District' column
def clean_district(name):
    if isinstance(name, str):
        name = name.lower()
        match = re.search(r"(.*?school district)", name)
        if match:
            return match.group(1).strip()
        return name.strip()
    return ""  # return empty string for non-string or NaN entries

df['clean_district'] = df['School District'].apply(clean_district)

# Count number of rows per cleaned school district
district_counts = df['clean_district'].value_counts().reset_index()
district_counts.columns = ['school_district', 'count']

# Save the results
district_counts.to_csv("MuslimPerSchoolDistrict.csv", index=False)
