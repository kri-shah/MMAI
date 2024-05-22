from flask import Flask, request, render_template, jsonify
from predict import main

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        fighter1 = request.form['name1']
        fighter2 = request.form['name2']
        error, res = main(fighter1, fighter2)
        if error:
            return jsonify({'error': error}), 400
        return jsonify({'prediction': res})
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(debug=True)
