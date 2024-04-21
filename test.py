import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_tweet_content(url):
    # アーカイブURLを追加したURLを作成
    archive_url = f"https://web.archive.org/web/20210305013649/{url}"
    
    # リクエストのリトライとタイムアウト設定
    retries = 3
    time.sleep(15) 
    for _ in range(retries):
        try:
            response = requests.get(archive_url, timeout=10)  # タイムアウトを10秒に設定
            response.raise_for_status()  # HTTPエラーチェック
            break  # 成功した場合はループを抜ける
        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {e}")
            
    else:
        # リトライが失敗した場合
        print(f"Failed to access URL after {retries} retries.")
        return None
    
    # 正常なレスポンスが得られた場合は解析
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find("meta", property="og:description")
    if meta_tag:
        tweet_text = meta_tag['content']
        return tweet_text
    else:
        return None

def main():
    input_file = 'doya.txt'
    output_file = 'tweet.csv'
    
    # CSVファイルを書き込みモードでオープン
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['URL', 'Tweet Content'])
        
        # test.txtからURLを読み込み、各URLに対してスクレイピングを実行
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                url = line.strip()  # 改行を除去
                tweet_content = scrape_tweet_content(url)
                
                if tweet_content:
                    csv_writer.writerow([url, tweet_content])
                else:
                    csv_writer.writerow([url, 'Failed to retrieve tweet content'])
    
    print(f"Scraping completed. Results saved to {output_file}")

if __name__ == "__main__":
    main()

