import matplotlib.pyplot as plt
import random
import numpy as np


def bandit_algorithm(k_arm, epsilon, runs, time):
    collect_reward = np.zeros((runs, time))
    collect_op_action = np.zeros((runs, time))

    action_list = list(range(k_arm))

    for run in range(runs):
        # Initialize, for a = 1 to k
        # q*(a) is an normal distribution with mean 0 and variance 1 for each action a = 0, 1, ..., 9 [Figure 2.1]
        q_true = np.random.normal(0, 1, k_arm)
        optimal_action = np.argmax(q_true)
        # initial estimate Q1(a) = 0, for all a
        q_estimated = np.zeros(k_arm)
        # counts the occurence in an action
        action_count = [0] * k_arm
        # Loop forever
        for t in range(time):
            # random variable epsilon-gredy simulation
            if random.uniform(0, 1) < 1 - epsilon:
                action = np.argmax(q_estimated)
            else:
                action = random.choice(action_list)
            # R_t has distribution normal with mean q*(A_t) and variance 1 [Figure 2.1]
            reward = random.gauss(q_true[action], 1)
            # update the occurrences in an action
            action_count[action] += 1
            # sample-average technique Q(A) = Q(A) + 1/N(A)*(reward - Q(A))
            q_estimated[action] = q_estimated[action] + (reward - q_estimated[action]) / action_count[action]
            # collect the reward ti print
            collect_reward[run, t] = reward

            if action == optimal_action:
                collect_op_action[run, t] += 1

    return collect_reward.mean(axis=0), collect_op_action.mean(axis=0)

