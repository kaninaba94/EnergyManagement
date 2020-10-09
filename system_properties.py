import numpy as np
import gym

# electricity demand 24 hours in kW
ED = np.array([0,0,0,0,0,0,0,0,5,1,1,1,1,1,1,1,1,1,1,1,3,4,2,2])

# PV production 24 hours in kW
PV = np.array([0,0,0,0,0,0,0,0,0,0,1,2,4,4,4,1,1,0,0,1,1,0,0,0])

# price of electricity 24 hours in €/kWh
priceE = np.array([0.3,0.3,0.3,0.3,0.3,0.2,0.2,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.3,0.3,0.3,0.3,0.3,0.3,0.3])

# EES capacity in kWh
capacityEES = 10
