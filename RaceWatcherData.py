import fastf1
import streamlit as st
import matplotlib.pyplot as mpl
import os
import pandas as pd
import math

os.makedirs("F1Cached", exist_ok=True)
fastf1.Cache.enable_cache("F1Cached")

def Load_Race(Year,GP):
    schedule = fastf1.get_event_schedule(Year)
    if GP.strip().isdigit():
        FindingRace = schedule[schedule["RoundNumber"] == int(GP.strip())]
    else:
        FindingRace = schedule[
        schedule["EventName"].str.contains(GP.strip(), case=False, na=False, regex=False)
        | schedule["Country"].str.contains(GP.strip(), case=False, na=False, regex=False)
    ]

    if not FindingRace.empty:
        RoundNumber = FindingRace["RoundNumber"].iloc[0]
        race = fastf1.get_session(Year, int(RoundNumber), "R")
        race.load()
        FirstLaps = race.laps[race.laps["LapNumber"] == 1]
        RaceStartTime = FirstLaps["LapStartTime"].min()
        
        DriverData = {}

        for driver in race.drivers:
            position_data = race.pos_data[driver]
            DriverData[driver] = position_data

        return DriverData,RaceStartTime
    
    else:
        st.error("Grand Prix not found, try again")
        return False



def Get_Driver_Position(position_data, CurrentTime):
    BeforeClosest = position_data[position_data["SessionTime"] <= CurrentTime].iloc[-1]
    AfterClosest = position_data[position_data["SessionTime"] > CurrentTime].iloc[0]

    BeforeX = BeforeClosest["X"]
    BeforeY = BeforeClosest["Y"]
    BeforeTime = BeforeClosest["SessionTime"]

    AfterX = AfterClosest["X"]
    AfterY = AfterClosest["Y"]
    AfterTime = AfterClosest["SessionTime"]

    PercentageThrough = (CurrentTime - BeforeTime) / (AfterTime - BeforeTime)
    x = BeforeX + (AfterX - BeforeX) * PercentageThrough
    y = BeforeY + (AfterY - BeforeY) * PercentageThrough

    return x, y
