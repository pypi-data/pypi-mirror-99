import tensorflow as tf

from rlfw.discrete.value import QFunction
from rlfw.parameter import HyperParameter
from rlfw.util import random_generator, create_counter


class Policy:
    def __call__(self, state):
        """
        Get an action from a state

        Parameters
        ----------
        state : array-like
            Single state

        Returns
        -------
        action : np.ndarray
            An action obeying policy
        """
        state = tf.expand_dims(tf.constant(state), axis=0)
        return tf.squeeze(self.get_action(state), axis=0).numpy()

    def get_action(self, state: tf.Tensor):
        raise NotImplementedError


class RandomPolicy(Policy):
    """
    Random Policy

    Choose action randomly
    """
    def __init__(self, act_size: int, *, seed = None):
        """
        Initialize RandomPolicy

        Parameters
        ----------
        act_size : int
            Number of actions
        seed : int, optional
            Seed for Random Generator
        """
        self.act_size = tf.constant(act_size, dtype=tf.int64)
        self.rng = random_generator(seed)

    @tf.function
    def get_action(self, state: tf.Tensor):
        return self.rng.uniform([state.shape[0]],
                                minval=0, maxval=self.act_size,
                                dtype=tf.int64)


class GreedyPolicy(Policy):
    """
    Greedy Policy

    Choose action such as argmax Q(state, action)
    """
    def __init__(self, Q: QFunction):
        """
        Initialize GreedyPolicy

        Parameters
        ----------
        Q : rlfw.discrete.value.QFunction
            Q function which takes state and returns Q value for each discrete action
        """
        self.Q = Q

    @tf.function
    def get_action(self, state: tf.Tensor):
        return tf.math.argmax(self.Q._call(state), axis=1)


class EpsilonGreedyPolicy(Policy):
    """
    epsilon-Greedy Policy

    Choose action such as argmax Q(state, action) or random search
    """
    def __init__(self, act_size: int, Q: QFunction, eps: HyperParameter,
                 *, seed=None):
        """
        Initialize EpsilonGreedyPolicy

        Parameters
        ----------
        act_size : int
            Number of actions
        Q : rlfw.discrete.value.QFunction
            Q function which takes state and returns Q value for each discrete action
        eps : rlfw.parameter.HyperParameter
            Small probability to search randomly
        seed : float, optional
            Seed for Random Generator
        """
        self.eps = eps
        self.rng = random_generator(seed)

        self.random_policy = RandomPolicy(act_size, seed=self.rng)
        self.greedy_policy = GreedyPolicy(Q)
        self.train_counts = create_counter()

    @tf.function
    def get_action(self, state: tf.Tensor):
        eps = self.eps.get_value(self.train_counts)
        self.train_counts.assign_add(1)

        if self.rng.uniform([1], minval=0.0, maxval=1.0) < eps:
            return self.random_policy.get_action(state)
        else:
            return self.greedy_policy.get_action(state)
