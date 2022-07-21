import numpy as np


# source: https://medium.com/analytics-vidhya/coding-a-neural-network-for-xor-logic-classifier-from-scratch-b90543648e8a
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


def forward_prop(w1, w2, x):
    z1 = np.dot(w1, x)
    a1 = sigmoid(z1)
    z2 = np.dot(w2, a1)
    a2 = sigmoid(z2)
    return z1, a1, z2, a2


def back_prop(m, w1, w2, z1, a1, z2, a2, x, y):
    dz2 = a2 - y
    dw2 = np.dot(dz2, a1.T) / m
    dz1 = np.dot(w2.T, dz2) * a1 * (1 - a1)
    dw1 = np.dot(dz1, x.T) / m
    dw1 = np.reshape(dw1, w1.shape)

    dw2 = np.reshape(dw2, w2.shape)
    return dz2, dw2, dz1, dw1


def load_train_data(file):
    with open(file, "r") as f:
        x = [[], []]
        y = []
        while True:
            data = f.readline().replace('\n', '').split(' ')
            if not data[0]:
                break
            x[0].append(int(data[0]))
            x[1].append(int(data[1]))
            y.append(int(data[2]))
        return np.array(x), np.array(y)


def predict(w1, w2, _input):
    z1, a1, z2, a2 = forward_prop(w1, w2, _input)
    a2 = np.squeeze(a2)
    if a2 >= 0.5:
        print("Acuratete:", a2)
        print("For input", [i[0] for i in _input], "output is 1")
    else:
        print("Acuratete:", 1 - a2)
        print("For input", [i[0] for i in _input], "output is 0")


def predict_multiple(w1, w2, _inputs):
    pass


def training(w1, w2, x, y):
    iterations = 1000  # epochs
    lr = 1  # learning rate
    m = x.shape[1]  # total training examples
    for i in range(iterations):
        z1, a1, z2, a2 = forward_prop(w1, w2, x)
        da2, dw2, dz1, dw1 = back_prop(m, w1, w2, z1, a1, z2, a2, x, y)
        w2 = w2 - lr * dw2
        w1 = w1 - lr * dw1
    return w1, w2


X, Y = load_train_data(input("Function: (OR / AND / XOR): ").upper() + ".txt")
# Number of inputs
n_x = 2
# Number of neurns in output layer
n_y = 1
# Number of neurons in hidden layer
n_h = 2

np.random.seed(5)
# Define weight matrices for neural network
# weight matrix for hidden and output layer
W1 = np.random.randn(n_h, n_x)
W2 = np.random.randn(n_y, n_h)

W1, W2 = training(W1, W2, X, Y)

if __name__ == "__main__":
    predict(W1, W2, np.array([[0], [0]]))
    predict(W1, W2, np.array([[0], [1]]))
    predict(W1, W2, np.array([[1], [0]]))
    predict(W1, W2, np.array([[1], [1]]))
