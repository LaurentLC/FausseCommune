from flask import Flask, render_template, request

from create_name import MarkovModel

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('gpt.html')

@app.route('/get_geo_info', methods=['POST'])
def get_geo_info():
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    model = MarkovModel((lat, long), 3)
    names = model.generate_names(10)
    return ', '.join(names)

if __name__ == '__main__':
    app.run(debug=True)
