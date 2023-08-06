import tensorflow as tf

from rlfw.parameter import HyperParameter, ConstantParameter
from rlfw.util import random_generator, create_counter


class Policy(tf.keras.Model):
    def __init__(self, act_min, act_max):
        super().__init__()

        self.act_min = act_min
        self.act_max = act_max

    def call(self, state, *args, **kwargs):
        """
        Get an action from a state

        Parameters
        ----------
        state : array-like
            Single state

        Reeturns
        --------
        action : np.ndarray
            An action obeying policy
        """
        state = tf.expand_dims(tf.constant(state), axis=0)
        v = tf.squeeze(self.get_action(state), axis=0).numpy()

        if self.act_min or self.act_max:
            v = v.clip(min=self.act_min, max=self.act_max)

        return v

    def get_action(self, state: tf.Tensor):
        raise NotImplementedError

    def get_config(self):
        return {"act_min": self.act_min, "act_max": self.act_max}


class GreedyPolicy(Policy):
    """
    Greedy Policy
    """
    def __init__(self, state_shape, act_dim, act_min, act_max,
                 fully_connected = (100, 100, 100)):
        """
        Initialize Greedy Policy

        Parameters
        ----------
        state_shape : array-like of int
            Shape of state
        act_dim : int
            Dimension of action
        act_min : float
            Minimum action
        act_max : float
            Maximum action
        fully_connected : array_like of int, option
            Numbers of units at fully connected layers.
            Default is `(100, 100, 100)`
        """
        super().__init__(act_min=act_min, act_max=act_max)

        act_size = 1
        if isinstance(act_dim, int):
            act_size = act_dim
        else:
            for i in act_dim:
                act_size *= i

        FC = tf.keras.layers.Dense
        self.i = tf.keras.layers.InputLayer(input_shape=state_shape)
        self.fc = [FC(u, activation="relu") for u in fully_connected]
        self.o = FC(act_size, activation="tanh")

        self.center = tf.constant((act_min + act_max)/2)
        self.scale  = tf.constant((act_max - act_min)/2)

    @tf.function
    def get_action(self, state: tf.Tensor):
        state = self.i(state)

        for L in self.fc:
            state = L(state)

        return self.o(state) * self.scale + self.center

    def get_weights(self):
        weights = []

        weights.append([L.get_weights() for L in self.fc])
        weights.append(self.o.get_weights())

        return weights

    def set_weights(self, weights):
        fc, output = weights

        for L, w in zip(self.fc, fc):
            L.set_weights(w)

        self.o.set_weights(output)

    def get_config(self):
        return {**super().get_config(),
                "state_shape": self.i.get_config()["batch_input_shape"][1:],
                "act_dim": self.o.units,
                "fully_connected": (L.units for L in self.fc)}


class GaussianNoisePolicy(Policy):
    """
    Gaussian Noise Policy
    """
    def __init__(self, policy: Policy,
                 noise_sigma: HyperParameter,
                 act_min, act_max, *,
                 seed = None):
        """
        Initialize GaussianNoisePolicy

        Parameters
        ----------
        policy : Policy
            Policy to add noise to
        noise_sigma : HyperParameter or float
            Gaussian Noise standard deviation.
        act_min : float
            Minimum action
        act_max : float
            Maximum action
        seed : int or tf.random.Generator, optional
            Seed for random generator
        """
        super().__init__(act_min=act_min, act_max=act_max)

        self.policy = policy

        if isinstance(noise_sigma, HyperParameter):
            self.noise_sigma = noise_sigma
        else:
            self.noise_sigma = ConstantParameter("GaussianNoisePolicy/sigma",
                                                 noise_sigma)

        self.rng = random_generator(seed)
        self.counts = create_counter()

    @tf.function
    def get_action(self, state: tf.Tensor):
        action = self.policy.get_action(state)

        noise = self.rng.normal(action.shape,
                                stddev=self.noise_sigma.get_value(self.counts))
        self.counts.assign_add(1)
        return action + noise

    def get_weights(self):
        return self.policy.get_weights()

    def set_weights(self, weights):
        self.policy.set_weights(weights)

    def get_config(self):
        return {**super().get_config(),
                "policy": self.policy,
                "noise_sigma": self.noise_sigma,
                "seed": self.rng}
