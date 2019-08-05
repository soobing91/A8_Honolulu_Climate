from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def welcome():
    return(
        f'Welcome to the Honolulu Weather API created by Soo Bin!</br>'
        f'Available routes:</br>'
        f'/api/v1.0/precipitation</br>'
        f'/api/v1.0/stations</br>'
        f'/api/v1.0/tobs</br>'
        f'/api/v1.0/<start></br>'
        f'/api/v1.0/<start>/<end></br>'
    )

@app.route('/api/v1.0/precipitation')
def prcp():
    return()

@app.route('/api/v1.0/stations')
def prcp():
    return()

@app.route('/api/v1.0/tobs')
def prcp():
    return()

@app.route('/api/v1.0/<start>')
def prcp():
    return()

@app.route('/api/v1.0/<start>/<end>')
def prcp():
    return()

if __name__ == 'main':
    app.run(debug = True)