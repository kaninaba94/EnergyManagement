import numpy as np
from math import inf

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

        self.timestep = 0

    def step(self, action):
        # execute one time step within the environment
        self._take_action(action)

        self.timestep += 1

    def _take_action(self, action):


    def reset(self):
        pass

    def render(self, mode='human'):
        pass

