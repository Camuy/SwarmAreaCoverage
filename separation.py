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
    prob = np.multiply(stats.norm.cdf(upper, mu, std) - stats.norm.cdf(lower, mu, std), 1)
    #print(prob)

    return prob

def separation(s_min, agent_power, neighbours_power):
    #print(neighbours_power)
    s = 1.5 - estimate_probability(data=neighbours_power, upper=agent_power)
    return s

def separation_old(self):
        
    #print("separation at step ", self.step_number," = ", self.separation)
    self.separation += np.multiply(1 - np.divide(self.battery + 40, 100), 2)
    if self.separation < self.min_separation:
        self.separation = self.min_separation
    if self.energy_harvested < self.mean_energy_harvested:
        self.separation = np.multiply(self.min_separation - 1, 3)

    else:
        self.separation  = np.multiply(self.min_separation, 2) - 1
                
    if self.separation > self.vision:
        print("separation is bigger than the vision of agent")
        self.separation = self.vision
    return