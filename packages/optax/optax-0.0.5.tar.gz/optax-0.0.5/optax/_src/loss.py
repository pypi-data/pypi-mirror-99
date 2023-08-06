# Lint as: python3
# Copyright 2019 DeepMind Technologies Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Standard losses used in optimisation.

We provide implementations of the most canonical losses used in deep
learning. These operate transparently on batches, and do not perform any
reduction over the batch dimensions, leaving it to the user to, for instance,
mean or sum losses across batch dimensions.
"""

from typing import Optional

import chex
import jax
import jax.numpy as jnp
from optax._src import utils


def l2_loss(
    predictions: chex.Array,
    targets: Optional[chex.Array] = None,
) -> chex.Array:
  """Calculates the L2 loss for a set of predictions.

  Note: the 0.5 term is standard in "Pattern Recognition and Machine Learning"
  by Bishop, but not "The Elements of Statistical Learning" by Tibshirani.

  References:
    [Chris Bishop, 2006](https://bit.ly/3eeP0ga)

  Args:
    predictions: a vector of arbitrary shape.
    targets: a vector of shape compatible with predictions; if not provides
      then it is assumed to be zero.

  Returns:
    the squared error loss.
  """
  chex.assert_type([predictions], float)
  errors = (predictions - targets) if (targets is not None) else predictions
  return 0.5 * (errors)**2


def huber_loss(
    predictions: chex.Array,
    targets: Optional[chex.Array] = None,
    delta: float = 1.) -> chex.Array:
  """Huber loss, similar to L2 loss close to zero, L1 loss away from zero.

  If gradient descent is applied to the `huber loss`, it is equivalent to
  clipping gradients of an `l2_loss` to `[-delta, delta]` in the backward pass.

  References:
    [Huber, 1964](www.projecteuclid.org/download/pdf_1/euclid.aoms/1177703732)

  Args:
    predictions: a vector of arbitrary shape.
    targets: a vector of shape compatible with predictions; if not provides
      then it is assumed to be zero.
    delta: the bounds for the huber loss transformation, defaults at 1.

  Returns:
    a vector of same shape of `x`.
  """
  chex.assert_type([predictions], float)
  errors = (predictions - targets) if (targets is not None) else predictions
  # 0.5 * err^2                  if |err| <= d
  # 0.5 * d^2 + d * (|err| - d)  if |err| > d
  abs_errors = jnp.abs(errors)
  quadratic = jnp.minimum(abs_errors, delta)
  # Same as max(abs_x - delta, 0) but avoids potentially doubling gradient.
  linear = abs_errors - quadratic
  return 0.5 * quadratic ** 2 + delta * linear


def smooth_labels(
    labels: chex.Array,
    alpha: float,
) -> jnp.ndarray:
  """Apply label smoothing.

  Label smoothing is often used in combination with a cross-entropy loss.
  Smoothed labels favour small logit gaps, and it has been shown that this can
  provide better model calibration by preventing overconfident predictions.

  References:
    [Müller et al, 2019](https://arxiv.org/pdf/1906.02629.pdf)

  Args:
    labels: one hot labels to be smoothed.
    alpha: the smoothing factor, the greedy category with be assigned
      probability `(1-alpha) + alpha / num_categories`

  Returns:
    a smoothed version of the one hot input labels.

  """
  chex.assert_type([labels], float)
  num_categories = labels.shape[-1]
  return (1.0 - alpha) * labels + alpha / num_categories


def sigmoid_binary_cross_entropy(logits, labels):
  """Computes sigmoid cross entropy given logits and multiple class labels.

  Measures the probability error in discrete classification tasks in which
  each class is an independent binary prediction and different classes are
  not mutually exclusive. This may be used for multilabel image classification
  for instance a model may predict that an image contains both a cat and a dog.

  References:
    [Goodfellow et al, 2016](http://www.deeplearningbook.org/contents/prob.html)

  Args:
    logits: unnormalized log probabilities.
    labels: the probability for that class.

  Returns:
    a sigmoid cross entropy loss.
  """
  chex.assert_equal_shape([logits, labels])
  chex.assert_type([logits, labels], float)
  log_p = jax.nn.log_sigmoid(logits)
  # log(1 - sigmoid(x)) = log_sigmoid(-x), the latter more numerically stable
  log_not_p = jax.nn.log_sigmoid(-logits)
  return -labels * log_p - (1. - labels) * log_not_p


def softmax_cross_entropy(
    logits: chex.Array,
    labels: chex.Array,
) -> chex.Array:
  """Computes the softmax cross entropy between sets of logits and labels.

  Measures the probability error in discrete classification tasks in which
  the classes are mutually exclusive (each entry is in exactly one class).
  For example, each CIFAR-10 image is labeled with one and only one label:
  an image can be a dog or a truck, but not both.

  References:
    [Goodfellow et al, 2016](http://www.deeplearningbook.org/contents/prob.html)

  Args:
    logits: unnormalized log probabilities.
    labels: a valid probability distribution (non-negative, sum to 1), e.g a
      one hot encoding of which class is the correct one for each input.

  Returns:
    the cross entropy loss.
  """
  chex.assert_equal_shape([logits, labels])
  chex.assert_type([logits, labels], float)
  return -jnp.sum(labels * jax.nn.log_softmax(logits, axis=-1), axis=-1)


def cosine_distance(
    predictions: chex.Array,
    targets: chex.Array,
    epsilon: float = 0.,
) -> chex.Array:
  r"""Computes the cosine distance between targets and predictions.

  The cosine **similarity** is a measure of similarity between vectors defined
  as the cosine of the angle between them, which is also the inner product of
  those vectors normalized to have unit norm. The cosine **distance**,
  implemented here, measures instead the **dissimilarity** as `1 - cos(\theta)`.

  References:
    [Wikipedia, 2021](https://en.wikipedia.org/wiki/Cosine_similarity)

  Args:
    predictions: The predicted vector.
    targets: Ground truth target vector.
    epsilon: minimum norm for terms in the denominator of the cosine similarity.

  Returns:
    cosine similarity values.
  """
  chex.assert_equal_shape([targets, predictions])
  chex.assert_type([targets, predictions], float)
  # vectorize norm fn, to treat all dimensions except the last as batch dims.
  batched_norm_fn = jnp.vectorize(
      utils.safe_norm, signature='(k)->()', excluded={1})
  # normalise the last dimension of targets and predictions.
  unit_targets = targets / jnp.expand_dims(
      batched_norm_fn(targets, epsilon), axis=-1)
  unit_predictions = predictions / jnp.expand_dims(
      batched_norm_fn(predictions, epsilon), axis=-1)
  # cosine distance = 1 - cosine similarity.
  return 1. - jnp.sum(unit_targets * unit_predictions, axis=-1)
