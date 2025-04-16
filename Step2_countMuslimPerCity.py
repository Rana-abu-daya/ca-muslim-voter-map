import pandas as pd

# Load full merged voter file
df = pd.read_csv("MuslimsDistrict.csv")

# Filter only Arab voters
# Group by City and count
city_counts = df.groupby("City").size().reset_index(name="MuslimNumbers")

# Save to file
city_counts.to_csv("MuslimsPerCity.csv", index=False)
print("✅ Saved arab_voters_by_city.csv")
