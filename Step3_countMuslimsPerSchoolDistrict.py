import pandas as pd
import re

# Load your dataset
df = pd.read_csv("muslim_voters_with_vote_status.csv")

# Clean the 'School District' column
def clean_district(name):
    if isinstance(name, str):
        name = name.lower()
        match = re.search(r"(.*?school district)", name)
        if match:
            return match.group(1).strip()
        return name.strip()
    return ""  # return empty string for NaN or invalid entries

df["clean_district"] = df["School District"].apply(clean_district)

# Total Muslim count per district
total_counts = df.groupby("clean_district").size().reset_index(name="Muslim_Total")

# Voted Muslim count per district
voted_df = df[df["Voted"].str.lower() == "yes"]
voted_counts = (
    voted_df.groupby("clean_district")
    .size()
    .reset_index(name="Muslim_Voted")
)

# Merge both
merged = pd.merge(total_counts, voted_counts, on="clean_district", how="left")

# Fill NaN and calculate percentage
merged["Muslim_Voted"] = merged["Muslim_Voted"].fillna(0).astype(int)
merged["Muslim_Voted_Percent"] = (merged["Muslim_Voted"] / merged["Muslim_Total"] * 100).round(2)

# Rename for consistency
merged = merged.rename(columns={"clean_district": "school_district"})

# Save to file
merged.to_csv("MuslimPerSchoolDistrictVoted2.csv", index=False)
print("✅ Saved to MuslimPerSchoolDistrict.csv")
