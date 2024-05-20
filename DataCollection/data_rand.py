import pandas as pd
df = pd.read_csv('ufc2.csv')
print(df)
df.rename(columns={'fighterxw': 'fighterx'}, inplace=True)
df.rename(columns={'fighteryl': 'fightery'}, inplace=True)

df.rename(columns={'stancexopenstance': 'stanceopenstancex'}, inplace=True)
df.rename(columns={'stancexorthodox': 'stanceorthodoxx'}, inplace=True)
df.rename(columns={'stancexsouthpaw': 'stancesouthpawx'}, inplace=True)
df.rename(columns={'stancexswitch': 'stanceswitchx'}, inplace=True)

df.rename(columns={'stanceyopenstance': 'stanceopenstancey'}, inplace=True)
df.rename(columns={'stanceyorthodox': 'stanceorthodoxy'}, inplace=True)
df.rename(columns={'stanceysouthpaw': 'stancesouthpawy'}, inplace=True)
df.rename(columns={'stanceyswitch': 'stanceswitchy'}, inplace=True)

columns_to_swap = ['fighterx', 'fightery', 'agex', 'heightx', 'reachx', 'slpmx', 'stacx', 'sapmx', 
                   'tdavgx', 'tdaccx', 'tddefx', 'subavgx', 'winsx', 'lossesx', 'drawsx', 'stanceopenstancex', 
                   'stanceorthodoxx', 'stancesouthpawx', 'stanceswitchx', 'agey', 'heighty', 'reachy', 'slpmy', 
                   'stacy', 'sapmy', 'tdavgy', 'tdaccy', 'tddefy', 'subavgy', 'winsy', 'lossesy', 'drawsy', 
                   'stanceopenstancey', 'stanceorthodoxy', 'stancesouthpawy', 'stanceswitchy']

# Swap the values within specified columns


df = df.sort_values(by='wl')
value_to_count = 2
num_twos = (df['wl'] == value_to_count).sum()
iters = df.shape[0] - num_twos

iters = iters // 2
i = 0

df = df.sample(frac=1)
rows_to_swap = df.sample(frac=0.5).index

for row in rows_to_swap:
    for column in columns_to_swap:
        # Perform the swap
        df.at[row, column], df.at[row, column[:-1] + 'y'] = df.at[row, column[:-1] + 'y'], df.at[row, column]
        # Set the corresponding cell in the 'wl' column to 0
        df.at[row, 'wl'] = 0


df = df.sort_values('fighterx')
print(df)

df = df.drop('Unnamed: 0', axis=1)

df = df[df['wl'] != 2]

df.to_csv(r"fixed.csv", index=False) 
