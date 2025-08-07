import os
import random
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

data_kupon = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_kupon
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            df = pd.read_excel(filepath)
            data_kupon = df.to_dict(orient='records')
            return redirect(url_for('draw'))
    return render_template('index.html')

@app.route('/draw')
def draw():
    return render_template('result.html', data=data_kupon)

@app.route('/get_winner')
def get_winner():
    if data_kupon:
        winner = random.choice(data_kupon)
        return winner
    return {}

from flask import jsonify

@app.route('/save_winners', methods=['POST'])
def save_winners():
    from flask import request
    winners = request.get_json()
    if winners:
        df = pd.DataFrame(winners)
        df.to_excel("winners.xlsx", index=False)
        return jsonify({"status": "success"})
    return jsonify({"status": "failed"})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
