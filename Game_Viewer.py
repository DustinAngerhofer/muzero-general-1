import gym
import pickle
import time

path_1 = '/home/w033dja/PycharmProjects/muzero-general-1/results/Video_Pinball/2020-06-02--13-40-48/replay_buffer.pkl'
path_2 = '/home/w033dja/PycharmProjects/muzero-general-1/results/Video_Pinball/2020-05-30--00-21-55/replay_buffer.pkl'
path_3 = '/results/Video_Pinball/Fry_Training_Results_2020_06_01/replay_buffer.pkl'
path_4 = '/replay_buffer.pkl'

with open(path_1, 'rb') as f:
    data = pickle.load(f)

# print(data)
env_name = 'VideoPinball-ram-v0'
env = gym.make(env_name)


env.reset()
env.seed(0)
for i in range(len(data.action_history)):
    action = data.action_history[i]
    env.step(action)
    env.render()
    time.sleep(0.01)
    '''
env.reset()
env.seed(0)
for i in range(500000):
    action = env.action_space.sample()
    env.step(action)
    env.render()
    time.sleep(0.01)
'''