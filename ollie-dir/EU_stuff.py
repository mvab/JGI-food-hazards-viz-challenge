import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

food_haz = pd.read_csv('data/tidy/food_hazards_data_all.csv')
fruitveg = food_haz.loc[food_haz.product_categoty == 'fruits and vegetables']
fruitveg = fruitveg[fruitveg.origin_country_EU != 'UK']

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

plt.figure(figsize=(10, 8))
sns.barplot('freq', 'hazard', hue='origin', data=counts.sort_values('freq', ascending=False))
plt.tight_layout()

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
    row = [haz, diff]
    diff_df.loc[len(diff_df)] = row
diff_df.sort_values('freq_diff', ascending=False, inplace=True)


def colors_from_values(values, palette_name):
    # normalize the values to range [0, 1]
    normalized = (values - min(values)) / (max(values) - min(values))
    # convert to indices
    indices = np.round(normalized * (len(values) - 1)).astype(np.int32)
    # use the indices to get the colors
    palette = sns.color_palette(palette_name, len(values))
    return np.array(palette).take(indices, axis=0)

y = list(diff_df.freq_diff.values)
y[-1]+=0.09
y[0] -= 0.03
y[1] -= 0.02
plt.figure(figsize=(10, 8))
sns.barplot('freq_diff', 'hazard', data=diff_df, palette=colors_from_values(y, 'cool'))
plt.ylabel('')
plt.xlabel('Relative frequency change')
plt.title('Difference in relative frequency of hazard types\nwhen changing from EU to non-EU fuits and veg')
plt.tight_layout()
