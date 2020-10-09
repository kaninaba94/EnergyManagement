import numpy as np
from math import inf

from initial_values import INITIAL_CHARGE_EES, INITIAL_ELECTRICAL_DEMAND, INITIAL_PRODUCTION_PV, INITIAL_ELECTRICITY_COST
from constants import CAPACITY_EES, DELTA_T, MAXIMUM_CHARGING_POWER_EGEES
from temporal_profiles import PV_PRODUCTION, ELECTRICAL_DEMAND, COST_OF_ELECTRICITY

import gym
from gym import spaces

class EnergyManagementSystem(gym.Env):
    def __init__(self):
        super(EnergyManagementSystem, self).__init__()
        # action space: power flow from EG to EES {0.0,0.25,0.5,0.75,1.0}
        self.action_space = spaces.Discrete(5,)

        # state space: state of EES charge [kWh], PV production [kW], electrical demand (ED) [kW], cost of electricity from the grid [€/kWh]
        # define min and max state values
        # self.observation_space = spaces.Box(
            # low=np.array([0.0, 0.0, 0.0, 0.0]),high=np.array([10.0, inf, inf, inf]),dtype=np.float16
        # )

        self.reset()
        self.timestep = 0

    def reset(self):
        # observed state variables
        self.E_EES = INITIAL_CHARGE_EES
        self.P_PV = INITIAL_PRODUCTION_PV
        self.P_ED = INITIAL_ELECTRICAL_DEMAND
        self.C_EG = INITIAL_ELECTRICITY_COST

        # unobserved state variables
        self.P_PVED = 0
        self.P_PVEES = 0
        self.P_PVEG = 0
        self.P_EESED = 0
        self.P_EGED = 0
        self.P_EGEES = 0

        self.done = False # initialize the "end of episode"-flag to False

    def step(self, action):
        # execute one time step within the environment
        # action corresponds to a_EGEES, i.e. charging power from electrical grid (EG) to electrical energy storage (EES)
        # given as a fraction of the maximum charging power

        # update state values
        # amount of power flow from EG to EES       # action/4 because the action space is defined as integers from 0 to 4
        self.P_EGEES = min(action / 4 * MAXIMUM_CHARGING_POWER_EGEES, (CAPACITY_EES - self.E_EES) / DELTA_T)
        # amount of power flow from PV to ED
        self.P_PVED = min(self.P_ED, self.P_PV)
        # amount of power flow from PV to EES
        self.P_PVEES = min((CAPACITY_EES - self.E_EES) / DELTA_T, self.P_PV - self.P_PVED)
        # amount of power flow from PV to EG
        self.P_PVEG = self.P_PV - self.P_PVEES - self.P_PVED
        # amount of power flow from EES to ED
        self.P_EESED = min(self.P_ED - self.P_PVED, self.E_EES / DELTA_T)
        # amount of power flow from EG to ED
        self.P_EGED = self.P_ED - self.P_PVED - self.P_EESED

        # amount of electrical energy stored in EES
        self.E_EES = min(self.E_EES + (self.P_PVEES + self.P_EGEES - self.P_EESED)*DELTA_T, CAPACITY_EES)
        self.P_PV = PV_PRODUCTION[self.timestep]
        self.P_ED = ELECTRICAL_DEMAND[self.timestep]
        self.C_EG = COST_OF_ELECTRICITY[self.timestep]

        obs = [self.E_EES, self.P_PV, self.P_ED, self.C_EG]
        reward = - self.C_EG*(self.P_EGEES + self.P_EGED)

        # if max #timesteps is reached (e.g. 24 with hourly resolution and one episode representing one day), set done = True
        if self.timestep == 24:
            self.done = True

        info = {} # no information to give

        self.timestep += 1

        print(f"reward:     {reward}\n")

        return obs, reward, self.done, info

    def render(self, mode='human'):

        print(f"timestep:   {self.timestep}\n\n"
              f"P_EGEES:    {self.P_EGEES}\n"
              f"P_PVEES:    {self.P_PVEES}\n"
              f"P_PVEG:     {self.P_PVEG}\n"
              f"P_EESED:    {self.P_EESED}\n"
              f"P_EGED:     {self.P_EGED}\n"
              f"P_PVED:     {self.P_PVED}\n\n"
              f"E_EES:      {self.E_EES}\n"
              f"P_PV:       {self.P_PV}\n"
              f"P_ED:       {self.P_ED}\n"
              f"C_EG:       {self.C_EG}\n\n"
              f"-------------------------\n")

