import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify

engine = create_engine("sqlite:////Users/Mason/Data_Bootcamp/sqlalchemychallenge/Resources/hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect = True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# List all routes that are available
@app.route('/')
def Home():
    return '''
        <div>
            Home Page
            <ul>
                <li>/api/v1.0/precipitation</li>
                <li>/api/v1.0/stations</li>
                <li>/api/v1.0/tobs</li>
                <li>/api/v1.0/<start> and /api/v1.0/<start>/<end></li>
            </ul>
        </div>
    '''

# Return the query results as a dictionary, with date as the key and prcp as the value.
@app.route('/api/v1.0/precipitation')
def Prcp():
    session = Session(engine)
    
    prcp_q = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    order_by(Measurement.date).\
    all()
    
    dates = []
    for date, prcp in prcp_q:
        date_dict = {}
        date_dict['Date'] = date
        date_dict['Prcp'] = prcp
        dates.append(date_dict)
        
    return jsonify(dates)

# Return a JSON dictionary of stations from the dataset.
@app.route('/api/v1.0/stations')
def Stations():
    session = Session(engine)
    
    station_q = session.query(Station.name, Station.station).\
    all()
    
    stations = []
    for name, station in station_q:
        station_dict = {}
        station_dict['Name'] = name
        station_dict['Station'] = station
        stations.append(station_dict)

    return jsonify(stations)
    
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route('/api/v1.0/tobs')
def Tobs():
    session = Session(engine)
    
    tobs_q = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > '2016-08-23').\
    filter(Measurement.station == 'USC00519281').\
    all()
    
    tobs_year = []
    for date, tobs in tobs_q:
        tobs_dict = {}
        tobs_dict['Date'] = date
        tobs_dict['Tobs'] = tobs
        tobs_year.append(tobs_dict)
    
    return jsonify(tobs_year)

# Return a JSON list of the minimum, average, and max temperature after a given start date.
@app.route('/api/v1.0/<start>')
def Start(start):
    session = Session(engine)
    
    max_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()
    
    min_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()
    
    avg_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()
    
    temps = [max_temp, min_temp, avg_temp]
    return jsonify(temps)
    

# Return a JSON list of the minimum, average, and max temperature between a given start-end range (inclusive).
@app.route('/api/v1.0/<start>/<end>')
def End(start, end):
    session = Session(engine)
    
    max_temp = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()
    
    min_temp = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()
    
    avg_temp = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()
    
    temps = [max_temp, min_temp, avg_temp]
    return jsonify(temps)

if __name__ == "__main__":
    app.run(host ='127.0.0.1', port ='5000')