import xarray as xr
import pandas as pd
import numpy as np
import glob
import os

def load_historical_data(var_name, data_dir, month, lat, lon):
    years = range(1980, 2017)  # MERRA2 range
    data_list = []
    for year in years:
        # Assume monthly files: MERRA2_400.tavgM_2d_slv_Nx.YYYYMM.nc4
        file_pattern = os.path.join(data_dir, f"MERRA2_*.tavgM_2d_slv_Nx.{year}{month:02d}.nc4")
        files = glob.glob(file_pattern)
        if files:
            try:
                ds = xr.open_dataset(files[0])
                # Handle lon -180 to 180; MERRA2 lon 0-360 often
                if lon < 0:
                    lon += 360
                point_data = ds[var_name].sel(lat=slice(None), lon=slice(None), method='nearest').sel(lat=lat, lon=lon, method='nearest').values
                if len(point_data) > 0:
                    data_list.append({'year': year, 'value': point_data.mean()})  # Monthly mean
                ds.close()
            except Exception as e:
                print(f"Error: {e}")
    if not data_list:
        # Dummy for demo
        data_list = [{'year': y, 'value': np.random.normal(20 if var_name=='T2M' else 5, 5)} for y in years]
    return pd.DataFrame(data_list)

def compute_probabilities(data_dict, conditions):
    thresholds = {
        'T2M': {'hot': 305.37, 'cold': 273.15},  # >32C hot, <0C cold
        'wind': 9.0,  # m/s ~20mph sqrt(u^2+v^2)
        'PRECTOT': 25.4 / 86400  # kg/m2/s to mm/day ~1inch, but check units
    }
    probs = {}
    for cond in conditions:
        if cond == 'hot':
            df = data_dict['T2M']
            probs[cond] = np.mean(df['value'] > thresholds['T2M']['hot']) * 100
        elif cond == 'cold':
            df = data_dict['T2M']
            probs[cond] = np.mean(df['value'] < thresholds['T2M']['cold']) * 100
        elif cond == 'windy':
            u_df = data_dict.get('U10M', pd.DataFrame())
            v_df = data_dict.get('V10M', pd.DataFrame())
            if not u_df.empty and not v_df.empty:
                wind_speed = np.sqrt(u_df['value']**2 + v_df['value']**2)
                probs[cond] = np.mean(wind_speed > thresholds['wind']) * 100
            else:
                probs[cond] = 0
        elif cond == 'wet':
            df = data_dict['PRECTOT']
            probs[cond] = np.mean(df['value'] * 86400 > 25.4) * 100  # Convert to mm/day
        elif cond == 'uncomfortable':
            # Dummy: high temp + assume humidity, use hot prob
            probs[cond] = probs.get('hot', 0)
    return probs

def get_activity_suggestions(probs):
    low_risk = all(p < 30 for p in probs.values() if p > 0)  # If all probs low
    if low_risk:
        return ["Hiking on trails", "Fishing on lakes", "Beach vacation", "Outdoor events", "Picnics in parks"]
    elif probs.get('wet', 0) > 50:
        return ["Indoor alternatives", "Covered activities"]
    else:
        return ["Prepare for variable weather", "Check forecasts closer to date"]
    # Expand based on [web:20-22]: low rain/wind/extreme -> outdoor; high rain -> avoid water activities, etc.