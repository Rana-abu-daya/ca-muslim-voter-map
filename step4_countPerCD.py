import pandas as pd

# Load full merged voter file (must have 'Congressional District' and 'Voted' columns)
df = pd.read_csv("muslim_Voters_data_with_SchoolDistrict_CD_LD_Voted.csv")

# Step 1: Clean 'Congressional District' names
df["Congressional District"] = df["Congressional District"].astype(str).str.strip()

# Step 2: Total Muslim count per Congressional District
total_counts = df.groupby("Congressional District").size().reset_index(name="Muslim_Total")

# Step 3: Voted Muslim count per Congressional District
voted_counts = (
    df[df["Voted"].str.lower() == "yes"]
    .groupby("Congressional District")
    .size()
    .reset_index(name="Muslim_Voted")
)

# Step 4: Merge both counts
merged = pd.merge(total_counts, voted_counts, on="Congressional District", how="left")

# Fill NaN voted counts with 0
merged["Muslim_Voted"] = merged["Muslim_Voted"].fillna(0).astype(int)

# Step 5: Calculate voting percentage
merged["Muslim_Voted_Percent"] = (
    merged["Muslim_Voted"] / merged["Muslim_Total"] * 100
).round(2)

# Step 6: Save the result
merged.to_csv("MuslimsPerCongressionalDistrictVoting.csv", index=False)
print("✅ Saved to MuslimsPerCongressionalDistrictVoting.csv")
