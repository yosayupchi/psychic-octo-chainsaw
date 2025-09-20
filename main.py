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
# 勝率予測を表示する関数
def predict_win_rate(data_list):
    if not data_list:
        print("データがありません")
        return

    # 例: 出玉や大当たり回数を使った簡易スコア
    scores = []
    for row in data_list:
        try:
            atari = int(row[1])   # 2列目を大当たり回数と仮定
            dema = int(row[2])    # 3列目を出玉と仮定
            score = atari * 2 + dema / 1000
            scores.append((row, score))
        except:
            continue

    if not scores:
        print("スコアを計算できませんでした")
        return

    # スコア順に並べ替え
    scores.sort(key=lambda x: x[1], reverse=True)

    print("勝率予測ランキング (上位5台):")
    for i, (row, score) in enumerate(scores[:5], 1):
        print(f"{i}位: 台情報={row}, スコア={score:.2f}")


if __name__ == "__main__":
    data = fetch_data()
    save_to_csv(data)
    predict_win_rate(data)
