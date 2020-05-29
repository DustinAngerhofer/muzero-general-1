import gym
import pickle
import time


with open('/home/w033dja/PycharmProjects/muzero-general/results/Video Pinball/2020-05-29--09-48-23/replay_buffer.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data)


env_name = 'VideoPinball-ram-v0'
env = gym.make(env_name)


env.reset()

for i in range(len(data[0].action_history)):
    action = data[2].action_history[i]
    env.step(action)
    env.render()
    time.sleep(0.03)



