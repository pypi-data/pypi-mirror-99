import tensorflow as tf

from rlfw.network import NoisyDense


class QFunction(tf.keras.Model):
    def __init__(self, state_shape, act_size,
                 fully_connected = (100, 100, 100), *,
                 Noisy = False, Duelling = False):
        super().__init__()

        FC = NoisyDense if Noisy else tf.keras.layers.Dense

        self.i = tf.keras.layers.InputLayer(input_shape = state_shape)

        self.fc = [FC(u, activation="relu") for u in fully_connected]

        # Must be Python object, to evaluate only once in @tf.function
        self.duel = bool(Duelling)
        if Duelling:
            self.A = [FC(u, activation="relu") for u in Duelling]
            self.A.append(FC(act_size))

            self.V = [FC(u, activation="relu") for u in Duelling]
            self.V.append(FC(1))

        self.o = FC(act_size)


    @tf.function
    def _call(self, state):
        state = self.i(state)

        for L in self.fc:
            state = L(state)

        if self.duel:
            a = state
            v = state

            for L in self.A:
                a = L(a)
            a = a - tf.stop_gradient(tf.reduce_mean(a, axis=1, keepdims=True))

            for L in self.V:
                v = L(v)
            v = tf.expand_dims(v, axis=1)

            state = v + a

        return self.o(state)

    def call(self, state, training=False):
        state = tf.constant(state)
        return self._call(state)

    def get_weights(self):
        weights = []

        weights.append([L.get_weights() for L in self.fc])

        weights.append([L.get_weights() for L in self.A] if self.duel else None)
        weights.append([L.get_weights() for L in self.V] if self.duel else None)

        weights.append(self.o.get_weights())

        return weights

    def set_weights(self, weights):
        fc, A, V, output = weights

        for L, w in zip(self.fc, fc):
            L.set_weights(w)

        if self.duel:
            for L, w in zip(self.A, A):
                L.set_weights(w)

            for L, w in zip(self.V, V):
                L.set_weights(w)

        self.o.set_weights(output)

    def get_config(self):
        return {"state_shape": self.i.get_config()["batch_input_shape"][1:],
                "act_size": self.o.units,
                "fully_connected": (L.units for L in self.fc),
                "Noisy": isinstance(self.fc[0], NoisyDense),
                "Duelling": self.duel and (L.units for L in self.A)}
