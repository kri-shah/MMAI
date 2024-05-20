import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import joblib

def predict(UFC_data):
    # Load the model
    model = tf.keras.models.load_model(
        'UFC', custom_objects=None, compile=True, safe_mode=True, 
    )
    # Extract features
    x_data = UFC_data.drop(['wl', 'fighterx', 'fightery'], axis=1)
    #print(x_data)
    # Normalize features
    scaler = joblib.load('scaler.pkl')

    # Normalize features
    x_data_normalized = scaler.transform(x_data)
    
    predictions = model.predict(x_data_normalized)

    # Print predictions
    #print("Predictions:", predictions)
    return predictions

def main(fighterx, fightery):
    df = pd.read_csv('fighter_stats.csv')

    fighterx = fighterx.title()
    fighterx = fighterx.rstrip() 
    
    
    fightery = fightery.title()
    fightery = fightery.rstrip() 
    
    fighterx_info = df[df['fighter'] == fighterx]
    fightery_info = df[df['fighter'] == fightery]
    if fighterx_info.empty:
        #print(f"{fighterx} not in database")
        return "", f"{fighterx} not in database (check spelling + only UFC fighters)"
        
    if fightery_info.empty:
        #print(f"{fightery} not in database")
        return "", f"{fightery} not in database (check spelling + only UFC fighters)"
    
    data = {
        'wl': [''],
        'fighterx': [fighterx],
        'fightery': [fightery],
    }

    input_df = pd.DataFrame(data)

    # Iterate over the columns of fighterx_info DataFrame
    for col_name, col_values in fighterx_info.items():
        if col_name != "fighter":
            input_df[f'{col_name}x'] = col_values.values

    # Iterate over the columns of fightery_info DataFrame
    for col_name, col_values in fightery_info.items():
        if col_name != "fighter":
            input_df[f'{col_name}y'] = col_values.values

    f1_odds = predict(input_df)
    f1_odds *= 100
    f1_odds = np.round(f1_odds, 2)
    
    return "", str(f1_odds[0][0])



