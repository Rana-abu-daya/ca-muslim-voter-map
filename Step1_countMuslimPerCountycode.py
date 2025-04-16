import pandas as pd

# Load your full merged data (with CountyCode, Voted, etc.)
df = pd.read_csv("muslim_voters_with_vote_status.csv")

# --- Step 1: Total Muslim count per CountyCode ---
total_counts = df.groupby("CountyCode").size().reset_index(name="Muslim_Total")

# --- Step 2: Filter for voted == 'Yes' ---
voted_df = df[df["Voted"].str.lower() == "yes"]
voted_counts = voted_df.groupby("CountyCode").size().reset_index(name="Muslim_Voted")

# --- Step 3: Merge both counts ---
merged = pd.merge(total_counts, voted_counts, on="CountyCode", how="left")

# Fill NaN voted counts with 0
merged["Muslim_Voted"] = merged["Muslim_Voted"].fillna(0).astype(int)

# --- Step 4: Calculate percentage ---
merged["Muslim_Voted_Percent"] = (merged["Muslim_Voted"] / merged["Muslim_Total"]) * 100
merged["Muslim_Voted_Percent"] = merged["Muslim_Voted_Percent"].round(2)  # Optional: round to 2 decimals

# --- Step 5: Save to file ---
merged.to_csv("MuslimVoterStatsByCountyCode.csv", index=False)
print("✅ Saved to MuslimVoterStatsByCountyCode.csv")
