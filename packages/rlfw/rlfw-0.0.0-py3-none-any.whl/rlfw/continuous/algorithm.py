import tensorflow as tf

from cpprb import ReplayBuffer, PrioritizedReplayBuffer

from rlfw.continuous.value import QFunction
from rlfw.continuous.policy import Policy
from rlfw.loss import Huber
from rlfw.parameter import HyperParameter, ConstantParameter
from rlfw.util import clone_model, create_counter

class OffPolicy:
    def __init__(self, *,
                 prioritized: bool = True,
                 Nstep: int = None,
                 gamma: float = 0.99,
                 dtype = tf.float32):
        # Mus be Python object, to evaluate only once in @tf.function
        self.prioritized = bool(prioritized)

        self.train_counts = create_counter()

        self.dtype = tf.float32

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
                    "act": {"shape": env.action_space.shape},
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
        obs = tf.constant(sample["obs"], dtype=self.dtype)
        act = tf.constant(sample["act"], dtype=self.dtype)
        rew = tf.constant(sample["rew"].ravel(), dtype=self.dtype)
        next_obs = tf.constant(sample["next_obs"], dtype=self.dtype)
        done = tf.constant(sample["done"].ravel(), dtype=self.dtype)

        if self.prioritized:
            weight = tf.constant(sample["weights"].ravel(), dtype=self.dtype)
        else:
            weight = tf.constant(1.0)

        absTD = self._train(obs, act, rew, next_obs, done, weight)
        self.train_counts.assign_add(1)
        return absTD

    def _train(self, obs: tf.Tensor, act: tf.Tensor,
               rew: tf.Tensor, next_obs: tf.Tensor,
               done: tf.Tensor, weight: tf.Tensor):
        raise NotImplementedError


class DDPG(OffPolicy):
    """
    Deep Deterministic Policy Gradient (DDPG)
    """
    def __init__(self, Q: QFunction, pi: Policy, * ,
                 polyak: float = 0.99,
                 gamma: float = 0.99,
                 Nstep: int = None,
                 prioritized: bool = True,
                 loss = Huber,
                 optimizer = None):
        """
        Initialize DDPG algorithm

        Parameters
        ----------
        Q : QFunction
            Q function which takes state and action and returns Q
        pi : Policy
            Policy function which takes state and returns action
        polyak : float or HyperParameter, optional
            Target network update polyak parameter
        Nstep : int, optional
            Nstep reward. Default is `None` (= 1 step)
        prioritized : bool, optional
            Whether use prioritized experience replay
        loss : callable, optional
            Loss function taking |TD|. Default is Huber loss
        optimizer : tf.keras.optimizers.Optimizer, optional
            Optimizer. Default is Adam
        """
        super().__init__(prioritized=prioritized, Nstep=Nstep, gamma=gamma)

        self.Q = Q
        self.pi = pi

        self.target_Q = clone_model(Q)
        self.target_pi = clone_model(pi)

        if isinstance(polyak, HyperParameter):
            self.polyak = polyak
        else:
            self.polyak = ConstantParameter("DDPG/polyak", polyak)

        self.loss = loss
        self.optimizer = optimizer or tf.keras.optimizers.Adam()

    def update_target(self):
        p = self.polyak.get_value(self.train_counts)
        one_p = 1-p

        for t, s in zip(self.target_Q.trainable_weights, self.Q.trainable_weights):
            t.assign(p*t + one_p*s)

        for t, s in zip(self.target_pi.trainable_weights, self.pi.trainable_weights):
            t.assign(p*t + one_p*s)

    @tf.function
    def _train(self, obs: tf.Tensor, act: tf.Tensor,
               rew : tf.Tensor, next_obs: tf.Tensor,
               done: tf.Tensor, weight: tf.Tensor):

        with tf.GradientTape() as pi_tape:
            pi_tape.watch(self.pi.trainable_weights)
            Q = tf.squeeze(self.Q._call(obs, self.pi.get_action(obs)), axis=1)
            actor_loss = Q

            if self.prioritized:
                actor_loss = actor_loss * weight
            actor_loss = - 1.0 * tf.reduce_mean(actor_loss)


        with tf.GradientTape() as Q_tape:
            Q_tape.watch(self.Q.trainable_weights)

            Q = tf.squeeze(self.Q._call(obs, act), axis=1)

            Q1 = self.target_Q._call(next_obs, self.target_pi.get_action(next_obs))
            Q1 = tf.stop_gradient(tf.squeeze(Q1, axis=1))

            assert Q1.shape == rew.shape, f"BUG: Shape mismuch between rew ({rew}) and Q1 ({Q1})"
            r_yQ = rew + (1.0 - done) * self.discount * Q1

            assert r_yQ.shape == Q.shape, f"BUG: Shape mismch between r_yQ ({r_yQ}) and Q ({Q})"
            absTD = tf.math.abs(r_yQ - Q)
            critic_loss = self.loss(absTD)

            if self.prioritized:
                critic_loss = critic_loss * weight
            critic_loss = tf.reduce_mean(critic_loss)

        grad_Q = Q_tape.gradient(critic_loss, self.Q.trainable_weights)
        grad_pi=pi_tape.gradient(actor_loss, self.pi.trainable_weights)

        self.optimizer.apply_gradients(zip(grad_Q + grad_pi,
                                           self.Q.trainable_weights +
                                           self.pi.trainable_weights))

        tf.summary.scalar("Training/Actor-Loss",
                          data=actor_loss, step=self.train_counts)
        tf.summary.scalar("Training/Critic-Loss",
                          data=critic_loss, step=self.train_counts)

        if self.prioritized:
            absTD = tf.math.abs(r_yQ -
                                tf.squeeze(self.Q._call(obs,
                                                        self.pi.get_action(obs)),
                                           axis=1))
        else:
            absTD = tf.constant(1.0)

        self.update_target()

        return absTD
