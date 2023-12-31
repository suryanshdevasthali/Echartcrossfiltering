import streamlit as st
from streamlit_echarts import st_echarts
from vega_datasets import data
import pandas as pd

def main():

    df = pd.read_csv(r"C:\Users\DELL\Downloads\us-employment.csv").set_index("month").drop(columns=["nonfarm_change"])
    means = df.mean(axis=0).map("{:.2f}".format)
    sums = df.sum(axis=1)

    bar_options = {
        "title": {"text": "Mean US employment this past decade"},
        "xAxis": {
            "type": "category",
            "axisTick": {"alignWithLabel": True},
            "data": means.index.values.tolist(),
        },
        "yAxis": {"type": "value"},
        "tooltip": {"trigger": "item"},
        "emphasis": {"itemStyle": {"color": "#a90000"}},
        "series": [{"data": means.tolist(), "type": "bar"}],
    }

    clicked_label = st_echarts(
        bar_options,
        events={"click": "function(params) {return params.name}"},
        height="500px",
        key="global",
    )

    line_options_1 = {
        "title": {"text": f"Breakdown US employment"},
        "xAxis": {
            "type": "category",
            "axisTick": {"alignWithLabel": True},
            "data": sums.index.values.tolist(),
        },
        "yAxis": {"type": "value"},
        "tooltip": {"trigger": "axis"},
        "itemStyle": {"color": "#a90000"},
        "lineStyle": {"color": "#a90000"},
        "series": [
            {
                "data": sums.tolist(),
                "type": "line",
                "smooth": True,
            }
        ],
    }

    if clicked_label is None:
        return st_echarts(line_options_1)

    filtered_df = df[clicked_label].sort_index()
    line_options = {
        "title": {"text": f"Breakdown US employment for {clicked_label}"},
        "xAxis": {
            "type": "category",
            "axisTick": {"alignWithLabel": True},
            "data": filtered_df.index.values.tolist(),
        },
        "yAxis": {"type": "value"},
        "tooltip": {"trigger": "axis"},
        "itemStyle": {"color": "#a90000"},
        "lineStyle": {"color": "#a90000"},
        "series": [
            {
                "data": filtered_df.tolist(),
                "type": "line",
                "smooth": True,
            }
        ],
    }
    clicked_label = st_echarts(line_options, key="detail")


if __name__ == "__main__":
    st.set_page_config(
        page_title="GARVIS Crossfiltering Implemetation DEMO", page_icon=":chart_with_upwards_trend:"
    )
    st.title("GARVIS Crossfiltering Implemetation DEMO")
    main()
    with st.sidebar:
        st.header("Echart Crossfiltering Example")

