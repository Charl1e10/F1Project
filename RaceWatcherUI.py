import streamlit as st
import matplotlib.pyplot as mpl
import RaceWatcherData
import time
import pandas as pd

st.markdown("""
<style>
    .stMainBlockContainer {
        padding-top: 2rem;
    }

    .stButton {
    margin-top: 28px;
    }
</style>

<h1 style="color: #8A2BE2; margin-top: 0rem; margin-left: -4rem; font-weight: bold;">
    Race Watcher
</h1>
"""
, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
if "result" not in st.session_state:
    st.session_state.result = False

with col1:
    Year = st.number_input(
        "Year",
        min_value=2018,
        max_value=2026,
        value=2026,
        step=1
    )

with col2:
    GrandPrix = st.text_input(
        "Grand Prix",
        placeholder="Race Number, Country, Track Name"
    )

with col3:
    if st.button("Search"):
        st.session_state.result = RaceWatcherData.Load_Race(Year,GrandPrix)

if st.session_state.result is not False:
    DriverData, RaceStartTime = st.session_state.result
    first_driver = next(iter(DriverData))
    first_lap = DriverData[first_driver]
    x = first_lap["X"]
    y = first_lap["Y"]
    track, ax = mpl.subplots(figsize=(10, 6))
    ax.plot(x, y, color="grey", linewidth=8)
    ax.set_aspect("equal")
    ax.axis("off")
    track.patch.set_alpha(0)
    track.patch.set_facecolor("#1E1230")
    ax.set_facecolor("#1E1230")
    st.write("Drivers:", len(DriverData))

    markers = {}
    StartClock = time.perf_counter()
    AnimationTime = RaceStartTime
    RaceDuration = pd.Timedelta(0)

    for position_data in DriverData.values():
        DriverDuration = position_data["SessionTime"].max()

        if DriverDuration > RaceDuration:
            RaceDuration = DriverDuration

    for driver, position_data in DriverData.items():
        ValidPositions = position_data[(position_data["X"] != 0) | (position_data["Y"] != 0)]   

        if not ValidPositions.empty:
            marker, = ax.plot(
            ValidPositions["X"].iloc[0],
            ValidPositions["Y"].iloc[0],
            marker="o",
            color="red",
            markersize=4,
            linestyle="None",
            zorder=10
            )

            markers[driver] = marker


    update = st.empty()
    RaceTimer = st.empty()
    while AnimationTime < RaceDuration:
        AnimationTime = RaceStartTime + pd.Timedelta(seconds=time.perf_counter() - StartClock)
        for driver, position_data in DriverData.items():
            if driver in markers:
                x,y = RaceWatcherData.Get_Driver_Position(position_data,AnimationTime)

                markers[driver].set_data([x], [y])

        FrameStart = time.perf_counter()
        update.pyplot(track, width="stretch")
        print("Seconds per frame:", time.perf_counter() - FrameStart)
        RaceTimer.markdown(f"Race Time: {AnimationTime}")



