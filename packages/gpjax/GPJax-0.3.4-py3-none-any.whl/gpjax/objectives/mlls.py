from typing import Callable

import jax.numpy as jnp
from multipledispatch import dispatch
from tensorflow_probability.substrates.jax import distributions as tfd

from ..gps import ConjugatePosterior, NonConjugatePosterior
from ..kernels import gram
from ..likelihoods import link_function
from ..parameters.priors import evaluate_prior, prior_checks
from ..types import Array, Dataset
from ..utils import I, concat_dictionaries


@dispatch(ConjugatePosterior)
def marginal_ll(
    gp: ConjugatePosterior,
    transform: Callable,
    negative: bool = False,
) -> Callable:
    r"""
    Compute :math:`\log p(y | x, \theta) for a conjugate, or exact, Gaussian process.
    Args:
        x: A set of N X M inputs
        y: A set of N X 1 outputs
    Returns: A multivariate normal distribution
    """

    def mll(params: dict, training: Dataset, priors: dict = None, static_params: dict = None):
        x, y = training.X, training.y
        params = transform(params)
        if static_params:
            params = concat_dictionaries(params, transform(static_params))
        mu = gp.prior.mean_function(x)
        gram_matrix = gram(gp.prior.kernel, x, params)
        gram_matrix += params["obs_noise"] * I(x.shape[0])
        L = jnp.linalg.cholesky(gram_matrix)
        random_variable = tfd.MultivariateNormalTriL(mu, L)

        log_prior_density = evaluate_prior(params, priors)
        constant = jnp.array(-1.0) if negative else jnp.array(1.0)
        return constant * (random_variable.log_prob(y.squeeze()).mean() + log_prior_density)

    return mll


@dispatch(NonConjugatePosterior)
def marginal_ll(
    gp: NonConjugatePosterior,
    transform: Callable,
    negative: bool = False,
    jitter: float = 1e-6,
) -> Callable:
    def mll(
        params: dict,
        training: Dataset,
        priors: dict = {"latent": tfd.Normal(loc=0.0, scale=1.0)},
        static_params: dict = None,
    ):
        x, y = training.X, training.y
        n = training.n
        params = transform(params)
        if static_params:
            params = concat_dictionaries(params, transform(static_params))
        link = link_function(gp.likelihood)
        gram_matrix = gram(gp.prior.kernel, x, params)
        gram_matrix += I(n) * jitter
        L = jnp.linalg.cholesky(gram_matrix)
        F = jnp.matmul(L, params["latent"])
        rv = link(F)
        ll = jnp.sum(rv.log_prob(y))

        priors = prior_checks(gp, priors)
        log_prior_density = evaluate_prior(params, priors)
        constant = jnp.array(-1.0) if negative else jnp.array(1.0)
        return constant * (ll + log_prior_density)

    return mll
