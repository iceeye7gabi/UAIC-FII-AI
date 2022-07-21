import gym
import numpy as np
env = gym.make('FrozenLake-v1')
action_size = env.action_space.n
state_size = env.observation_space.n

Q = np.zeros([state_size, action_size])

alpha = .65
gamma = .9
number_of_episodes = 1000
max_steps = 99
rev_list = []
for i in range(number_of_episodes):
    state = env.reset()
    total_reward = 0
    done = False
    j = 0
    while j < max_steps:
        env.render()
        j += 1
        action = np.argmax(Q[state, :] + np.random.randn(1, env.action_space.n) * (1./(i + 1)))
        new_state, reward, done, _ = env.step(action)
        Q[state, action] = Q[state, action] + alpha * (reward + gamma * np.max(Q[new_state, :]) - Q[state, action])
        if done:
            total_reward = 1
            break
        state = new_state
    rev_list.append(total_reward)
    env.render()
    print(f"Reward:{total_reward}")
    print("Final Values Q table")
    print(Q)