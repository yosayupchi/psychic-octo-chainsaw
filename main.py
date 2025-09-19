import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# 例: 特定の店舗のスロット一覧ページ
URL = "https://daidata.goraggio.com/100813/list?mode=psModelNameSearch&ballPrice=20.00&ps=S"

def fetch_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    data_list = []

    # 台情報を取得（HTML構造に依存するので要調整）
    rows = soup.select("table tr")  # 仮: テーブル内の行を取得
    for row in rows[1:]:  # ヘッダー除外
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if cols:
            data_list.append(cols)

    return data_list

def save_to_csv(data):
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"data_{today}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["台番号", "機種名", "BB", "RB", "差枚", "回転数"])  # 仮カラム
        writer.writerows(data)

    print(f"✅ {filename} に保存しました")

if __name__ == "__main__":
    data = fetch_data()
    save_to_csv(data)
