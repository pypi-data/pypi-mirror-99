from pathlib import Path
from pprint import pprint

import gym
import gym_d2d

env_config = {
    'num_rbs': 3,
    'num_cues': 3,
    'num_due_pairs': 3,
    'due_max_tx_power_dBm': 2,
    'device_config_file': Path.cwd() / 'device_config.json',
}
env = gym.make('D2DEnv-v0', env_config=env_config)

obses = env.reset()
game_over = False
for _ in range(3):
    actions = {}
    for agent_id, obs in obses.items():
        if agent_id.startswith('due'):
            actions[agent_id] = env.action_space['due'].sample()
        elif agent_id.startswith('cue'):
            actions[agent_id] = env.action_space['cue'].sample()
        else:
            actions[agent_id] = env.action_space['mbs'].sample()

    obses, rewards, game_over, info = env.step(actions)
    print(obses)
    pprint(info)
    print('\n\n')
