import fastf1
import math
import pandas
import random
import matplotlib.pyplot as mpl

ChosenDriver = input("What driver would you like to choose in there 3 initial format:")
ChosenCircuit = input("What circuit would you like to choose: ")
ChosenYear = int(input("What year would you like this race to be: "))

print("FastF1 imported")

fastf1.Cache.enable_cache(r"C:\Users\Charlie\Documents\F1PythonProject\F1Cached")

print("Getting Sessions")

event = fastf1.get_event(ChosenYear, ChosenCircuit)

print(event)

fp1 = fastf1.get_session(ChosenYear, ChosenCircuit, "FP1")
fp2 = fastf1.get_session(ChosenYear, ChosenCircuit, "FP2")
fp3 = fastf1.get_session(ChosenYear, ChosenCircuit, "FP3")
quali = fastf1.get_session(ChosenYear, ChosenCircuit, "Q")
race = fastf1.get_session(ChosenYear, ChosenCircuit, "R")

print("Created Sessions")

fp1.load()
fp2.load()
fp3.load()
quali.load()
race.load()

print("Loaded Sessions")

def Format_Time(seconds):
    if math.isnan(seconds):
        return "NaN"
    minutes = int(seconds // 60)
    seconds = seconds % 60
    return f"{minutes}:{seconds:06.3f}"

def Format_LapNumber(Lapnumber):
   return f"{Lapnumber:2.0f}"

def Format_Difference(seconds):
    return f"{seconds:+.3f}"

def Get_QualiSession(Lap_number):
   if Lap_number in Q1["LapNumber"].values:
      return ("Q1")
   elif Lap_number in Q2["LapNumber"].values:
      return ("Q2")
   elif Lap_number in Q3["LapNumber"].values:
      return ("Q3")
   else:
      return ("Unknown")

def SimulateLaps1(Simulations):
    FastestSimulatedLap = None
    FastestSimulatedLapS1 = None
    FastestSimulatedLapS2 = None
    FastestSimulatedLapS3 = None
    for i in range(Simulations):
        S1 = random.gauss(AverageSector1, Sector1StandardDeviation)
        S2 = random.gauss(AverageSector2, Sector2StandardDeviation)
        S3 = random.gauss(AverageSector3, Sector3StandardDeviation)
        LapTime = S1 + S2 + S3
        if FastestSimulatedLap is None or LapTime < FastestSimulatedLap:
            FastestSimulatedLap = LapTime
            FastestSimulatedLapS1 = S1
            FastestSimulatedLapS2 = S2
            FastestSimulatedLapS3 = S3

    return ("Fastest simulated Lap was: " + Format_Time(FastestSimulatedLap) + " Fastest simulated S1: " + Format_Time(FastestSimulatedLapS1) + " Fastest simulated S2: " + Format_Time(FastestSimulatedLapS2) + " Fastest simulated S3: " + Format_Time(FastestSimulatedLapS3))

LapTimes = {
    "FP1LapTimes" : fp1,
    "FP2LapTimes" : fp2,
    "FP3LapTimes" : fp3,
    "QualiLapTimes" : quali,
    "RaceLapTimes" : race
}

for SessionName, Session in LapTimes.items():
    fastestLap = (
        Session.laps
        .pick_drivers(ChosenDriver)
        .pick_fastest()
    )

    laptime = (fastestLap["LapTime"]).total_seconds()
    LapNumber = (fastestLap["LapNumber"])
    print(ChosenDriver + "'s fastest lap: " + Format_Time(laptime) + " " + SessionName + " on lap " + Format_LapNumber(LapNumber))

FastestS1Time = None
FastestS2Time = None
FastestS3Time = None

for SessionName, Session in LapTimes.items():
    DriverLaps = (
        Session.laps
        .pick_drivers(ChosenDriver)
    )

    SessionSector1Time = DriverLaps["Sector1Time"].min().total_seconds()
    SessionSector2Time = DriverLaps["Sector2Time"].min().total_seconds()
    SessionSector3Time = DriverLaps["Sector3Time"].min().total_seconds()

    if (FastestS1Time is None or SessionSector1Time < FastestS1Time):
     FastestS1Time = SessionSector1Time
     S1Session = SessionName
     FastestS1Lap = DriverLaps.loc[DriverLaps["Sector1Time"].idxmin()]
     FastestS1LapNumber = (FastestS1Lap["LapNumber"])

    if (FastestS2Time is None or SessionSector2Time < FastestS2Time):
     FastestS2Time = SessionSector2Time
     S2Session = SessionName 
     FastestS2Lap = DriverLaps.loc[DriverLaps["Sector2Time"].idxmin()]
     FastestS2LapNumber = (FastestS2Lap["LapNumber"])

    if (FastestS3Time is None or SessionSector3Time < FastestS3Time):
     FastestS3Time = SessionSector3Time
     S3Session = SessionName
     FastestS3Lap = DriverLaps.loc[DriverLaps["Sector3Time"].idxmin()]
     FastestS3LapNumber = (FastestS3Lap["LapNumber"])

S1Time = FastestS1Time

print("The fastest S1 time by " + ChosenDriver  + " was: " + Format_Time(S1Time) + " in " + S1Session + " on lap " + Format_LapNumber(FastestS1LapNumber))

S2Time = FastestS2Time

print("The fastest S2 time by " + ChosenDriver + " was: " + Format_Time(S2Time) + " in " + S2Session + " on lap " + Format_LapNumber(FastestS2LapNumber))

S3Time = FastestS3Time
S3Minutes = int(S3Time // 60)
S3Seconds = S3Time % 60
print("The fastest S3 time by " + ChosenDriver + " was: " + Format_Time(S3Time) + " in " + S3Session + " on lap " + Format_LapNumber(FastestS3LapNumber))

TheoreticalFastestLap = FastestS1Time + FastestS2Time + FastestS3Time

print("The fastest theoretical time " + ChosenDriver + " could do is: " + Format_Time(TheoreticalFastestLap))

print("//////////////////////////////////////////////////////////////////////////////")
print("Lap: " + Format_LapNumber(FastestS1LapNumber) + " compared lap: " + Format_LapNumber(FastestS2LapNumber))
print("Sector 1: " , FastestS1Lap["Sector1Time"].total_seconds() - FastestS2Lap["Sector1Time"].total_seconds())
print("Sector 2: " , FastestS1Lap["Sector2Time"].total_seconds() - FastestS2Lap["Sector2Time"].total_seconds())
print("Sector 3: " , FastestS1Lap["Sector3Time"].total_seconds() - FastestS2Lap["Sector3Time"].total_seconds())
print("//////////////////////////////////////////////////////////////////////////////")

print("All of " + ChosenDriver + "pushing quali laps")
QualiDriverLaps = quali.laps.pick_drivers(ChosenDriver)
AverageQualiLap = QualiDriverLaps["LapTime"].dt.total_seconds().mean()

AccuratePushQualiLaps = QualiDriverLaps[
    (QualiDriverLaps["IsAccurate"] == True) & (QualiDriverLaps["LapTime"].dt.total_seconds() < AverageQualiLap)
].copy()
print(AccuratePushQualiLaps)

Q1, Q2, Q3 = quali.laps.split_qualifying_sessions()
AccuratePushQualiLaps["QualiSession"] = (AccuratePushQualiLaps["LapNumber"].apply(Get_QualiSession))
RawAccuratePushQualiLaps = AccuratePushQualiLaps.copy()

Q1Sector1Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q1"]["Sector1Time"].dt.total_seconds().mean())
Q1Sector2Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q1"]["Sector2Time"].dt.total_seconds().mean())
Q1Sector3Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q1"]["Sector3Time"].dt.total_seconds().mean())
Q1Average = Q1Sector1Average + Q1Sector2Average + Q1Sector3Average

Q2Sector1Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q2"]["Sector1Time"].dt.total_seconds().mean())
Q2Sector2Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q2"]["Sector2Time"].dt.total_seconds().mean())
Q2Sector3Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q2"]["Sector3Time"].dt.total_seconds().mean())

Q3Sector1Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q3"]["Sector1Time"].dt.total_seconds().mean())
Q3Sector2Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q3"]["Sector2Time"].dt.total_seconds().mean())
Q3Sector3Average = (AccuratePushQualiLaps[AccuratePushQualiLaps["QualiSession"] == "Q3"]["Sector3Time"].dt.total_seconds().mean())
Q3Average = Q3Sector1Average + Q3Sector2Average + Q3Sector3Average

S1Q1ToQ2 = Q2Sector1Average - Q1Sector1Average
S1Q2ToQ3 = Q3Sector1Average - Q2Sector1Average

S2Q1ToQ2 = Q2Sector2Average - Q1Sector2Average
S2Q2ToQ3 = Q3Sector2Average - Q2Sector2Average

S3Q1ToQ2 = Q2Sector3Average - Q1Sector3Average
S3Q2ToQ3 = Q3Sector3Average - Q2Sector3Average

AverageLapTime = AccuratePushQualiLaps["LapTime"].dt.total_seconds().mean()
AverageSector1 = AccuratePushQualiLaps["Sector1Time"].dt.total_seconds().mean()
AverageSector2 = AccuratePushQualiLaps["Sector2Time"].dt.total_seconds().mean()
AverageSector3 = AccuratePushQualiLaps["Sector3Time"].dt.total_seconds().mean()

Sector1StandardDeviation = AccuratePushQualiLaps["Sector1Time"].dt.total_seconds().std()
Sector2StandardDeviation = AccuratePushQualiLaps["Sector2Time"].dt.total_seconds().std()
Sector3StandardDeviation = AccuratePushQualiLaps["Sector3Time"].dt.total_seconds().std()

SpeedSectorAnalysis = AccuratePushQualiLaps[
    [
        "Sector1Time",
        "Sector2Time",
        "Sector3Time",
        "SpeedST",
        "SpeedI1",
        "SpeedI2",
        "SpeedFL"
    ]
].copy()

Correlation = SpeedSectorAnalysis.corr().loc[
    ["Sector1Time", "Sector2Time", "Sector3Time"],
    ["SpeedST", "SpeedI1", "SpeedI2", "SpeedFL"]
]

AccuratePushQualiLaps["S1Loss"] = (AccuratePushQualiLaps["Sector1Time"].dt.total_seconds() - AccuratePushQualiLaps["Sector1Time"].dt.total_seconds().min()).apply(Format_Time)
AccuratePushQualiLaps["S2Loss"] = (AccuratePushQualiLaps["Sector2Time"].dt.total_seconds() - AccuratePushQualiLaps["Sector2Time"].dt.total_seconds().min()).apply(Format_Time)
AccuratePushQualiLaps["S3Loss"] = (AccuratePushQualiLaps["Sector3Time"].dt.total_seconds() - AccuratePushQualiLaps["Sector3Time"].dt.total_seconds().min()).apply(Format_Time)

AccuratePushQualiLaps["DifferenceFromAverage"] = (AccuratePushQualiLaps["LapTime"].dt.total_seconds() - AverageLapTime).apply(Format_Difference)
AccuratePushQualiLaps["LossFromTheoretical"] = (AccuratePushQualiLaps["LapTime"].dt.total_seconds() - TheoreticalFastestLap).apply(Format_Time)
AccuratePushQualiLaps["LapTime"] = (AccuratePushQualiLaps["LapTime"].dt.total_seconds().apply(Format_Time))
AccuratePushQualiLaps["Sector1Time"] = (AccuratePushQualiLaps["Sector1Time"].dt.total_seconds().apply(Format_Time))
AccuratePushQualiLaps["Sector2Time"] = (AccuratePushQualiLaps["Sector2Time"].dt.total_seconds().apply(Format_Time))
AccuratePushQualiLaps["Sector3Time"] = (AccuratePushQualiLaps["Sector3Time"].dt.total_seconds().apply(Format_Time))
AccuratePushQualiLaps["LapNumber"] = (AccuratePushQualiLaps["LapNumber"].apply(Format_LapNumber))



print(
    AccuratePushQualiLaps[["LapNumber","LapTime","DifferenceFromAverage","LossFromTheoretical","Sector1Time","Sector2Time","Sector3Time","S1Loss","S2Loss","S3Loss","SpeedST","SpeedI1","SpeedI2","SpeedFL","QualiSession","Compound","TyreLife"]].to_string(index=False)
)

print("Average pushing lap time: " + Format_Time(AverageLapTime) + " compared to fastest theoretical time: " + Format_Time(TheoreticalFastestLap))
print("Average pushing sector 1 time: " + Format_Time(AverageSector1) + " compared to fastest time: " + Format_Time(S1Time))
print("Average pushing sector 2 time: " + Format_Time(AverageSector2) + " compared to fastest time: " + Format_Time(S2Time))
print("Average pushing sector 3 time: " + Format_Time(AverageSector3) + " compared to fastest time: " + Format_Time(S3Time))

print(f"Sector 1 standard deviation: ±{Sector1StandardDeviation:.3f}")
print(f"Sector 2 standard deviation: ±{Sector2StandardDeviation:.3f}")
print(f"Sector 3 standard deviation: ±{Sector3StandardDeviation:.3f}")

print("Q1 S1 Average:", Format_Time(Q1Sector1Average))
print("Q1 S2 Average:", Format_Time(Q1Sector2Average))
print("Q1 S3 Average:", Format_Time(Q1Sector3Average))

print("Q2 S1 Average:", Format_Time(Q2Sector1Average))
print("Q2 S2 Average:", Format_Time(Q2Sector2Average))
print("Q2 S3 Average:", Format_Time(Q2Sector3Average))

print("Q3 S1 Average:", Format_Time(Q3Sector1Average))
print("Q3 S2 Average:", Format_Time(Q3Sector2Average))
print("Q3 S3 Average:", Format_Time(Q3Sector3Average))

print("The difference in average lap time between Q1 and Q3 is: ", Format_Time(Q1Average-Q3Average))

print("The average loss between a pushing lap and theoretical best is: ", Format_Time(AverageLapTime - TheoreticalFastestLap))

print(Correlation)

print(SimulateLaps1(100))

print("//////////////////// QUALIFYING PROGRESSION ////////////////////")

print("S1 Q1 → Q2:", Format_Difference(S1Q1ToQ2))
print("S1 Q2 → Q3:", Format_Difference(S1Q2ToQ3))

print("S2 Q1 → Q2:", Format_Difference(S2Q1ToQ2))
print("S2 Q2 → Q3:", Format_Difference(S2Q2ToQ3))

print("S3 Q1 → Q2:", Format_Difference(S3Q1ToQ2))
print("S3 Q2 → Q3:", Format_Difference(S3Q2ToQ3))

Lap11 = QualiDriverLaps[QualiDriverLaps["LapNumber"] == 11].iloc[0]
Lap17 = QualiDriverLaps[QualiDriverLaps["LapNumber"] == 17].iloc[0]

Lap11Telemetry = Lap11.get_telemetry()
Lap17Telemetry = Lap17.get_telemetry()

print("//////////////////// TELEMETRY CHANNELS ////////////////////")
Lap11Telemetry = Lap11Telemetry.add_distance()
Lap17Telemetry = Lap17Telemetry.add_distance()

print("//////////////////// LAP 11 TELEMETRY ////////////////////")
print(Lap11Telemetry[["Distance", "Speed", "Throttle", "Brake", "nGear", "RPM", "DRS"]].head(20))

print("//////////////////// LAP 17 TELEMETRY ////////////////////")
print(Lap17Telemetry[["Distance", "Speed", "Throttle", "Brake", "nGear", "RPM", "DRS"]].head(20))

print("//////////////////// TRACK INFORMATION ////////////////////")

print("Track length:", Lap11Telemetry["Distance"].max())

print(
    Lap11Telemetry[
        ["Distance", "RelativeDistance", "X", "Y", "Z"]
    ]
)

CircuitInfo = quali.get_circuit_info()

print("//////////////////// T1 COMPARISON ////////////////////")

T1Distance = CircuitInfo.corners.loc[CircuitInfo.corners["Number"] == 1, "Distance"].iloc[0]

print("T1 distance:", T1Distance)

print("Lap 11 nearest T1:")
print(
    Lap11Telemetry.iloc[
        (Lap11Telemetry["Distance"] - T1Distance).abs().argmin()
    ][["Distance", "Speed", "Throttle", "Brake", "nGear"]]
)

print("Lap 17 nearest T1:")
print(
    Lap17Telemetry.iloc[
        (Lap17Telemetry["Distance"] - T1Distance).abs().argmin()
    ][["Distance", "Speed", "Throttle", "Brake", "nGear"]]
)

Corners = mpl.plot(CircuitInfo.corners.X,CircuitInfo.corners.Y,"o",color = "black")
for _, corner in CircuitInfo.corners.iterrows():
    mpl.annotate(corner.Number, (corner.X, corner.Y), xytext=(5, 5), textcoords="offset points")



Lap11Line = mpl.plot(Lap11Telemetry.X,Lap11Telemetry.Y)
Lap17Line = mpl.plot(Lap17Telemetry.X,Lap17Telemetry.Y,color = "red")
ax = mpl.gca()
ax.set_axis_off()
#mpl.show() can show when needed

print("//////////////////// L11 ET COMPARISON ////////////////////")
CornerComparrison = []

for _, Current in CircuitInfo.corners.iterrows():
    Lap11 = Lap11Telemetry.iloc[
        (Lap11Telemetry["Distance"] - Current["Distance"]).abs().argmin()
    ]

    Lap17 = Lap17Telemetry.iloc[
        (Lap17Telemetry["Distance"] - Current["Distance"]).abs().argmin()
    ]

    CornerComparrison.append({
        "Corner": Current["Number"],

        "Lap11Dist": Lap11["Distance"],
        "Lap17Dist": Lap17["Distance"],
        "DistanceDiff": Lap11["Distance"] - Lap17["Distance"],

        "Lap11Speed": Lap11["Speed"],
        "Lap17Speed": Lap17["Speed"],
        "SpeedDiff": Lap11["Speed"] - Lap17["Speed"],

        "Lap11Throttle": Lap11["Throttle"],
        "Lap17Throttle": Lap17["Throttle"],
        "ThrottleDiff": Lap11["Throttle"] - Lap17["Throttle"],

        "Lap11Gear": Lap11["nGear"],
        "Lap17Gear": Lap17["nGear"],
        "GearDiff": Lap11["nGear"] - Lap17["nGear"]
    })

CornerComparrison = pandas.DataFrame(CornerComparrison)

print(CornerComparrison.to_string(index=False))

CornerTimeComparrison = []

TotalLap11 = 0
TotalLap17 = 0

for _, Current in CircuitInfo.corners.iterrows():
    Lap11 = Lap11Telemetry.iloc[
        (Lap11Telemetry["Distance"] - Current["Distance"]).abs().argmin()
    ]

    Lap17 = Lap17Telemetry.iloc[
        (Lap17Telemetry["Distance"] - Current["Distance"]).abs().argmin()
    ]

    CornerTimeComparrison.append({
        "Corner": Current["Number"],

        "Lap11Time": Format_Time(Lap11["Time"].total_seconds()),
        "Lap17Time": Format_Time(Lap17["Time"].total_seconds()),

        "Lap11TimeC2C": Format_Time(Lap11["Time"].total_seconds() - TotalLap11),
        "Lap17TimeC2C": Format_Time(Lap17["Time"].total_seconds() - TotalLap17),

        "TimeDiff": Format_Difference((Lap17["Time"].total_seconds() - TotalLap17) - (Lap11["Time"].total_seconds() - TotalLap11))
    })

    TotalLap11 = Lap11["Time"].total_seconds()
    TotalLap17 = Lap17["Time"].total_seconds()

CornerTimeComparrison = pandas.DataFrame(CornerTimeComparrison)

print(CornerTimeComparrison.to_string(index=False))

QualiTimeComparrison = []
PreviousCornerTimes = {}

for _, CurrentCorner in CircuitInfo.corners.iterrows():
    for _, CurrentLap in RawAccuratePushQualiLaps.iterrows():
        Lap = CurrentLap
        LapTele = Lap.get_telemetry()
        
        indexOfCorner = LapTele["Distance"].searchsorted(CurrentCorner["Distance"])
        BeforeCorner = LapTele.iloc[indexOfCorner - 1]
        AfterCorner = LapTele.iloc[indexOfCorner]

        PercentageThrough = (CurrentCorner["Distance"] - BeforeCorner["Distance"]) / (AfterCorner["Distance"] - BeforeCorner["Distance"])
        
        CornerTime = BeforeCorner["Time"].total_seconds() + (PercentageThrough * (AfterCorner["Time"].total_seconds() - BeforeCorner["Time"].total_seconds()))
        CornerSpeed = (BeforeCorner["Speed"]+ PercentageThrough * (AfterCorner["Speed"] - BeforeCorner["Speed"]))
        CornerThrottle = (BeforeCorner["Throttle"]+ PercentageThrough * (AfterCorner["Throttle"] - BeforeCorner["Throttle"]))
        
        if CurrentCorner["Number"] == 1:
            PreviousCornerTimes[CurrentLap["LapNumber"]] = 0

        
        QualiTimeComparrison.append({
            "Corner": CurrentCorner["Number"],
            "Lap" : (CurrentLap["LapNumber"]),
            "LapTime" : Format_Time(CurrentLap["LapTime"].total_seconds()),
            "LapTimeC2C" : (CornerTime - PreviousCornerTimes[CurrentLap["LapNumber"]]),
            "ThrottleBeforeCorner" : BeforeCorner["Throttle"],
            "Throttle" : CornerThrottle,
            "ThrottleAfterCorner" : AfterCorner["Throttle"],
            "SpeedBeforeCorner" : BeforeCorner["Speed"],
            "Speed" : CornerSpeed,
            "SpeedAfterCorner" : AfterCorner["Speed"],
            "GearBeforeCorner" : BeforeCorner["nGear"],
            "GearAfterCorner" : AfterCorner["nGear"],
            "BrakeBeforeCorner" : BeforeCorner["Brake"],
            "BrakeAfterCorner" : AfterCorner["Brake"],
            "DifferenceBetween" : AfterCorner["Distance"] - BeforeCorner["Distance"]
        })

        PreviousCornerTimes[CurrentLap["LapNumber"]] = CornerTime

        if CurrentCorner["Number"] == CircuitInfo.corners["Number"].iloc[-1]:

            FinishTime = CurrentLap["LapTime"].total_seconds()
            LCTime = CornerTime

            LapStartTime = LapTele["Time"].iloc[0].total_seconds()

            TimeToLC = LCTime - LapStartTime
            ToFinish = FinishTime - TimeToLC

            ToFinishData = LapTele.iloc[-1]


            QualiTimeComparrison.append({
                "Corner": "ToFinish",
                "Distance": LapTele["Distance"].iloc[-1],
                "Lap": CurrentLap["LapNumber"],
                "LapTime": (CurrentLap["LapTime"]),
                "LapTimeC2C": ToFinish,
                "Throttle": ToFinishData["Throttle"],
                "Speed": ToFinishData["Speed"],
                "Gear": ToFinishData["nGear"],
                "Brake": ToFinishData["Brake"],
                "Relative": ToFinishData["RelativeDistance"]
            })

print("//////////////////// Quali Push Comparrison ////////////////////")
QualiTimeComparrison = pandas.DataFrame(QualiTimeComparrison)
print(QualiTimeComparrison.to_string(index=False))


C2CQualiAnalysis = []
C2CFastestQuali = []

for CornerNumber, CornerData in QualiTimeComparrison.groupby("Corner"):

    minimumC2C = CornerData["LapTimeC2C"].min()
    minC2CIndex = CornerData["LapTimeC2C"].idxmin()
    FastestData = CornerData.loc[minC2CIndex]
    for _, QualiLap in CornerData.iterrows():
        C2CQualiAnalysis.append({
            "Corner" : CornerNumber,
            "Lap" : QualiLap["Lap"],
            "Speed" : QualiLap["Speed"],
            "Throttle" : QualiLap["Throttle"],
            "DifferenceFromMin" : Format_Difference(QualiLap["LapTimeC2C"] - minimumC2C)
        })

    fastestLapSeenI = RawAccuratePushQualiLaps["LapTime"].idxmin()
    fastestLapSeen = RawAccuratePushQualiLaps.loc[fastestLapSeenI]
    fastestLapNumber = fastestLapSeen["LapNumber"]

    fastestLapC2C = QualiTimeComparrison[QualiTimeComparrison["Lap"] == fastestLapNumber]
    fastestLapSeen = fastestLapC2C[fastestLapC2C["Corner"] == FastestData["Corner"]].iloc[0]
    
    C2CFastestQuali.append({
        "Corner" : FastestData["Corner"],
        "Lap" : FastestData["Lap"],
        "FastestLap" : fastestLapNumber,
        "C2CTime" : FastestData["LapTimeC2C"],
        "C2CFastestLap" : fastestLapSeen["LapTimeC2C"],
        "C2CPercentageDiff" : (((fastestLapSeen["LapTimeC2C"] - FastestData["LapTimeC2C"]) / FastestData["LapTimeC2C"]) * 100),
        "C2CTimeDiff" : (fastestLapSeen["LapTimeC2C"] - FastestData["LapTimeC2C"]),
        "Speed" : FastestData["Speed"],
        "SpeedFastestLap" : fastestLapSeen["Speed"],
        "Throttle" : FastestData["Throttle"],
        "ThrottleFastestLap" : fastestLapSeen["Throttle"]
        })

print("//////////////////// Quali Push C2C Comparrison ////////////////////")
C2CQualiAnalysis = pandas.DataFrame(C2CQualiAnalysis)
print(C2CQualiAnalysis.to_string(index=False))

C2CFastestQuali = pandas.DataFrame(C2CFastestQuali)
print(C2CFastestQuali.to_string(index=False))

TheoreticalFastestLapWithC2C = 0

for _,C2CData in C2CFastestQuali.iterrows():
    TheoreticalFastestLapWithC2C += C2CData["C2CTime"]

print("Theoretical fastest looking at corner to corner: ", Format_Time(TheoreticalFastestLapWithC2C), " Actual fasted lap: ", Format_Time(fastestLapSeen["LapTime"].total_seconds()), " Percentage difference: ",(((fastestLapSeen["LapTime"].total_seconds() - TheoreticalFastestLapWithC2C) / TheoreticalFastestLapWithC2C) * 100), "%")
