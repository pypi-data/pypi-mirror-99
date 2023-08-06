import tensorflow as tf

from cpprb import ReplayBuffer, PrioritizedReplayBuffer

from rlfw.discrete.value import QFunction
from rlfw.loss import Huber
from rlfw.parameter import HyperParameter, ConstantParameter
from rlfw.util import clone_model, create_counter

class OffPolicy:
    def __init__(self, *,
                 prioritized: bool = True,
                 Nstep: int = None,
                 gamma: float = 0.99):
        # Must be Python object, to evaluate only once in @tf.function
        self.prioritized = bool(prioritized)

        self.train_counts = create_counter()

        self.gamma = tf.constant(gamma)
        if Nstep is None:
            self.Nstep = False
            self.discount = self.gamma
        else:
            self.Nstep = tf.constant(Nstep, shape=[1], dtype=tf.int32)
            self.discount = tf.constant(gamma ** Nstep)

    def create_buffer(self, buffer_size, env, **kwargs):
        """
        Create Replay Buffer

        Parameters
        ----------
        buffer_size : int
            Buffer size
        env : gym.Env
            Environment
        **kwargs : keyword, optional
            Additional keyword to pass replaybuffer
        """
        RB = PrioritizedReplayBuffer if self.prioritized else ReplayBuffer

        env_dict = {"obs": {"shape": env.observation_space.shape},
                    "act": {"dtype": int},
                    "rew": {},
                    "next_obs": {"shape": env.observation_space.shape},
                    "done": {}}

        Nstep = {"size": int(self.Nstep),
                 "gamma": float(self.gamma)} if self.Nstep is not None else None

        return RB(buffer_size, env_dict, Nstep=Nstep, **kwargs)

    def train(self, sample):
        """
        Train Q value function

        Parameters
        ----------
        sample
            Sample transitions

        Returns
        -------
        absTD : tf.Tensor
           Absolute value of TD if prioritized else 1.0
        """
        obs = tf.constant(sample["obs"])
        act = tf.constant(sample["act"].ravel())
        rew = tf.constant(sample["rew"].ravel())
        next_obs = tf.constant(sample["next_obs"])
        done = tf.constant(sample["done"].ravel())

        if self.prioritized:
            weight = tf.constant(sample["weights"].ravel())
        else:
            weight = tf.constant(1.0)

        absTD = self._train(obs, act, rew, next_obs, done, weight)
        self.train_counts.assign_add(1)
        return absTD

    def _train(self, obs: tf.Tensor, act: tf.Tensor,
               rew: tf.Tensor, next_obs: tf.Tensor,
               done: tf.Tensor, weight: tf.Tensor):
        raise NotImplementedError


class DQN(OffPolicy):
    """
    Deep Q Network

    References
    ----------
    """
    def __init__(self, Q: QFunction,* ,
                 target_update_freq: int = 5000,
                 gamma: float = 0.99,
                 Nstep: int = None,
                 double_DQN: bool = False,
                 prioritized: bool = True,
                 loss = Huber,
                 optimizer = None):
        """
        Initialize DQN algorithm

        Parameters
        ----------
        Q : rlfw.discrete.value.QFnunction
            Q function which takes state and returns Q value for each discrete action
        target_update_freq : int, optional
            Target network udate frequency. Default is `5000`
        gamma : float, optional
            Reward discount factor. Default it `0.99`
        Nstep : int, optional
            Nstep reward. Default is `None` (= 1 step)
        double_DQN : bool, optional
            Whether use Double DQN. Default is `False`
        prioritized : bool, optional
            Whether use prioritized experience replay
        loss : callable, optional
            Loss function taking |TD|. Default is Huber loss
        optimizer : tf.keras.optimizers.Optimizer, optional
            Optimizer. Default is Adam
        """
        super().__init__(prioritized=prioritized, Nstep=Nstep, gamma=gamma)

        self.Q = Q
        self.target_Q = clone_model(Q)

        if isinstance(target_update_freq, HyperParameter):
            self.target_update_freq = target_update_freq
        else:
            self.target_update_freq = ConstantParameter("target_update_freq",
                                                        target_update_freq,
                                                        dtype=tf.int64)

        # Must be Python object, to evaluate only once in @tf.function
        self.double_DQN = bool(double_DQN)

        self.loss = loss
        self.optimizer = optimizer or tf.keras.optimizers.Adam()

    def update_target(self):
        for t, s in zip(self.target_Q.trainable_weights, self.Q.trainable_weights):
            t.assign(s)

    @tf.function
    def _train(self, obs: tf.Tensor, act: tf.Tensor,
               rew : tf.Tensor, next_obs: tf.Tensor,
               done: tf.Tensor, weight: tf.Tensor):

        with tf.GradientTape() as tape:
            tape.watch(self.Q.trainable_weights)
            Q  = self.Q._call(obs)
            act_dim = Q.shape[1]
            act_hot = tf.one_hot(act, depth=act_dim)

            Q = tf.reduce_sum(Q * act_hot, axis=1)
            Q1 = self.target_Q._call(next_obs)

            if self.double_DQN:
                Q1 = Q1 * tf.one_hot(tf.math.argmax(self.Q._call(next_obs), axis=1),
                                     depth=act_dim)
                Q1 = tf.reduce_sum(Q1, axis=1)
            else:
                Q1 = tf.reduce_max(Q1, axis=1)
            Q1 = tf.stop_gradient(Q1)

            assert Q1.shape == rew.shape, f"BUG: Shape mismuch between rew ({rew}) and Q1 ({Q1})"
            r_yQ = rew + (1.0 - done) * self.discount * Q1

            assert r_yQ.shape == Q.shape, f"BUG: Shape mismuch between r_yQ ({r_yQ}) and Q ({Q})"
            absTD = tf.math.abs(r_yQ - Q)
            loss = self.loss(absTD)

            if self.prioritized:
                loss = loss * weight

            loss = tf.reduce_mean(loss)

        grad = tape.gradient(loss, self.Q.trainable_weights)
        self.optimizer.apply_gradients(zip(grad, self.Q.trainable_weights))
        tf.summary.scalar("Training/Loss", data=loss, step=self.train_counts)

        if self.prioritized:
            absTD = tf.math.abs(r_yQ - tf.reduce_max(self.Q._call(obs) * act_hot))
        else:
            absTD = tf.constant(1.0)

        if tf.math.floormod(self.train_counts,
                            self.target_update_freq.get_value()) == 0:
            self.update_target()

        return absTD
