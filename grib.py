import os
import sys
import argparse
from datetime import datetime, timedelta
import pygrib
import pandas as pd
import numpy as np

def extract_grib_data(init_time, lat, lon):
    base_url = "http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/"
    year = init_time[:4]
    month = init_time[4:6]
    day = init_time[6:8]
    hour = init_time[8:10]
   
    file_names = [
        f"Z__C_RJTD_{year}{month}{day}{hour}0000_GSM_GPV_Rjp_Gll0p1deg_L-pall_FD0000-0100_grib2.bin",
        f"Z__C_RJTD_{year}{month}{day}{hour}0000_GSM_GPV_Rjp_Gll0p1deg_L-pall_FD0103-0200_grib2.bin",
        f"Z__C_RJTD_{year}{month}{day}{hour}0000_GSM_GPV_Rjp_Gll0p1deg_L-pall_FD0203-0300_grib2.bin",
        f"Z__C_RJTD_{year}{month}{day}{hour}0000_GSM_GPV_Rjp_Gll0p1deg_L-pall_FD0303-0400_grib2.bin"
    ]
   
    data_dir = os.path.join(os.getcwd(), "gpv_data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    data = {'Time': [], 'Level': [], 'Parameter': [], 'Value': []}
 
    for file_name in file_names:
        file_path = os.path.join(data_dir, file_name)
        url = base_url + year + "/" + month + "/" + day + "/" + file_name
        if not os.path.exists(file_path):
            os.system(f"wget -O {file_path} {url}")
 
        grbs = pygrib.open(file_path)
        for grb in grbs:
            lats, lons = grb.latlons()
            lat_diff = np.abs(lats - lat)
            lon_diff = np.abs(lons - lon)
            lat_index = np.unravel_index(lat_diff.argmin(), lat_diff.shape)[0]
            lon_index = np.unravel_index(lon_diff.argmin(), lon_diff.shape)[1]
            print(lon_index,lat_index)
            if lat_index >= lats.shape[0] or lon_index >= lons.shape[1]:
                print(f"Warning: Latitude or longitude {lat}, {lon} is out of bounds for file {file_name}")
                continue
            value = grb.values[lat_index, lon_index]
            data['Time'].append(grb.validDate)
            data['Level'].append(grb.level)
            data['Parameter'].append(grb.parameterName)
            data['Value'].append(value)            
        grbs.close()
 
    df = pd.DataFrame(data)
 
    csv_file = os.path.join(data_dir, f"GSM_GPV_data_{init_time}_{lat}_{lon}.csv")
    df.to_csv(csv_file, index=False)

if __name__ == "__main__":
    #parser = argparse.ArgumentParser(description='Extract GSM GPV data for a specific location and time.')
    #parser.add_argument('--init_time', type=str, default='2024042200', help='Initial time in YYYYMMDDHH format.')
    #parser.add_argument('--lat', type=float, default=40, help='Latitude of the location.')
    #parser.add_argument('--lon', type=float, default=140, help='Longitude of the location.')
 
    #args = parser.parse_args()  # Read command line arguments
 
    #extract_grib_data(args.init_time, args.lat, args.lon)
    extract_grib_data('2024042200', 35.692, 139.75)
