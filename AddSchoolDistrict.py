import pandas as pd

# Load the two CSV files
df1 = pd.read_csv('FinaaaalCD AND LD data.csv')    # This file has 'statevoterid'
df2 = pd.read_csv('muslim_voters_with_vote_status.csv')   # This file has 'resgid' and other columns

# Select only 'resgid' and the two columns you want to bring over
columns_needed = ['RegistrantID', 'School District', 'Voted']  # Replace column1, column2 with actual names
df2 = df2[columns_needed]
df2 = df2.drop_duplicates(subset=['RegistrantID'])
# Merge the two files: match statevoterid in df1 to resgid in df2
merged_df = df1.merge(df2, left_on='Voters Id', right_on='RegistrantID', how='left')

# Optionally, drop the 'resgid' after the merge if you don't need it
merged_df = merged_df.drop(columns=['RegistrantID'])

# Save the final result
merged_df.to_csv('muslim_Voters_data_with_SchoolDistrict_CD_LD_Voted.csv', index=False)

# Print to verify
print(merged_df.head())
