import pandas as pd

# Load full merged voter file (must have 'City' and 'Voted' columns)
df = pd.read_csv("muslim_voters_with_vote_status.csv")

# Step 1: Clean City names (optional but helps with grouping)
df["City"] = df["City"].astype(str).str.strip().str.title()

# Step 2: Total Muslim count per city
total_counts = df.groupby("City").size().reset_index(name="Muslim_Total")

# Step 3: Voted Muslim count per city
voted_counts = (
    df[df["Voted"].str.lower() == "yes"]
    .groupby("City")
    .size()
    .reset_index(name="Muslim_Voted")
)

# Step 4: Merge both counts
merged = pd.merge(total_counts, voted_counts, on="City", how="left")

# Fill NaN values in voted column with 0
merged["Muslim_Voted"] = merged["Muslim_Voted"].fillna(0).astype(int)

# Step 5: Calculate percentage
merged["Muslim_Voted_Percent"] = (
    merged["Muslim_Voted"] / merged["Muslim_Total"] * 100
).round(2)

# Step 6: Save to CSV
merged.to_csv("MuslimsPerCityVoting.csv", index=False)
print("✅ Saved to MuslimsPerCity.csv")
