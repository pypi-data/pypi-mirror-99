import tensorflow as tf

from rlfw.network import NoisyDense


class QFunction(tf.keras.Model):
    def __init__(self, state_shape, act_dim,
                 fully_connected = (100, 100, 100), *,
                 Noisy = False,
                 dtype = tf.float32):
        super().__init__(dtype=dtype)

        FC = NoisyDense if Noisy else tf.keras.layers.Dense

        state_size = 1
        if isinstance(state_shape, int):
            state_size *= state_shape
        else:
            for i in state_shape:
                state_shape *= i

        act_size = 1
        if isinstance(act_dim, int):
            act_size *= act_dim
        else:
            for i in act_dim:
                act_size *= i

        self.i = tf.keras.layers.InputLayer(input_shape=state_size+act_size)
        self.fc = [FC(u, activation="relu") for u in fully_connected]
        self.o = FC(1)

    @tf.function
    def _call(self, state: tf.Tensor, action: tf.Tensor):
        inputs = self.i(tf.concat([state, action], axis=1))

        for L in self.fc:
            inputs = L(inputs)

        return self.o(inputs)

    def call(self, inputs, training=False):
        state, action = inputs
        state = tf.constant(state, dtype=self.dtype)
        action = tf.constant(action, dtype=self.dtype)
        return self._call(state, action)

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
        return {"state_shape": self.i.get_config()["batch_input_shape"][1:],
                "act_dim": 0,
                "fully_connected": (L.units for L in self.fc),
                "Noisy": isinstance(self.fc[0], NoisyDense)}
