import tensorflow as tf

def Huber(absTD: tf.Tensor):
    """
    Calculate Huber Loss for each

    |TD| >  1 -> |TD|
    |TD| <= 1 -> |TD|^2

    Parameters
    ----------
    absTD : tf.Tensor
        |TD|

    Returns
    -------
    Loss : tf.Tensor
    """
    return tf.where(absTD > 1.0, absTD, tf.math.square(absTD))

def MSE(absTD: tf.Tensor):
    """
    Calculate Squred Error for each (Don't take mean)

    |TD|^2

    Parameters
    ----------
    absTD : tf.Tensor
        |TD|

    Returns
    -------
    Loss : tf.Tensor
    """
    return tf.square(absTD)
