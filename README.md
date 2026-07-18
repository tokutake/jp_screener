# jp_screener

日本株（日経平均株価 Nikkei 225 構成銘柄 225 社）の財務・指標を
yfinance で取得し、CSV に保存するスクリーナー。

## 構成

- `fetch_data.py` — Nikkei 225 構成銘柄 225 社の株価・時価総額・PER・PBR・
  配当利回り・売上/営業利益成長率などを取得し `japan_stocks.csv` に保存する。
- `japan_stocks.csv` — 取得済みのデータ（UTF-8 BOM 付き）。
- `app.py` — 取得データを表示・絞り込むためのアプリ（要実装確認）。

## 使い方

```bash
pip install yfinance pandas lxml
python3 fetch_data.py   # -> japan_stocks.csv を生成
```

## 取得項目

code, name, price, market_cap, per, pbr, div_yield,
revenue_growth, operating_profit_growth, sector

## 注意

- 構成銘柄リストは Wikipedia の「日経平均株価」ページから作成（2026-07 時点）。
- データソースは Yahoo Finance 経由の yfinance であり、精度は保証されない。
