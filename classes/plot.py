import os
import pickle
import re

import matplotlib.pyplot as plt

data_path = "data"
assert os.path.exists(data_path), "Path does not exist!"

for file in os.listdir(data_path):
    board_size, iters, games = list(map(int, re.findall(r"\d+", file)))

    file_path = data_path + "/" + file
    with open(file_path, "rb") as file:
        df = pickle.load(file)
        df = df["red_mu"]
    df.plot(label=iters)

plt.xlabel("#Games")
plt.ylabel("Elo rating")
plt.legend(title="#Iterations", loc="best")
plt.show()