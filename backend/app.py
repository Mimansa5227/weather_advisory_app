from flask import Flask, request, jsonify
from flask_cors import CORS
import xarray as xr
import pandas as pd
import numpy as np
import os
from utils.data_processor import load_historical_data, compute_probabilities, get_activity_suggestions
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow React frontend

DATA_DIR = 'data/'  # Adjust to your MERRA2 files path
# Assume files like M2T1NXSLV_5.12.4.YYYYMMDD.nc4 or monthly; for demo, monthly tavgM_2d_slv_Nx.YYYYMM.nc4
# Variables: T2M (K), U10M/V10M (m/s), PRECTOT (kg/m^2/s, convert to mm/day *86400)

@app.route('/api/query', methods=['GET'])
def query_weather():
    lat = float(request.args.get('lat', 40.7128))
    lon = float(request.args.get('lon', -74.0060))
    month = int(request.args.get('month', 4))
    day = int(request.args.get('day', 15))  # For day-of-year approx, use monthly for simplicity
    conditions = request.args.get('conditions', '').split(',')  # e.g., 'hot,cold,windy,wet,uncomfortable'

    # Load data for relevant vars
    vars_to_load = []
    if 'hot' in conditions or 'cold' in conditions or 'uncomfortable' in conditions:
        vars_to_load.extend(['T2M'])
    if 'windy' in conditions:
        vars_to_load.extend(['U10M', 'V10M'])
    if 'wet' in conditions:
        vars_to_load.append('PRECTOT')

    data_dict = {}
    for var in set(vars_to_load):
        df = load_historical_data(var, DATA_DIR, month, lat, lon)
        data_dict[var] = df

    # Compute probs
    probs = compute_probabilities(data_dict, conditions)

    # Suggestions
    suggestions = get_activity_suggestions(probs)

    # Export data
    export_data = {'probs': probs, 'suggestions': suggestions, 'mean_values': {k: v['value'].mean() for k, v in data_dict.items()}}

    return jsonify(export_data)

@app.route('/api/download/<condition>', methods=['GET'])
def download_csv(condition):
    # Implement CSV generation based on query params similar to above
    # For now, placeholder
    return jsonify({'error': 'Implement CSV export'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)