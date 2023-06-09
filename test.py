import gym
import matplotlib.pyplot as plt
import pandas as pd

from river import bandit
from river import proba
from river import stats

from bayes_ucb import BayesUCB


def pull_func(policy, env):
    return next(policy.pull(range(env.action_space.n)))


if __name__ == '__main__':
    policies = [
        BayesUCB(seed=123),
        bandit.EpsilonGreedy(epsilon=0.9, seed=101),
        bandit.UCB(delta=100),
        bandit.ThompsonSampling(dist=proba.Beta(), seed=101),
    ]

    policy_names = {
        0: 'BayesUCB',
        1: 'EpsilonGreedy',
        2: 'UCB',
        3: 'ThompsonSampling'
    }

    colors = {
        'BayesUCB': 'tab:blue',
        'EpsilonGreedy': 'tab:red',
        'UCB': 'tab:green',
        'ThompsonSampling': 'tab:orange'
    }

    env = gym.make('river_bandits/CandyCaneContest-v0', max_episode_steps=1000)

    trace_sum = bandit.evaluate(
        policies=policies,
        env=env,
        reward_stat=stats.Sum(),
        pull_func=pull_func,
        n_episodes=10,
        seed=42
    )
    trace_sum = pd.DataFrame(trace_sum)
    print(trace_sum.sample(5, random_state=42))  # example

    trace_mean = bandit.evaluate(
        policies=policies,
        env=env,
        reward_stat=stats.Mean(),
        pull_func=pull_func,
        n_episodes=10,
    )
    trace_mean = pd.DataFrame(trace_mean)
    print(trace_mean.sample(5, random_state=42))  # example


    # plot
    fig, axes = plt.subplots(nrows=1, ncols=2)

    (
        trace_sum
            .assign(policy=trace_sum.policy_idx.map(policy_names))
            .groupby(['step', 'policy'])
        ["reward_stat"].mean()
            .unstack()
            .plot(ax=axes[0], color=colors)
    )

    (
        trace_mean
            .assign(policy=trace_mean.policy_idx.map(policy_names))
            .groupby(['step', 'policy'])
        ["reward_stat"].mean()
            .unstack()
            .plot(ax=axes[1], color=colors)
    )

    axes[0].set_ylabel('sum reward')
    axes[1].set_ylabel('mean reward')

    plt.show()

