import numpy as np
from scipy import stats

def estimate_probability(data, lower=None, upper=None):
    """
    Estimate the probability of a value (or range) based on data.

    Parameters:
    - data (list or np.array): The dataset
    - lower (float): Lower bound of the interval (None means -∞)
    - upper (float): Upper bound of the interval (None means +∞)
    - use_kde (bool): Use KDE instead of normal distribution

    Returns:
    - prob (float): Estimated probability
    """

    data = np.array(data)

    # Set bounds
    if lower is None:
        lower = -np.inf
    if upper is None:
        upper = np.inf
    
    mu, std = stats.norm.fit(data)
    prob = stats.norm.cdf(upper, mu, std) - stats.norm.cdf(lower, mu, std)
    print(prob)

    return prob

def separation(s_min, agent_power, neighbours_power):
    print(neighbours_power)
    s = np.multiply(s_min, 2 - estimate_probability(data=neighbours_power, upper=agent_power))
    if s < s_min:
            s = s_min
    return s