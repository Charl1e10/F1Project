import math
# Qualifying minimum formula: 726 kg + nominal tyre mass
CarMass = 770 #Kg

#Power
EnginePower = 750000 #W

# Aerodynamics
DragCornerMode = 1.0 # Drag coefficient x frontal area (m^2)
DragStraightMode  = 0.8 # Lower drag with straight line aero
DownforceCoefficientArea = 4.0 # Aero parameter for car (m^2) * Downforce Coefficient

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
TargetSpeed = 10 #m/s 30 is around 108 km/h

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
GripForce = TyreGripCo * CarMass * G # Force = Coefficient of Friction * Downward Force # Downward Force = Mass * Gravity will need to add downforce later
CrossSpeed = EnginePower / GripForce # Velocity = Power / Force # Allows me too see 
Downforce = 0.5 * AirDensity * DownforceCoefficientArea * StartingSpeed ** 2 # FDownforce = 0.5 * Air Density * Downforce Coefficient * Refrence Area * velocity^2
MaxGripForce = TyreGripCo * ((CarMass * G) + Downforce) # Force = Coefficient of Friction * Downward Force # Downward Force = Mass * Gravity + Downforce #as its also adding force downwards
BrakingDistance = (TargetSpeed**2 - StartingSpeed**2) / (2 * -MaxBraking) # Breaking Distance = (End Velocity^2 - Starting Velocity^2) / (2 * Acceleration) #The acceleration will be negative


SectionDistance = 1253.5 # distance variable for testing c18 -> c1 on suzuka

while TotalDistance < SectionDistance:
    DistanceToCorner = SectionDistance - TotalDistance
    MaxSpeed = (TargetSpeed**2 + 2 * MaxBraking * DistanceToCorner)**0.5 #Final Velocity = Square Root(Initial Velocity^2 * Acceleration * Distance Travelled)
    if StartingSpeed > MaxSpeed:
        print("Braking needed", DistanceToCorner,MaxSpeed)
    else:
        print("Accelerating possible", DistanceToCorner,MaxSpeed)
    DrivingForce = EnginePower / StartingSpeed
    Downforce = 0.5 * AirDensity * DownforceCoefficientArea * StartingSpeed ** 2
    MaxGripForce = TyreGripCo * ((CarMass * G) + Downforce)
    GripLimitedForce = min(DrivingForce, MaxGripForce)
    DragForce = 0.5 * AirDensity * DragStraightMode * StartingSpeed ** 2
    netForce = GripLimitedForce - DragForce
    Acceleration = netForce / CarMass
    DistanceTravelled = StartingSpeed * STime + 0.5 * Acceleration * STime ** 2
    TotalDistance = TotalDistance + DistanceTravelled
    StartingSpeed = StartingSpeed + Acceleration * STime
    TotalTime += STime

StraightEndSpeed = StartingSpeed
BrakingDistance = (TargetSpeed**2 - StraightEndSpeed**2) / (2 * -MaxBraking)
BrakingStartDistance = SectionDistance - BrakingDistance

print(TotalTime,StartingSpeed,GripLimitedForce,DragForce,Acceleration)
print(BrakingDistance,BrakingStartDistance)



