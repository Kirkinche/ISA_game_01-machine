import numpy as np
import random
from dynamics import Dynamics
from machine_component import MachineComponent

class BayesianInference:
    def __init__(self, prior_mean, prior_variance, likelihood_variance):
        self.prior_mean = prior_mean
        self.prior_variance = prior_variance
        self.likelihood_variance = likelihood_variance

    def update_posterior(self, observed_data):
        n = len(observed_data)
        sample_mean = np.mean(observed_data)
        
        # Calculate the posterior mean and variance
        posterior_variance = 1 / (1/self.prior_variance + n/self.likelihood_variance)
        posterior_mean = posterior_variance * (self.prior_mean/self.prior_variance + n*sample_mean/self.likelihood_variance)
        
        return posterior_mean, posterior_variance

class MetropolisAlgorithm:
    def __init__(self, component, temperature=1.0):
        self.component = component
        self.temperature = temperature

    def acceptance_probability(self, old_cost, new_cost):
        """ Calculate acceptance probability for the new state. """
        if new_cost < old_cost:
            return 1.0
        else:
            return np.exp((old_cost - new_cost) / self.temperature)

    def propose_new_state(self, perturbation_factors):
        """ Propose a new state by perturbing forces, environmental conditions, or other critical parameters. """
        proposed_state = self.component  # Clone the component if necessary
        
        # Perturb forces applied to the component
        for name in proposed_state.forces:
            perturbation = np.random.normal(0, perturbation_factors["force"])
            proposed_state.forces[name]["vector"] = tuple(f + perturbation for f in proposed_state.forces[name]["vector"])
        
        # Perturb environmental conditions such as temperature
        proposed_state.temperature += np.random.normal(0, perturbation_factors["temperature"])
        
        return proposed_state

    def evaluate_state(self, component):
        """ Evaluate the 'cost' of the current state.
        This could be based on factors such as stress, wear, energy consumption, etc.
        """
        component.calculate_dynamics(time_interval=1)  # Use Dynamics module
        stress = component.stress
        wear = component.wear
        energy = component.kinetic_energy + component.potential_energy
        
        # Define a cost function (example: weighted sum of stress, wear, energy)
        cost = stress + wear * 10 + energy * 0.1
        return cost

    def run(self, iterations=1000, perturbation_factors=None):
        if perturbation_factors is None:
            perturbation_factors = {"force": 0.1, "temperature": 0.5}

        current_state = self.component
        current_cost = self.evaluate_state(current_state)
        
        for i in range(iterations):
            new_state = self.propose_new_state(perturbation_factors)
            new_cost = self.evaluate_state(new_state)

            acceptance_prob = self.acceptance_probability(current_cost, new_cost)
            if random.uniform(0, 1) < acceptance_prob:
                current_state = new_state
                current_cost = new_cost
                print(f"Iteration {i}: Accepted new state with cost {current_cost}")
            else:
                print(f"Iteration {i}: Rejected new state with cost {new_cost}")
        
        return current_state

class MetropolisAlgorithmWithBayesian(MetropolisAlgorithm):
    def __init__(self, component, temperature=1.0):
        super().__init__(component, temperature)
        self.bayesian_inference = BayesianInference(
            prior_mean=0, 
            prior_variance=1, 
            likelihood_variance=1
        )

    def evaluate_state_with_bayesian(self, component, observed_data):
        cost = self.evaluate_state(component)
        posterior_mean, posterior_variance = self.bayesian_inference.update_posterior(observed_data)
        
        # Example: Combine prior and posterior information into the cost
        prior_weight = 0.3
        posterior_weight = 1 - prior_weight
        adjusted_cost_component = prior_weight * self.bayesian_inference.prior_mean + posterior_weight * posterior_mean
        
        # Penalize high variance (uncertainty)
        uncertainty_penalty = posterior_variance * 10  # Arbitrary scaling factor

        # Update the cost with Bayesian-influenced adjustments
        cost += adjusted_cost_component + uncertainty_penalty
        
        return cost

    def run(self, iterations=1000, perturbation_factors=None, observed_data=None):
        if perturbation_factors is None:
            perturbation_factors = {"force": 0.1, "temperature": 0.5}
        
        if observed_data is None:
            observed_data = []
        
        current_state = self.component
        current_cost = self.evaluate_state_with_bayesian(current_state, observed_data)
        
        for i in range(iterations):
            new_state = self.propose_new_state(perturbation_factors)
            new_cost = self.evaluate_state_with_bayesian(new_state, observed_data)

            acceptance_prob = self.acceptance_probability(current_cost, new_cost)
            if random.uniform(0, 1) < acceptance_prob:
                current_state = new_state
                current_cost = new_cost
                print(f"Iteration {i}: Accepted new state with cost {current_cost}")
            else:
                print(f"Iteration {i}: Rejected new state with cost {new_cost}")
        
        return current_state
