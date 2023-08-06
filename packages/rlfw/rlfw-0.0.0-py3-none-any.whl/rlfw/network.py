import tensorflow as tf

class NoisyDense(tf.keras.layers.Layer):
    """
    Noisy Dense Layer with Factorized Gaussian Noise

    References
    ----------
    https://arxiv.org/abs/1706.10295
    """
    def __init__(self,units,*args,**kwargs):
        """
        Initialize NoisyDense Layer

        Parameters
        ----------
        units : int
            Number of units
        activation : None or "relu" or callable, optional
            Activation function
        seed : int, optional
            Seed for Random Generator
        """
        self.units = units

        seed = kwargs.pop("seed", None)
        if seed is None:
            self.rng = tf.random.Generator.from_non_deterministic_state()
        else:
            self.rng = tf.random.Generator.from_seed(seed)

        self.activation = kwargs.pop("activation",None)
        if self.activation == "relu":
            self.activation = tf.nn.relu

        super().__init__(*args, **kwargs)

    def build(self,input_shape: tf.TensorShape):
        inv_sqrt_p = tf.math.sqrt(1.0/input_shape[-1])
        mu_init = tf.keras.initializers.RandomUniform(minval=-inv_sqrt_p,
                                                      maxval=inv_sqrt_p)
        sigma_init = tf.keras.initializers.Constant(value=0.5*inv_sqrt_p)

        self.w_mu    = self.add_weight(name="w_mu",
                                       shape=(input_shape[-1],self.units),
                                       initializer=mu_init,
                                       trainable=self.trainable)

        self.w_sigma = self.add_weight(name="w_sigma",
                                       shape=(input_shape[-1],self.units),
                                       initializer=sigma_init,
                                       trainable=self.trainable)

        self.b_mu    = self.add_weight(name="b_mu",
                                       shape=(self.units,),
                                       initializer=mu_init,
                                       trainable=self.trainable)

        self.b_sigma = self.add_weight(name="b_sigma",
                                       shape=(self.units,),
                                       initializer=sigma_init,
                                       trainable=self.trainable)

    def _f(self,eps):
        return tf.stop_gradient(tf.math.sign(eps) * tf.math.sqrt(tf.math.abs(eps)))

    @tf.function
    def call(self,inputs, **kwargs):
        eps_in  = self._f(self.rng.normal(shape=(self.w_mu.shape[0],1)))
        eps_out = self._f(self.rng.normal(shape=(1,self.w_mu.shape[1])))
        eps_w = tf.stop_gradient(tf.tensordot(eps_in, eps_out, axes=[[-1],[0]]))
        assert eps_w.shape == self.w_mu.shape, "Factorized Noise shape mismatch"

        w = self.w_mu + self.w_sigma * eps_w
        b = self.b_mu + self.b_sigma * tf.squeeze(eps_out)
        y = tf.tensordot(inputs,w,axes=[[-1],[0]]) + b

        if self.activation:
            y = self.activation(y)
        return y

    def get_config(self):
        return {**super().get_config(),
                "units": self.units,"activation": self.activation}

    def get_weights(self):
        return [self.w_mu.numpy(), self.w_sigma.numpy(),
                self.b_mu.numpy(), self.b_sigma.numpy()]

    def set_weights(self,weights):
        w_mu, w_sigma, b_mu, b_sigma = weights

        self.w_mu.assign(w_mu)
        self.w_sigma.assign(w_sigma)
        self.b_mu.assign(b_mu)
        self.b_sigma.assign(b_sigma)
