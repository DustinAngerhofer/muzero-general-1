import gym
import time

env = gym.make("Amidar-v0")
print(env.action_space)
env.reset()
env.seed(0)
for i in range(3000):
    action = env.action_space.sample()
    env.step(action)
    env.render()
    time.sleep(0.03)