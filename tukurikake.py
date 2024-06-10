import pandas as pd
import matplotlib.pyplot as plt
 
# CSVファイルのパス
csv_file = 'MSM_2024052212_44132.csv'
 
# CSVファイルの読み込み
def load_csv_data(file_path):
    df = pd.read_csv(file_path, delimiter=',', header=0)
    df['Time'] = pd.to_datetime(df['Time'])
    return df
 
# 時間範囲と高度の指定
start_time = pd.Timestamp('2024-05-22 12:00:00')
end_time = pd.Timestamp('2024-05-23 12:00:00')
altitudes = [1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300]
 
# CSVデータを都度読み込んで処理
def process_csv_data(file_path):
    df = load_csv_data(file_path)
 
    # 指定した時間範囲と高度のデータを抽出
    selected_data = df[(df['Time'] >= start_time) & (df['Time'] <= end_time) & (df['Level'].isin(altitudes)) & (df['Parameter'] == 'Temperature')]
 
    # 時間ごとの気温データの辞書を作成
    temperature_data = {}
    for time in selected_data['Time'].unique():
        temp = selected_data[selected_data['Time'] == time]
        for altitude in altitudes:
            if altitude not in temperature_data:
                temperature_data[altitude] = []
            temperature_data[altitude].append(temp[temp['Level'] == altitude]['Value'].values[0])
 
    # 等温線の描画
    plt.figure(figsize=(10, 6))
    for altitude in altitudes:
        plt.plot(selected_data['Time'].unique(), [altitude] * len(selected_data['Time'].unique()), '--k', linewidth=0.5)
 
    # 気温データのプロット
    for altitude in altitudes:
        plt.scatter(selected_data['Time'].unique(), [altitude] * len(selected_data['Time'].unique()), c=temperature_data[altitude], cmap='coolwarm', vmin=min(selected_data['Value']), vmax=max(selected_data['Value']), s=50)
 
    # カラーバーの追加
    cbar = plt.colorbar()
    cbar.set_label('Temperature (°C)')
 
    # 軸ラベルやタイトルを設定
    plt.xlabel('Time')
    plt.ylabel('Altitude (hPa)')
    plt.title('Temperature at Different Altitudes')
 
    # グリッドを表示
    plt.grid(visible=True)
 
    # プロットを表示
    plt.show()
 
# CSVデータの処理を実行
process_csv_data(csv_file)
