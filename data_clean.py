import pandas as pd
import time
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import re 
start = time.time()
#read data
fight_data_df = pd.read_csv('Data/Fights.csv')
fighter_stats_df = pd.read_csv('Data/Fighter_Stats4.csv')
fight_data_df = fight_data_df.drop('ACC METHOD', axis=1)

#alphabetize data from csv with fighter stats and csv with fight stats (for my benefit -- will rand later)
fight_data_df = fight_data_df.sort_values('WINNER (F1)')
fighter_stats_df = fighter_stats_df.sort_values('Name')

#remove any fighter with a missing val in a column (if they have a missing val, they most likely have v few fights and not very accurate)
fighter_stats_df.replace('--', pd.NA, inplace=True)
fighter_stats_df.dropna(inplace=True)

#convert DOB -> Age
fighter_stats_df['DOB'] = pd.to_datetime(fighter_stats_df['DOB'])
current_date = datetime.now()
fighter_stats_df['Age'] = (current_date - fighter_stats_df['DOB']).astype('<m8[Y]')
fighter_stats_df.drop(columns=['DOB'], inplace=True) #remove dob

#merge two data files 
all_df = pd.merge(fight_data_df, fighter_stats_df, left_on='WINNER (F1)', right_on='Name', how='left')
all_df = pd.merge(all_df, fighter_stats_df, left_on='LOSER (F2)', right_on='Name', how='left')

#renaming cols to be more in line
all_df = all_df.rename(columns={'WINNER (F1)': 'Fighter_x (W)', 'LOSER (F2)': 'Fighter_y (L)'}) 

#removing no contests - essentially these are "fluke" fights dont tell us anything statistaclly interesting
all_df.replace('nc', pd.NA, inplace=True)
all_df.dropna(inplace=True)

#removing disqualifications - again flukey way to win
all_df.replace('DQ', pd.NA, inplace=True)
all_df.dropna(inplace=True)

#remove defualt first col df 
all_df = all_df.drop(all_df.columns[0], axis=1)

#make categorical col win -> 1; draw -> 2
all_df = all_df.replace('win', 1)
all_df = all_df.replace('draw', 2)


#split record from string to 3 columns wins/losses/draws
def split_record(para):
    wins = []
    losses = []
    draws = []
    for index, row in all_df.iterrows():
        t = row[f'Record_{para}']
        rec = t.split('-')
        wins.append(int(rec[0]))
        losses.append(int(rec[1]))
        #record is sometimes: {13-5-0 3} (3 dqs - dont care abt dqs, get rid of)
        if len(rec[2]) != 1:
            rec[2] = rec[2][0]
        draws.append(int(rec[2]))

    all_df[f'Wins_{para}'] = wins
    all_df[f'Losses_{para}'] = losses 
    all_df[f'Draws_{para}'] = draws

split_record('x')
split_record('y')

#drop specific fight stats (gonna just keep method of victory)
all_df = all_df.drop(['F1 KD','F2 KD','F1 STR','F2 STR','F1 TD','F2 TD','F1 SUB','F2 SUB','WEIGHT CLASS', 
'Name_x', 'Name_y', 'Unnamed: 0_y', 'ROUNDS', 'TIME', 'Unnamed: 0', 'Record_x', 'Record_y', 'Weight_x', 'Weight_y'], axis=1)

#simplify U-DEC, M_DEC, S-DEC to just decision (less features to encode)
all_df = all_df.replace(['U-DEC', 'S-DEC', 'M-DEC'], 'DEC')

#one hot encode stances and method of victory
all_df = pd.get_dummies(all_df, columns = ['GEN METHOD', 'Stance_x', 'Stance_y']) 

#function to convert height to inches
def height_to_inches(height):
    feet, inches = height.split("'")
    total_inches = int(feet) * 12 + int(inches.replace('"', ''))
    return total_inches

#apply function to the heights
all_df['Height_x'] = all_df['Height_x'].apply(height_to_inches)
all_df['Height_y'] = all_df['Height_y'].apply(height_to_inches)

#reorganize df
all_df = all_df[['W/L', 'Fighter_x (W)', 'Fighter_y (L)', 'GEN METHOD_DEC','GEN METHOD_KO/TKO','GEN METHOD_SUB',
'Age_x', 'Height_x','Reach_x','SLpM_x','StAC_x','SApM_x','TDAVG_x','TDACC_x','TDDEF_x','SUBAVG_x', 'Wins_x','Losses_x',
'Draws_x', 'Stance_x_Open Stance','Stance_x_Orthodox','Stance_x_Southpaw','Stance_x_Switch', 'Age_y','Height_y','Reach_y',
'SLpM_y','StAC_y','SApM_y','TDAVG_y','TDACC_y','TDDEF_y','SUBAVG_y','Wins_y','Losses_y','Draws_y','Stance_y_Open Stance',
'Stance_y_Orthodox','Stance_y_Southpaw','Stance_y_Switch']]

for i, row in all_df.iterrows():
    if row['W/L'] == '1' and i % 2 == 0:
        
        all_df['A'], all_df['B'] = all_df['B'], all_df['A']


#ensure that all data besides names is a number
def str_to_int(s):
    if type(s) == str: 
        s = s.replace('%', '')
    return int(s)

for col in all_df.columns:
    if col not in ['Fighter_x (W)', 'Fighter_y (L)']:
        all_df[col] = all_df[col].apply(str_to_int)

# Function to convert column names to TensorFlow compatible format
def convert_to_tensorflow_names(column_names):
    tensorflow_names = []
    for name in column_names:
        # Remove spaces and special characters
        clean_name = re.sub(r'[^a-zA-Z0-9]+', '', name)
        # Replace slashes with underscores
        clean_name = clean_name.replace('/', '_')
        # Convert to lowercase
        clean_name = clean_name.lower()
        tensorflow_names.append(clean_name)
    return tensorflow_names

# Update column names in DataFrame
all_df.columns = convert_to_tensorflow_names(all_df.columns)

#gonna drop method of victory
columns_to_drop = ['genmethoddec', 'genmethodkotko', 'genmethodsub']
all_df.drop(columns=columns_to_drop, inplace=True)


#normal_df.to_csv(r"ufc_data_normalized.csv", index=False)
all_df.to_csv(r"ufc2.csv", index="False")
end = time.time()
print(f"Took {end - start} seconds to run.") 
