import pandas as pd

# Load full merged voter file
df = pd.read_csv("MuslimsDistrict.csv")

# Filter only Arab voters
# Group by City and count
city_counts = df.groupby("CountyCode").size().reset_index(name="Muslim_Numbers")

# Save to file
city_counts.to_csv("MuslimPerCountycode.csv", index=False)
print("✅ Saved arab_voters_by_city.csv")
