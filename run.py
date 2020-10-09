from environment import EnergyManagementSystem
from temporal_profiles import PV_PRODUCTION

ems = EnergyManagementSystem()

print(f"Initial state of environment:\n")
ems.render()

for t in range(PV_PRODUCTION.shape[0]):

    action = ems.action_space.sample()
    print(f"action:     {action}\n")
    ems.step(action)

    ems.render()
