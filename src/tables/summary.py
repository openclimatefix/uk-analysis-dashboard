from datetime import datetime, timedelta

import numpy as np
import streamlit as st


def make_recent_summary_stats(values, title: str = "Recent MAE"):
    day_before_yesterday, today, yesterday = get_recent_daily_values(values)

    with st.expander(title):
        st.subheader(title)
        t = datetime.today() - timedelta(days=1)
        t2 = datetime.today() - timedelta(days=2)
        t3 = datetime.today() - timedelta(days=3)
        col1, col2, col3 = st.columns([1, 1, 1])

        col1.metric(label=t3.strftime("%d/%m/%y"), value=day_before_yesterday)
        col2.metric(label=t2.strftime("%d/%m/%y"), value=yesterday)
        col3.metric(label=t.strftime("%d/%m/%y"), value=today)


def get_recent_daily_values(values):
    """
    Get the recent daily values from the metric values
    """
    if len(values) == 0:
        day_before_yesterday = None
        yesterday = None
        today = None
    elif len(values) == 1:
        day_before_yesterday = None
        yesterday = None
        today = values[len(values) - 1]
    elif len(values) == 2:
        day_before_yesterday = None
        yesterday = values[len(values) - 2]
        today = values[len(values) - 1]
    else:
        day_before_yesterday = values[len(values) - 3]
        yesterday = values[len(values) - 2]
        today = values[len(values) - 1]

    return day_before_yesterday, yesterday, today

def convert_minutes_to_hours(minutes):
    return round(minutes / 60, 1)

def make_forecast_horizon_table(all_forecast_horizons_df, y_plive_mae):
    st.subheader("Data - forecast horizon averaged")
    # get average MAE for each forecast horizon
    df_mae_horizon_mean = (
        all_forecast_horizons_df.groupby(["forecast_horizon"]).mean().reset_index()
    )
    df_mae_horizon_mean.rename(columns={"MAE": "mean"}, inplace=True)
    df_mae_horizon_std = all_forecast_horizons_df.groupby(["forecast_horizon"]).std().reset_index()
    df_mae_horizon_mean["std"] = df_mae_horizon_std["MAE"]
    # Convert forecast_horizon from minutes to hours
    df_mae_horizon_mean["forecast_horizon"] = df_mae_horizon_mean["forecast_horizon"].apply(convert_minutes_to_hours)
    pv_live_mae = np.round(np.mean(y_plive_mae), 2)
    st.write(f"PV LIVE Mae {pv_live_mae} MW (intraday - day after)")
    st.write(df_mae_horizon_mean)
