import math
# Qualifying minimum formula: 726 kg + nominal tyre mass
CarMass = 770 #Kg

#Power
EnginePower = 750000 #W

# Aerodynamics
DragCornerMode = 1.0 # Drag coefficient x frontal area (m^2)
DragStraightMode  = 0.8 # Lower drag with straight line aero

# Air
# from the session weather and altitude
AirDensity = 1.225 #Kg/meters^3

# Tyres
TyreGripCo = 1.5

# Braking
# Temporary for maximum braking deceleration
MaxBraking = 45.0 #meters^2/s

# Simulation
STime = 0.02 #how many times it runs in a second
StartingSpeed = 20.0 #starting speed mps

#CalculationVariables
TotalDistance = 0
TotalTime = 0
G = 9.81 #gravity


F1_TEAMS = {
    "Mercedes": {"power_unit": "Mercedes",},
    "Ferrari": {"power_unit": "Ferrari",},
    "McLaren": {"power_unit": "Mercedes",},
    "Red Bull Racing": {"power_unit": "Red Bull Ford",},
    "Racing Bulls": {"power_unit": "Red Bull Ford",},
    "Alpine": {"power_unit": "Mercedes",},
    "Haas": {"power_unit": "Ferrari",},
    "Audi": {"power_unit": "Audi",},
    "Williams": {"power_unit": "Mercedes",},
    "Aston Martin": {"power_unit": "Honda",},
    "Cadillac": {"power_unit": "Ferrari",},
}

#Equations
DrivingForce = EnginePower / StartingSpeed # Force = Power / Velocity
DragForce = 0.5 * AirDensity * DragStraightMode * StartingSpeed ** 2 # Drag Force = 0.5 * Air Density * Velocity^2 * Drag Coefficient * Frontal Cross Sectional Area
netForce = DrivingForce - DragForce # Forward force - backward force
Acceleration = netForce / CarMass # Acceleration = Force / Mass # Newtons second law
NewSpeed = StartingSpeed + Acceleration * STime # New Velocity = Old Velocity + Acceleration * Change in Time
#Acceleration must be constant for distance
DistanceTravelled = StartingSpeed * STime + 0.5 * Acceleration * STime ** 2 # Change in Distance = Starting Velocity * Change in Time + 0.5 * Acceleration * Change in Time^2
TotalDistance = TotalDistance + DistanceTravelled #New Distance = Old Distance + Change in Distance
TyreForce = TyreGripCo * CarMass * G # Force = Coefficient of Friction * Downward Force # Downward Force = Mass * Gravity will need to add downforce later
CrossSpeed = EnginePower / TyreForce # Velocity = Power / Force # Allows me too see 

SectionDistance = 1253.5 # distance variable for testing c18 -> c1 on suzuka

while TotalDistance < SectionDistance:
    DrivingForce = EnginePower / StartingSpeed
    TyreForce = TyreGripCo * CarMass * G
    GripLimitedForce = min(DrivingForce, TyreForce)
    DragForce = 0.5 * AirDensity * DragStraightMode * StartingSpeed ** 2
    netForce = GripLimitedForce - DragForce
    Acceleration = netForce / CarMass
    DistanceTravelled = StartingSpeed * STime + 0.5 * Acceleration * STime ** 2
    TotalDistance = TotalDistance + DistanceTravelled
    StartingSpeed = StartingSpeed + Acceleration * STime
    TotalTime += STime

print(TotalTime,StartingSpeed,GripLimitedForce,DragForce,Acceleration)

