import numpy as np
from math import inf

from initial_values import INITIAL_CHARGE_EES, INITIAL_ELECTRICAL_DEMAND, INITIAL_PRODUCTION_PV, INITIAL_ELECTRICITY_COST, CAPACITY_EES, DELTA_T, MAXIMUM_CHARGING_POWER_EGEES

import gym
from gym import spaces

class EnergyManagementSystem(gym.Env):
    def __init__(self):
        super(EnergyManagementSystem, self).__init__()

        # action space: power flow from EG to EES {0.0,0.25,0.5,0.75,1.0}
        self.action_space = spaces.Discrete(5,)

        # state space: state of EES charge [kWh], PV production [kW], electrical demand (ED) [kW], cost of electricity from the grid [€/kWh]
        # define min and max state values
        self.observation_space = spaces.Box(
            low=np.array([0.0, 0.0, 0.0, 0.0]),high=np.array([10.0, inf, inf, inf]),dtype=float16
        )

        self.reset()
        self.timestep = 0

    def reset(self):
        self.E_EES = INITIAL_CHARGE_EES
        self.P_PV = INITIAL_PRODUCTION_PV
        self.P_ED = INITIAL_ELECTRICAL_DEMAND
        self.C_EG = INITIAL_ELECTRICITY_COST

        done = False # initialize the "end of episode"-flag to False


    def step(self, action):
        # execute one time step within the environment
        # action corresponds to a_EGEES, i.e. charging power from electrical grid (EG) to electrical energy storage (EES)
        # given as a fraction of the maximum charging power

        self.P_PVED = min(self.P_ED, self.P_PV)
        self.P_PVEES = min((CAPACITY_EES - self.E_EES) / DELTA_T, self.P_PV - self.P_PVED)
        self.P_PVEG = self.P_PV - self.P_PVEES - self.P_PVED
        self.P_EESED = min(self.P_ED - self.P_PVED, self.E_EES / DELTA_T)
        self.P_EGED = self.P_ED - self.P_PVED - self.P_EGED
        self.P_EGEES = min(self.action * MAXIMUM_CHARGING_POWER_EGEES, (CAPACITY_EES - self.E_EES) / DELTA_T)

        obs = [self.E_EES, self.P_PV, self.E_ED, self.C_EG]
        reward = - self.C_EG*(self.P_EGES + self.P_EGED)

        # if max #timesteps is reached (e.g. 24 with hourly resolution and one episode representing one day), set done = True
        if self.timestep == 24:
            done = True

        info = {} # no information to give

        self.timestep += 1

        return obs, reward, done, info



    def render(self, mode='human'):
        pass

