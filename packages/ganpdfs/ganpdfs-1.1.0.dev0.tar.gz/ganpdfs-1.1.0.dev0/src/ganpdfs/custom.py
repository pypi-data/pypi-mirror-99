import numpy as np
import tensorflow as tf

from tensorflow.keras import models
from tensorflow.train import Checkpoint
from tensorflow.keras import optimizers
from tensorflow.keras import constraints
from tensorflow.keras import initializers
from tensorflow.keras import backend as K
from tensorflow.keras.layers import Layer
from tensorflow.keras.constraints import Constraint
from tensorflow.keras.initializers import Zeros
from tensorflow.keras.initializers import Identity
from tensorflow.keras.constraints import MinMaxNorm


def wasserstein_loss(y_true, y_pred):
    """Compute the wasserstein loss from the true and predictions.
    The loss function is implemented by multiplying the expected
    label for each sample by the predicted score (element wise),
    then calculating the mean. For more details, refer to:
    https://arxiv.org/abs/1506.05439

    Parameters
    ----------
    y_true : tf.tensor(float)
        list of estimated probabilities for the true samples
    y_pred : tf.tensor(float)
        list of estimated probabilities for the fake samples

    Returns
    -------
    tf.tensor
        Tensor containing the mean of the predictions and the
        true values.
    """
    return K.mean(y_true * y_pred)


def get_optimizer(optimizer):
    """Overwrite keras default parameters for optimizer.

    Parameters
    ----------
    optimizer : dict
        Dictionary containing information on the optimizer.

    Returns
    -------
    tf.keras.optimizers
        Optimizer.
    """

    learning_rate = optimizer.get("learning_rate")
    optimizer_name = optimizer.get("optimizer_name")
    optimizer_class = optimizers.get(optimizer_name)
    optimizer_class.learning_rate = learning_rate
    return optimizer_class


def get_activation(model_params):
    """Extract activation functions from the input parameters.
    This is necessary for advanced activation functions.

    Parameters
    ----------
    model_params : dict
        Dictionary containing information on the Discriminator
        architecture.


    Returns
    -------
    tf.keras.activations
        Activation function.
    """

    if model_params.get("activation") == "elu":
        from tensorflow.keras.layers import ELU
        return ELU(alpha=1.0)
    elif model_params.get("activation") == "relu":
        from tensorflow.keras.layers import ReLU
        return ReLU()
    elif model_params.get("activation") == "leakyrelu":
        from tensorflow.keras.layers import LeakyReLU
        return LeakyReLU(alpha=0.2)
    else: raise ValueError("Activation not available.")


def get_init(kinit_name):
    """Get keras kernel initializers from runcadr."""

    return getattr(initializers, kinit_name)


def save_ckpt(generator, critic, adversarial):
    """Save the training information into a file. This includes but
    not limited to the information on the wieghts and the biases of
    the given network. The GANs model is a combination of three
    different neural networks (generator, critic/discriminator,
    adversarial) and the information on each one of them are saved.

    For more information on the constructor `Checkpoint` from
    the module `tensorflow.train`, refer to
    https://www.tensorflow.org/api_docs/python/tf/train/Checkpoint

    Parameters
    ----------
    generator : ganpdfs.model.WassersteinGanModel.generator
        generator neural network
    critic : ganpdfs.model.WassersteinGanModel.critic
        critic/discriminator neural network
    adversarial : ganpdfs.model.WassersteinGanModel.adversarial
        adversarial neural network

    Returns
    -------
    A load status object, which can be used to make assertions about
    the status of a checkpoint restoration
    """

    checkpoint = Checkpoint(
            critic=critic,
            generator=generator,
            adversarial=adversarial
    )
    return checkpoint


def turn_on_training(critic, generator):
    for layer in critic.layers:
        layer.trainable = True
    for layer in generator.layers:
        layer.trainable = True
    critic.trainable = True
    generator.trainable = True


def load_generator(model_name):
    """Load a saved/trained keras model from a folder.

    Parameters
    ----------
    model_name : tf.keras.Model
        Name of the saved folder.

    Returns
    -------
    tf.keras.Model
        Saved generator model.
    """

    return models.load_model(model_name)


class WeightsClipConstraint(Constraint):
    """Put constraints on the weights of a given layer.

    Parameters
    ----------
    value : float
        Value to which the weights will be bounded on.

    Returns
    -------
    tf.keras.constraints
        Constraint class.
    """

    def __init__(self, value):
        self.value = value

    def __call__(self, weights):
        return K.clip(weights, -self.value, self.value)

    def get_config(self):
        return {"value": self.value}


class GenKinit(initializers.Initializer):
    """Custom kernel initialization."""

    def __init__(self, valmin=-1, valmax=1):
        self.valmin = valmin
        self.valmax = valmax

    def __call__(self, shape, dtype=None):
        initk = tf.random.uniform(
                shape,
                minval=self.valmin,
                maxval=self.valmax,
                dtype=dtype
        )
        return initk

    def get_config(self):
        config = {
                'minval': self.valmin,
                'maxval': self.valmax
        }
        return config


class GradientPenalty(Layer):
    """Calculates the gradient penalty loss for a batch of "averaged" samples.
    In Improved WGANs, the 1-Lipschitz constraint is enforced by adding a term
    to the loss function that penalizes the network if the gradient norm moves
    away from 1. However, it is impossible to evaluate this function at all
    points in the input space. The compromise used in the paper is to choose
    random points on the lines between real and generated samples, and check
    the gradients at these points. Note that it is the gradient w.r.t. the input
    averaged samples, not the weights of the discriminator, that we're penalizing!
    In order to evaluate the gradients, we must first run samples through the
    generator and evaluate the loss. Then we get the gradients of the discri-
    minator w.r.t. the input averaged samples. The l2 norm and penalty can then
    be calculated for this gradient.
    Note that this loss function requires the original averaged samples as input,
    but Keras only supports passing y_true and y_pred to loss functions. To get
    around this, we make a partial() of the function with the average argument,
    and use that for model training.
    """

    def __init__(self, critic, batch, architect, gp_weight, **kwargs):
        self.critic = critic
        self.batch = batch
        self.architect = architect
        self.gp_weight = gp_weight
        super(GradientPenalty, self).__init__(**kwargs)

    def call(self, inputs):
        # Compute Random Weighted Average
        reals, fakes = inputs
        if self.architect == "dnn":
            alpha = K.random_uniform((self.batch, 1, 1))
        elif self.architect == "dcnn":
            alpha = K.random_uniform((self.batch, 1, 1, 1))
        rand_avg = (alpha * reals) + ((1 - alpha) * fakes)

        gradients = K.gradients(
                self.critic(rand_avg),
                [rand_avg]
        )[0]
        gradients_sqr = K.square(gradients)
        gradients_sqr_sum = K.sum(
                gradients_sqr,
                axis=np.arange(1, len(gradients_sqr.shape))
        )
        gradient_l2_norm = K.sqrt(gradients_sqr_sum)
        gradient_penalty = K.square(1 - gradient_l2_norm)
        gradient_penalty *= self.gp_weight
        return K.mean(gradient_penalty)


class AddLatent(Layer):
    """Keras layer that inherates from the keras `Layer` class. This layer
    class basically expands the input latent space tensors to the generator.

    Parameters
    ----------
    latent_vector : np.array
        Input latent vector.
    """

    def __init__(self, latent_vector, **kwargs):
        shape = latent_vector.shape[0]
        index = np.random.choice(shape, shape-1, replace=False)
        self.latent = latent_vector[index]
        super(AddLatent, self).__init__(**kwargs)

    def call(self, inputs):
        result = K.switch(
                K.cast(inputs.shape[0] is not None, tf.bool),
                lambda: inputs + self.latent[:inputs.shape[0]],
                lambda: inputs
        )
        return result


class ExpLatent(Layer):
    """Keras layer that inherates from the keras `Layer` class. This layer
    class basically expands the input latent space tensors to the generator.

    Parameters
    ----------
    output_dim : int
        Size of the output dimension.
    use_bias : bool
        Add or not biases to the output layer.
    """

    def __init__(self, output_dim, use_bias, **kwargs):
        self.use_bias = use_bias
        self.units = output_dim
        self.binitializer = Zeros()
        self.kinitializer = Identity()
        super(ExpLatent, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='kernel',
            shape=(input_shape[-1], self.units),
            initializer=initializers.get(self.kinitializer),
            trainable=False
        )
        if self.use_bias:
            self.bias = self.add_weight(
                name='bias',
                shape=(self.units),
                initializer=self.binitializer,
                trainable=True
            )
        else: self.bias = None
        super(ExpLatent, self).build(input_shape)

    def call(self, inputs):
        output = K.dot(inputs, self.kernel)
        if self.use_bias: output = output + self.bias
        return output


class GenDense(Layer):
    """Custom layer that inherates from the keras `Layer` class. This layer
    class  is proper to the `Generator` and takes the input parameters from
    the input runcard which contains all the parameters for the layer.

    Parameters
    ----------
    output_dim : int
        Size of the output dimension.
    dicparams : dict
        Dictionary containing the layer parameters.
    """

    def __init__(self, output_dim, dicparams, **kwargs):
        const = MinMaxNorm(
                min_value=-dicparams.get("MinNorm", 1),
                max_value=dicparams.get("MaxNorm", 1e-5),
                rate=dicparams.get("NormRate", 1.0),
                axis=0
        )
        bias_init = dicparams.get("bias_initializer", "zeros")
        self.units = output_dim
        self.kconstraint = constraints.get(const)
        self.kinitializer1 = Identity()
        self.kinitializer2 = initializers.get(GenKinit())
        self.binitializer = get_init(bias_init)
        self.use_bias = dicparams.get("use_bias", False)
        self.activation = dicparams.get("activation")
        super(GenDense, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel1 = self.add_weight(
            name='kernel',
            shape=(input_shape[-1], self.units),
            initializer=self.kinitializer1,
            trainable=False
        )
        self.kernel2 = self.add_weight(
            name='kernel',
            shape=(input_shape[-1], self.units),
            initializer=self.kinitializer2,
            trainable=True,
            constraint=self.kconstraint
        )
        if self.use_bias:
            self.bias = self.add_weight(
                name='bias',
                shape=(self.units),
                initializer=self.binitializer,
                trainable=True
            )
        else: self.bias = None
        super(GenDense, self).build(input_shape)

    def call(self, inputs):
        output = K.dot(inputs, self.kernel1 + self.kernel2)
        if self.use_bias: output = output + self.bias
        return output


class ExtraDense(Layer):
    """Keras layer that inherates from the keras `Layer` class. This layer
    class takes the input parameters from the input runcard which contains
    all the parameters for the layer.

    Parameters
    ----------
    output_dim : int
        Size of the output dimension.
    dicparams : dict
        Dictionary containing the layer parameters.
    """

    def __init__(self, output_dim, dicparams, **kwargs):
        wc = WeightsClipConstraint(dicparams.get("weights_constraints")) \
                if output_dim != 1 else None
        self.units = output_dim
        self.kconstraint = constraints.get(wc)
        self.binitializer = get_init(dicparams.get("bias_initializer", "zeros"))
        self.kinitializer = get_init(dicparams.get("kernel_initializer"))
        self.use_bias = dicparams.get("use_bias", False)
        self.activation = dicparams.get("activation")
        super(ExtraDense, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name='kernel',
            shape=(input_shape[-1], self.units),
            initializer=self.kinitializer,
            trainable=True,
            constraint=self.kconstraint
        )
        if self.use_bias:
            self.bias = self.add_weight(
                name='bias',
                shape=(self.units),
                initializer=self.binitializer,
                trainable=True
            )
        else: self.bias = None
        super(ExtraDense, self).build(input_shape)

    def call(self, inputs):
        output = K.dot(inputs, self.kernel)
        if self.use_bias: output = output + self.bias
        return output


class ConvolutePDF(Layer):
    """Convolute the output of the previous layer with
    a subsample of the input/prior replica.

    Parameters
    ----------
    pdf: np.array
        Array of PDF grids
    """

    def __init__(self, pdf, **kwargs):
        self.pdf = K.constant(pdf[0])
        super(ConvolutePDF, self).__init__(**kwargs)

    def compute_output_shape(self, input_shape):
        return (None, self.pdf.shape[1], self.pdf.shape[2])

    def call(self, previous_layer):
        mult = previous_layer * self.pdf
        return mult


class ConvXgrid(Layer):
    """Convolute the output of the previous layer with the input x-grid.
    """

    def __init__(self, output_dim, xval, kinit="glorot_uniform", **kwargs):
        self.units = output_dim
        self.xval = K.constant(xval)
        self.kernel_initializer = initializers.get(kinit)
        super(ConvXgrid, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name="kernel",
            shape=(K.int_shape(self.xval)[0], input_shape[1], self.units),
            initializer=self.kernel_initializer,
            trainable=True,
        )
        super(ConvXgrid, self).build(input_shape)

    def call(self, x):
        xres = tf.tensordot(x, self.xval, axes=0)
        xfin = tf.tensordot(xres, self.kernel, axes=([1, 2], [0, 1]))
        return xfin

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.units)


class PreprocessFit(Layer):
    """Add preprocessing to the output of the previous layer. This is
    expected to assure the PDF-like behavior of the generated samples.

    Parameters
    ----------
    xval: np.array
        Array of x-grid
    """

    def __init__(self, xval, trainable=True, kinit="ones", **kwargs):
        self.xval = xval
        self.trainable = trainable
        self.kernel_initializer = initializers.get(kinit)
        super(PreprocessFit, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = self.add_weight(
            name="kernel",
            shape=(2,),
            initializer=self.kernel_initializer,
            trainable=self.trainable,
        )
        super(PreprocessFit, self).build(input_shape)

    def compute_output_shape(self, input_shape):
        return input_shape

    def call(self, pdf):
        xres = self.xval ** self.kernel[0]
        zres = (1 - self.xval) ** self.kernel[1]
        return pdf * xres * zres
