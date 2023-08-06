from datetime import datetime
import tensorflow as tf

from tensorboard.plugins.custom_scalar.summary import pb
from tensorboard.plugins.custom_scalar.layout_pb2 import (Layout, Category, Chart,
                                                          MarginChartContent)

def random_generator(seed=None):
    """
    Create Random Generator

    Parameters
    ----------
    seed : int or tf.random.Generator, optional
        If `None` (default), create non deterministic Generator.
        If `int`, create Generator from seed.
        If `tf.random.Generator`, create independent Generator by split method.
    """
    if seed is None:
        return tf.random.Generator.from_non_deterministic_state()

    if isinstance(seed, tf.random.Generator):
        return seed.split()[0]

    return tf.random.Generator.from_seed(seed)


def clone_model(model: tf.keras.Model):
    """
    Clone model

    This is workaround, since tf.keras.models.clone_model cannot clone subclass of
    tf.keras.Model. https://github.com/tensorflow/tensorflow/issues/47048

    Parameters
    ----------
    model : tf.keras.Model

    Returns
    -------
    clone : tf.keras.Model
        Cloned model
    """
    clone = model.__class__(**model.get_config())
    clone.set_weights(model.get_weights())
    return clone


def evaluate(env, policy, training_step, max_episode_steps=None, ntimes=10):
    """
    Evaluate policy

    Parameters
    ----------
    env : gym.Env
        Environment
    policy : rlfw.discrete.policy.Policy or rlfw.continuious.policy.Policy
        Policy
    training_step : int
        Training step to be used for x-axis value
    max_episode_steps : int, optional
        Max episode steps to terminate episode. Default is None (Infinity)
    ntimes : int, optional
        Number of times to evaluate. Default is 1.

    Returns
    -------
    rewards : tf.Tensor
        Set of episode total reward
    """
    rewards = []

    for _ in range(ntimes):
        obs = env.reset()
        reward = 0.0

        step = 0
        while True:
            obs, rew, done, _ = env.step(policy(obs))
            reward += rew

            if done or (max_episode_steps and (step >= max_episode_steps)):
                break

            step += 1

        rewards.append(reward)

    rewards = tf.constant(rewards, dtype=tf.float32)

    mean = tf.reduce_mean(rewards)
    V = tf.math.reduce_variance(rewards)
    std = tf.math.reduce_std(rewards)
    ntimes = tf.constant(ntimes, dtype=tf.float32)

    if ntimes > 1:
        error = std/tf.math.sqrt(ntimes -1)
    else:
        error = tf.constant(0, dtype=tf.float32)

    tf.summary.scalar("Evaluation/Reward/mean",
                      data=mean, step=training_step)
    tf.summary.scalar("Evaluation/Reward/mean_upper",
                      data=mean+error, step=training_step)
    tf.summary.scalar("Evaluation/Reward/mean_lower",
                      data=mean-error, step=training_step)

    if ntimes > 1:
        unbiased_V = V * ntimes/(ntimes - 1)
        v_relative_error = tf.math.sqrt(2 / (ntimes - 1))

        tf.summary.scalar("Evaluation/Reward/variance",
                          data=unbiased_V, step=training_step)
        tf.summary.scalar("Evaluation/Reward/variance_upper",
                          data=unbiased_V*(1+v_relative_error), step=training_step)
        tf.summary.scalar("Evaluation/Reward/variance_lower",
                          data=unbiased_V*(1-v_relative_error), step=training_step)

    return rewards


def prepare_log(dir_name="./logs"):
    """
    Prepare Log

    Parameters
    ----------
    dir_name : str, optional
        Directory name to log. Default is './logs'

    Returns
    -------
    writer : tf.summary.FileWriter
    """
    log_dir = dir_name + datetime.now().strftime("/%Y%m%d%H%M%S")
    writer = tf.summary.create_file_writer(log_dir)
    writer.set_as_default()

    mean = MarginChartContent.Series(value="Evaluation/Reward/mean",
                                     lower="Evaluation/Reward/mean_upper",
                                     upper="Evaluation/Reward/mean_lower")
    variance = MarginChartContent.Series(value="Evaluation/Reward/variance",
                                         lower="Evaluation/Reward/variance_lower",
                                         upper="Evaluation/Reward/variance_upper")
    chart_m = Chart(title="Reward/mean",
                    margin=MarginChartContent(series=[mean]))
    chart_v = Chart(title="Reward/variance",
                    margin=MarginChartContent(series=[variance]))

    layout = pb(Layout(category=[Category(title="Evaluation",
                                          chart=[chart_m, chart_v])]))


    # https://github.com/tensorflow/tensorflow/issues/32918#issuecomment-749066283
    tf.summary.write(layout.value[0].tag,
                     tf.constant(tf.make_ndarray(layout.value[0].tensor)),
                     step=0,
                     metadata=layout.value[0].metadata)

    return writer


def create_counter(start=0):
    return tf.Variable(start, dtype=tf.int64)
