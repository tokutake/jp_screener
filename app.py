"""日本株スクリーナー — Streamlit Webアプリ

使い方:
    cd jp_screener
    streamlit run app.py
"""

import pandas as pd
import streamlit as st

CSV_PATH = "japan_stocks.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
    # 数値列を float に
    for c in ["price", "market_cap", "per", "pbr", "div_yield",
              "revenue_growth", "operating_profit_growth"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def main():
    st.set_page_config(page_title="日本株スクリーナー", layout="wide")
    st.title("🇯🇵 日本株スクリーナー")
    st.caption("売上・利益の成長率 × 割安さ（PER/PBR）で絞り込み")

    df = load_data()

    with st.sidebar:
        st.header("🔧 絞り込み条件")

        min_rev = st.slider("売上成長率 以上 (%)", -20.0, 100.0, 0.0, 0.5)
        min_op = st.slider("営業利益成長率 以上 (%)", -20.0, 100.0, 0.0, 0.5)
        max_per = st.slider("PER 以下", 0.0, 60.0, 60.0, 1.0)
        max_pbr = st.slider("PBR 以下", 0.0, 10.0, 10.0, 0.1)

        st.divider()
        sort_key = st.selectbox(
            "並び替え",
            ["revenue_growth", "operating_profit_growth", "per", "pbr"],
            format_func=lambda x: {
                "revenue_growth": "売上成長率",
                "operating_profit_growth": "営業利益成長率",
                "per": "PER（低い順）",
                "pbr": "PBR（低い順）",
            }[x],
        )
        use_asc = sort_key in ("per", "pbr")

    # フィルタリング
    mask = (
        (df["revenue_growth"] >= min_rev)
        & (df["operating_profit_growth"] >= min_op)
        & (df["per"].isna() | (df["per"] <= max_per))
        & (df["pbr"].isna() | (df["pbr"] <= max_pbr))
    )
    result = df[mask].sort_values(sort_key, ascending=use_asc)

    st.subheader(f"📋 該当: {len(result)} 社 / {len(df)} 社")

    if result.empty:
        st.warning("条件に合う銘柄がありません。緩めてみてください。")
        return

    # 表示用に整形
    show = result.copy()
    show["時価総額(兆円)"] = (show["market_cap"] / 1e12).round(2)
    show["売上成長(%)"] = show["revenue_growth"].round(1)
    show["営業益成長(%)"] = show["operating_profit_growth"].round(1)
    show["PER"] = show["per"].round(1)
    show["PBR"] = show["pbr"].round(2)
    show["配当利回(%)"] = (show["div_yield"] * 100).round(2)

    cols = ["code", "name", "price", "時価総額(兆円)",
            "売上成長(%)", "営業益成長(%)", "PER", "PBR", "配当利回(%)"]
    view = show[cols].rename(columns={"code": "コード", "name": "企業名", "price": "株価"})

    st.dataframe(view, use_container_width=True, hide_index=True)

    csv = view.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button("📥 CSVダウンロード", csv, "filtered_stocks.csv", "text/csv")


if __name__ == "__main__":
    main()
