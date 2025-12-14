import pickle
import sys

try:
    with open("qtable_farol.pkl", "rb") as f:
        q_table = pickle.load(f)
        print(f"Q-Table size: {len(q_table)}")
        print("Sample entries:")
        count = 0
        print(f"Values for (0, 0): {q_table.get((0, 0))}")
except Exception as e:
    print(f"Error reading Q-Table: {e}")

