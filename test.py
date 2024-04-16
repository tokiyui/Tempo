import pygrib
import matplotlib.pyplot as plt

grbs = pygrib.open('TL479_surf.grib2')
print(grbs[1])
'''
# GRIBファイルからデータを読み込む
data_surf = pygrib.open('TL479_surf.grib2')
data_land = pygrib.open('TL479_land.grib2')

# データを取得
surface_data = data_surf[1].values  # 1つ目のメッセージを取得
land_data = data_land[1].values      # 1つ目のメッセージを取得

# 描画領域を指定
lon_start, lon_end = 0, 360
lat_start, lat_end = -90, 90

print(len(surface_data[0]),len(surface_data[1]))
print(

# 描画領域にデータを切り出す
lon_slice = slice(int((lon_start) * len(surface_data[0]) / 360), int((lon_end) * len(surface_data[0]) / 360))
lat_slice = slice(int((lat_start) * len(surface_data[0]) / 180), int((lat_end) * len(surface_data[0]) / 180))

print(lon_slice)
surface_data_subregion = surface_data[lon_slice, lat_slice]
land_data_subregion = land_data[lon_slice, lat_slice]

# データをプロット
plt.figure(figsize=(8, 6))
plt.imshow(surface_data_subregion, cmap='jet', extent=[lon_start, lon_end, lat_start, lat_end])
plt.title('Surface Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(label='Value')
plt.grid(True)
plt.savefig('surface_data_subregion_plot.png')
plt.close()

plt.figure(figsize=(8, 6))
plt.imshow(land_data_subregion, cmap='terrain', extent=[lon_start, lon_end, lat_start, lat_end])
plt.title('Land Data')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.colorbar(label='Value')
plt.grid(True)
plt.savefig('land_data_subregion_plot.png')
plt.close()

'''
