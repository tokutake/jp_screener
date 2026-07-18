"""日本株スクリーナー — データ取得モジュール

yfinance を使って日本の有名企業40社の財務・指標を取得し、
CSV (japan_stocks.csv) に保存する。
"""

import time
import pandas as pd
import yfinance as yf

# 日本の有名企業40社（コード + 名称）
COMPANY_LIST = [
    ("7203.T", "トヨタ自動車"), ("6758.T", "ソニーグループ"), ("9984.T", "ソフトバンクグループ"),
    ("6861.T", "キーエンス"), ("7974.T", "任天堂"), ("8306.T", "三菱UFJフィナンシャル"),
    ("8411.T", "みずほフィナンシャル"), ("8316.T", "三井住友フィナンシャル"),
    ("2914.T", "日本たばこ産業"), ("4519.T", "中外製薬"), ("4568.T", "第一三共"),
    ("7267.T", "本田技研工業"), ("8058.T", "三菱商事"), ("8031.T", "三井物産"),
    ("8053.T", "住友商事"), ("8002.T", "丸紅"), ("9432.T", "日本電信電話"),
    ("9433.T", "KDDI"), ("9434.T", "ソフトバンク(移動体)"), ("9983.T", "ファーストリテイリング"),
    ("6098.T", "リクルートホールディングス"), ("6367.T", "ダイキン工業"), ("6981.T", "村田製作所"),
    ("4063.T", "信越化学工業"), ("6902.T", "デンソー"), ("9020.T", "東日本旅客鉄道"),
    ("9021.T", "西日本旅客鉄道"), ("9022.T", "東海旅客鉄道"), ("6501.T", "日立製作所"),
    ("6752.T", "パナソニック"), ("7751.T", "キヤノン"), ("6762.T", "東京エレクトロン"),
    ("6971.T", "京セラ"), ("4502.T", "武田薬品工業"), ("4503.T", "アステラス製薬"),
    ("4661.T", "オリエンタルランド"), ("8802.T", "三菱地所"), ("8801.T", "三井不動産"),
    ("1925.T", "大和ハウス工業"), ("3382.T", "セブン&アイ・ホールディングス"),
    ("8050.T", "広島銀行"),
]


def fetch():
    rows = []
    for code, name in COMPANY_LIST:
        try:
            t = yf.Ticker(code)
            info = t.info
            fin = t.financials  # 損益計算書（列=決算期）

            # 成長率計算（最新 vs 1期前）
            def growth(metric):
                if metric in fin.index:
                    s = fin.loc[metric].dropna()
                    if len(s) >= 2:
                        return (s.iloc[0] / s.iloc[1] - 1) * 100
                return None

            rev_g = growth("Total Revenue")
            op_g = growth("Operating Income")

            rows.append({
                "code": code,
                "name": name,
                "price": info.get("currentPrice"),
                "market_cap": info.get("marketCap"),
                "per": info.get("trailingPE"),
                "pbr": info.get("priceToBook"),
                "div_yield": info.get("dividendYield"),
                "revenue_growth": rev_g,
                "operating_profit_growth": op_g,
                "sector": info.get("sector"),
            })
            print(f"OK  {name}: 売上成長={rev_g:.1f}% PER={info.get('trailingPE')}")
        except Exception as e:
            print(f"NG  {name}: {e}")
        time.sleep(0.3)  # 負荷軽減

    df = pd.DataFrame(rows)
    df.to_csv("japan_stocks.csv", index=False, encoding="utf-8-sig")
    print(f"\n保存完了: {len(df)} 社 -> japan_stocks.csv")
    return df


if __name__ == "__main__":
    fetch()
