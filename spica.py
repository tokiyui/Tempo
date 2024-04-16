from skyfield.api import Star, Topos, load
from pytz import timezone
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import matplotlib.dates as mdates
 
# 初期時刻設定
ts = load.timescale()
t = ts.utc(2024, 8, 10, 9, 0, range(0, 11000)) #2024-08-10:Spica食
tz = timezone('Asia/Tokyo')
# 月位置の読み込み
eph = load('de421.bsp')
moon, earth = eph['moon'], eph['earth']
# J2000.0なので最新の値にせよ
star = Star(ra_hours=(13, 25, 11.57937), dec_degrees=(-11, 9, 40.7501))
# 観測地設定(現時点では大阪)
#osaka = earth + Topos('34.6914 N', '135.4917 E')
# 観測地設定（範囲内の格子点生成）
grid_points = []
latitudes = np.arange(26, 42, 0.5)
longitudes = np.arange(120, 142, 0.5)
 
for lat in latitudes:
    for lon in longitudes:
        grid_points.append((lat, lon))
 
# 等値線図データの初期化
eclipse_start_data = np.empty((len(latitudes), len(longitudes)), dtype='datetime64[s]')
eclipse_start_data.fill(np.datetime64('NaT'))
eclipse_end_data = np.empty((len(latitudes), len(longitudes)), dtype='datetime64[s]')
eclipse_end_data.fill(np.datetime64('NaT'))
 
# 観測地設定と計算
for i, lat in enumerate(latitudes):
    for j, lon in enumerate(longitudes):
        print(lat, lon)
        observer_location = earth + Topos(f'{lat} N', f'{lon} E')
 
        # 恒星・月の位置計算
        star_app = observer_location.at(t).observe(star).apparent()
        moon_app = observer_location.at(t).observe(moon).apparent()
 
        # 月の視半径の計算
        r_moon = 1737
        moon_dist = moon_app.distance().km
        moon_rad = np.arctan2(r_moon, moon_dist)
 
        # 恒星・月の角距離の計算
        app_sep = star_app.separation_from(moon_app).radians
 
        # 上記角距離と月の視半径の差
        percent_eclipse = moon_rad - app_sep
 
        # 欠け始めと食の終わりの検索
        eclipse = False
        for ti, pi in zip(t, percent_eclipse):
            if pi > 0:
                if not eclipse:
                    alt, az, _ = observer_location.at(ti).observe(moon).apparent().altaz()
                    # UTC時間を使って変換
                    eclipse_start_data[i, j] = np.datetime64(ti.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S'))
                    print('食の開始:', ti.astimezone(tz).strftime('%H:%M:%S'), 'JST', '高度:', round(alt.degrees, 1), '方位:', round(az.degrees, 1))
                    eclipse = True
            else:
                if eclipse:
                    alt, az, _ = observer_location.at(ti).observe(moon).apparent().altaz()
                    # UTC時間を使って変換
                    eclipse_end_data[i, j] = np.datetime64(ti.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S'))
                    print('食の終了:', ti.astimezone(tz).strftime('%H:%M:%S'), 'JST', '高度:', round(alt.degrees, 1), '方位:', round(az.degrees, 1))
                    eclipse = False
 
# 2Dグリッドの作成
lon_grid, lat_grid = np.meshgrid(longitudes, latitudes)
 
# 文字列からdatetime64への変換
eclipse_start_data_array = np.array(eclipse_start_data, dtype='datetime64')
eclipse_end_data_array = np.array(eclipse_end_data, dtype='datetime64')
 
# プロット
plt.figure(figsize=(12, 8))
 
# 等値線図の作成
contour_set_s = plt.contour(lon_grid, lat_grid, mdates.date2num(eclipse_start_data_array), colors='black')
contour_set_e = plt.contour(lon_grid, lat_grid, mdates.date2num(eclipse_end_data_array), linestyles='dashed', colors='black')
 
# 等値線に時刻ラベルを追加
plt.clabel(contour_set_s, inline=True, fmt=lambda x: mdates.num2date(x).strftime('%H:%M'), fontsize=8, colors='black')
plt.clabel(contour_set_e, inline=True, fmt=lambda x: mdates.num2date(x).strftime('%H:%M'), fontsize=8, colors='black')
 
plt.title('Eclipse Start and End Time')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
