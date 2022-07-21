import numpy as np


class Environment:
    number_rows = 4
    number_columns = 4
    action_size = 4
    state_size = 16

    learning_rate = 0.1
    gamma = 0.99

    number_of_episodes = 1000
    number_of_stepts = 100

    actions = {0: "N", 1: "S", 2: "V", 3: "E"}

    steps = {
        "N": (lambda x, y: (x, max(y - 1, 0))),
        "S": (lambda x, y: (x, min(y + 1, Environment.number_rows - 1))),
        "V": (lambda x, y: (max(x - 1, 0), y)),
        "E": (lambda x, y: (min(x + 1, Environment.number_columns - 1), y))
    }

    curr_state = [0, 0]
    rewards = [
        [0, 0, 0, 0],
        [0, -1, 0, -1],
        [0, 0, 0, -1],
        [-1, 0, 0, 1]
    ]

    matrix = [
        ['F', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H'],
        ['F', 'F', 'F', 'H'],
        ['H', 'F', 'F', 'G']
    ]

    def step(_state, _action):
        x, y = _state
        new_state = Environment.steps.get(Environment.actions.get(_action))(x, y)
        if (x >= 0 and y >= 0) and (x < Environment.state_size and y < Environment.action_size):
            Environment.curr_state = new_state
            return new_state
        else:
            return _state


Q = np.random.rand(Environment.state_size, Environment.action_size)
print(Q)


def print_data(s):
    matrix = Environment.matrix
    temp = ''
    print(s)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (i, j) == s:
                temp += "S "
            else:
                temp += matrix[i][j] + " "
        temp += '\n'
    print(temp)


if __name__ == "__main__":
    state = Environment.curr_state
    rev_list = []
    for i in range(Environment.number_of_episodes):
        state = [0, 0]
        print_data(state)
        total_reward = 0
        j = 0
        while j < Environment.number_of_stepts:
            j += 1
            x, y = state
            position = x * Environment.action_size + y
            action = np.argmax(Q[position,:])
            print(action)
            new_state = Environment.step(state, action)
            new_x, new_y = new_state
            reward = Environment.rewards[new_x][new_y]
            new_position = new_x * Environment.action_size + new_y
            Q[position, action] = Q[position, action] + Environment.learning_rate \
                * (reward + Environment.gamma * np.max(Q[new_position, :]) - Q[position, action])
            total_reward += reward
            print_data(new_state)
            if reward == 1 or reward == -1:
                break
            state = new_state
        rev_list.append(total_reward)
        print("Reward sum of all episodes: " + str(sum(rev_list) / Environment.number_of_episodes))
        print("Final Values Q table")
        print(Q)