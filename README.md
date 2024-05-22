# MMAI
Neural Network Predictive Model for MMA Fights - 69.41% accurate
ML Files:
DataCollection folder - Code I used to scrape and normalize stats
fighter_stats.csv - CSV with all fighter stats I scraped and normalized 
full_ufc_data.csv - CSV of historical fight outcomes appended with fighter stats for training
train.py - model is trained
predict.py - allows the user to input the names of two UFC fighters and get the projected victor with % likelyhood/confidence
scaler.pkl - min/max scalar for predict.py
UFC folder - trained, saved model

To try the model with minimum effort, download the UFC folder, scalar.pkl and predict.py. Call the main function with two fighter names. Enjoy!

Front End Files
website.py - main flask app to handle user input and victor projection
static - folder w JavaScript file, CSS, and images
templates - html

