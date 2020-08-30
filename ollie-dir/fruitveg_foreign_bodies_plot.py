import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

food_haz = pd.read_csv('data/tidy/food_hazards_foreign_bodies.csv')
food_haz = food_haz[food_haz.origin_country_EU != 'UK']
food_haz = food_haz[pd.notna(food_haz.origin_country_EU)]
food_haz = food_haz[food_haz.product_categoty == 'fruits and vegetables']

eu_count = sum(['non' not in x for x in food_haz.origin_country_EU.values])
non_eu_count = len(food_haz) - eu_count
counts = pd.DataFrame(columns=['origin', 'contaminant', 'count', 'freq'])
for tup, df in food_haz.groupby(['origin_country_EU', 'contaminant']):
    row = [tup[0], tup[1], len(df)]
    if 'non' in tup[0]:
        freq = len(df)/non_eu_count
    else:
        freq = len(df)/eu_count
    row.append(freq)
    counts.loc[len(counts)] = row


diff_df = pd.DataFrame(columns=['contaminant', 'freq_diff'])
for haz, df in counts.groupby('contaminant'):
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


def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

kepler_arc_blue = '#3748a6'
kepler_arc_red ='#951416'
header_blue = '#0E33FF'
header_red = '#FD250B'
color_vals = [(val-min(diff_df.freq_diff))/(max(diff_df.freq_diff)-min(diff_df.freq_diff)) for val in diff_df.freq_diff]
color_vals_uniform = [x/len(color_vals) for x in range(len(color_vals), 0, -1)]
color_vals2 = [np.mean(x) for x in zip(color_vals, color_vals_uniform)]
colorlist = [colorFader(header_blue, header_red, val) for val in color_vals2]
custom_palette = sns.color_palette(colorlist)

plt.style.use("dark_background")
plt.figure(figsize=(10, 8))
sns.barplot('freq_diff', 'contaminant', data=diff_df, palette=custom_palette)
plt.ylabel('')
plt.xlabel('Relative frequency change after switching to non-EU imports')
plt.title('Foreign bodies in fruits and vegetables: EU vs non-EU imports')
plt.tight_layout()
plt.savefig('foreign_bodies_eu_noneu.png')

