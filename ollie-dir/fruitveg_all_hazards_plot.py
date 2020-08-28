import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

food_haz = pd.read_csv('data/tidy/food_hazards_data_all.csv')
fruitveg = food_haz.loc[food_haz.product_categoty == 'fruits and vegetables']
fruitveg = fruitveg[fruitveg.origin_country_EU != 'UK']
fruitveg = fruitveg[pd.notna(fruitveg.origin_country_EU)]

eu_count = sum(['non' not in x for x in fruitveg.origin_country_EU])
non_eu_count = len(fruitveg) - eu_count
counts = pd.DataFrame(columns=['origin', 'hazard', 'count', 'freq'])
for tup, df in fruitveg.groupby(['origin_country_EU', 'hazard_group']):
    row = [tup[0], tup[1], len(df)]
    if 'non' in tup[0]:
        freq = len(df)/non_eu_count
    else:
        freq = len(df)/eu_count
    row.append(freq)
    counts.loc[len(counts)] = row

to_merge = {
    10: 11,
    3: 25,
    32: 53
}
for i, row in counts.iterrows():
    if i in to_merge.keys():
        counts['count'][to_merge[i]] += row['count']
        counts['freq'][to_merge[i]] += row['freq']
        counts.drop(index=[i], inplace=True)
diff_df = pd.DataFrame(columns=['hazard', 'freq_diff'])
for haz, df in counts.groupby('hazard'):
    if len(df) == 1:
        if 'non_EU' in df.origin:
            diff = df.freq.iloc[0]
        else:
            diff = - df.freq.iloc[0]
    else:
        eu_freq = df.loc[df.origin == 'EU'].freq.iloc[0]
        non_eu_freq = df.loc[df.origin == 'non_EU'].freq.iloc[0]
        diff = non_eu_freq - eu_freq
    if '(other)' in haz:
        haz = haz[:-8]
    row = [haz.capitalize(), diff]
    diff_df.loc[len(diff_df)] = row
diff_df.sort_values('freq_diff', ascending=False, inplace=True)

plt.style.use("dark_background")
plt.figure(figsize=(10, 8))
sns.barplot('freq_diff', 'hazard', data=diff_df, palette='RdBu')
plt.ylabel('')
plt.xlabel('Relative frequency change after switching to non-EU imports')
plt.title('Hazard alerts for fruits and vegetables: EU vs non-EU imports')
plt.tight_layout()
plt.savefig('figures/all_hazards_eu_noneu.png')
