import tensorflow as tf

class HyperParameter:
    def __init__(self, name):
        self.name = name

    def get_value(self, step=None):
        v = self._get_value()
        if step is not None:
            tf.summary.scalar(f"HyperParameter/{self.name}", data=v, step=step)
        return v

    def _get_value(self):
        raise NotImplementedError

class ConstantParameter(HyperParameter):
    def __init__(self, name, value, *, dtype=None):
        super().__init__(name)
        self.value = tf.constant(value, dtype=dtype)

    @tf.function
    def _get_value(self):
        return self.value



class LinearAnnealingParameter(HyperParameter):
    def __init__(self, name, start, step, stop, *, dtype=None):
        """
        Initialize LinearAnnealingParameter

        Parameters
        ----------
        name : str
            Name of parameter
        start : number
            Start value of this hyperparameter
        step : number
            Step size for linear increment (decriment)
        stop : number
            Stop value of this hyperparameter
        """
        super().__init__(name)
        self.value = tf.Variable(start, dtype=dtype)
        self.step = tf.constant(step)
        self.stop = tf.constant(stop)

        if step > 0:
            self._f = tf.math.minimum
        else:
            self._f = tf.math.maximum

    @tf.function
    def _get_value(self):
        value = tf.identity(self.value)
        self.value.assign(self._f(value+self.step, self.stop))
        return value
