# MMAI
**Neural Network Predictive Model for MMA Fights - 69.41% Accuracy**

## Overview
MMAI is a machine learning model designed to predict the outcomes of MMA fights with a 70% accuracy rate. This repository includes all necessary code and data for scraping fight statistics, training the model, and making predictions via a web interface.

## Repository Structure

### Machine Learning Files
- **DataCollection/**: Contains code for scraping and normalizing fight statistics.
- **fighter_stats.csv**: CSV file with normalized fighter statistics.
- **full_ufc_data.csv**: CSV file with historical fight outcomes and fighter statistics, used for training.
- **train.py**: Script to train the neural network model.
- **predict.py**: Script to predict fight outcomes. Users can input the names of two UFC fighters to get the projected victor and the confidence percentage.
- **scaler.pkl**: Min/Max scaler used in `predict.py`.
- **UFC/**: Folder containing the trained and saved model.

### Front End Files
- **website.py**: Main Flask app to handle user input and victor projection.
- **static/**: Contains JavaScript files, CSS, and images.
- **templates/**: HTML templates for the web interface.

## Quick Start
To try the model with minimal effort, follow these steps:

### Download Required Files
- `UFC` folder
- `scaler.pkl`
- `predict.py`

### Run Predictions
Call the main function in `predict.py` with the names of two fighters.
Example:
```python
from predict import main
result = main("Fighter A", "Fighter B")
print(result)
