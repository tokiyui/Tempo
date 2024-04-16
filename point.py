from skyfield.api import Star, Topos, load
from pytz import timezone
import numpy as np
 
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
osaka = earth + Topos('34.6914 N', '135.4917 E')
 
# 恒星・月の位置計算
star_app = osaka.at(t).observe(star).apparent()
moon_app = osaka.at(t).observe(moon).apparent()
 
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
    if pi > 0 :
        if eclipse == False:
            alt, az, d = osaka.at(ti).observe(moon).apparent().altaz()
            print('食の開始:', ti.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'), 'JST', '高度:', round(alt.degrees, 1), '方位:', round(az.degrees, 1))
            eclipse = True
    else :
        if eclipse == True:
            alt, az, d = osaka.at(ti).observe(moon).apparent().altaz()
            print('食の終了:', ti.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S'), 'JST', '高度:', round(alt.degrees, 1), '方位:', round(az.degrees, 1))
            eclipse = False
