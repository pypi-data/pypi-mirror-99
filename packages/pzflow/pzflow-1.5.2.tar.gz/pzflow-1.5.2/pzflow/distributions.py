from typing import Sequence, Tuple
import numpy as onp
import sys

import jax.numpy as np
from jax import random
from jax.scipy.special import gammaln

from pzflow.bijectors import Pytree

epsilon = sys.float_info.epsilon


def _mahalanobis_and_logdet(x, cov):
    """Calculate mahalanobis distance and log_det of cov.

    Uses scipy method, explained here:
    http://gregorygundersen.com/blog/2019/10/30/scipy-multivariate/
    """
    vals, vecs = np.linalg.eigh(cov)
    U = vecs * np.sqrt(1 / vals[..., None])
    maha = np.square(U @ x[..., None]).reshape(x.shape[0], -1).sum(axis=1)
    log_det = np.log(vals).sum(axis=-1)
    return maha, log_det


class Normal:
    """A multivariate Gaussian distribution with mean zero and unit variance."""

    def __init__(self, input_dim: int):
        """
        Parameters
        ----------
        input_dim : int
            The dimension of the distribution.
        """
        self.input_dim = input_dim

        # save dist info
        self._params = ()
        self.info = ("Normal", (input_dim,))

    def log_prob(
        self, params: Pytree, inputs: np.ndarray, cov: np.ndarray = None
    ) -> np.ndarray:
        """Calculates log probability density of inputs.

                Parameters
                ----------
                params : a Jax pytree
                    Empty pytree -- this distribution doesn't have learnable parameters.
                    This parameter is present to ensure a consistent interface.
                inputs : np.ndarray
                    Input data for which log probability density is calculated.
                cov : np.ndarray, default=None
                    Covariance matrix for the log probability calculation.

                Returns
                -------
                np.ndarray
                    Device array of shape (inputs.shape[0],).
        WARNING
                Notes
                -----
                jax.scipy.stats.multivariate_normal.log_pdf doesn't seem to work with
                different covariances for each input. To get around this, I implemented
                the method from the original scipy code.
                See:
                https://github.com/scipy/scipy/blob/v1.6.0/scipy/stats/_multivariate.py
                or
                http://gregorygundersen.com/blog/2019/10/30/scipy-multivariate/
        """
        if cov is None:
            maha = (inputs ** 2).sum(axis=1)
            log_det = 0.0
        else:
            maha, log_det = _mahalanobis_and_logdet(inputs, cov)

        log_prob = -0.5 * (inputs.shape[-1] * np.log(2 * np.pi) + log_det + maha)
        return log_prob

    def sample(self, params: Pytree, nsamples: int, seed: int = None) -> np.ndarray:
        """Returns samples from the distribution.

        Parameters
        ----------
        params : a Jax pytree
            Empty pytree -- this distribution doesn't have learnable parameters.
            This parameter is present to ensure a consistent interface.
        nsamples : int
            The number of samples to be returned.
        seed : int, optional
            Sets the random seed for the samples.

        Returns
        -------
        np.ndarray
            Device array of shape (nsamples, self.input_dim).
        """
        seed = onp.random.randint(1e18) if seed is None else seed
        return random.multivariate_normal(
            key=random.PRNGKey(seed),
            mean=np.zeros(self.input_dim),
            cov=np.identity(self.input_dim),
            shape=(nsamples,),
        )


class Tdist:
    """A multivariate T distribution with mean zero and unit scale matrix."""

    def __init__(self, input_dim: int):
        """
        Parameters
        ----------
        input_dim : int
            The dimension of the distribution.
        """
        self.input_dim = input_dim

        # save dist info
        self._params = np.log(30.0)
        self.info = ("Tdist", (input_dim,))

    def log_prob(self, params: Pytree, inputs: np.ndarray) -> np.ndarray:
        """Calculates log probability density of inputs.

        Uses method explained here:
        http://gregorygundersen.com/blog/2020/01/20/multivariate-t/

        Parameters
        ----------
        params : float
            The degrees of freedom (nu) of the t-distribution.
        inputs : np.ndarray
            Input data for which log probability density is calculated.

        Returns
        -------
        np.ndarray
            Device array of shape (inputs.shape[0],).
        """
        cov = np.identity(self.input_dim)
        nu = np.exp(params)
        maha, log_det = _mahalanobis_and_logdet(inputs, cov)
        t = 0.5 * (nu + self.input_dim)
        A = gammaln(t)
        B = gammaln(0.5 * nu)
        C = self.input_dim / 2.0 * np.log(nu * np.pi)
        D = 0.5 * log_det
        E = -t * np.log(1 + (1.0 / nu) * maha)

        return A - B - C - D + E

    def sample(self, params: Pytree, nsamples: int, seed: int = None) -> np.ndarray:
        """Returns samples from the distribution.

        Parameters
        ----------
        params : float
            The degrees of freedom (nu) of the t-distribution.
        nsamples : int
            The number of samples to be returned.
        seed : int, optional
            Sets the random seed for the samples.

        Returns
        -------
        np.ndarray
            Device array of shape (nsamples, self.input_dim).
        """
        mean = np.zeros(self.input_dim)
        nu = np.exp(params)

        seed = onp.random.randint(1e18) if seed is None else seed
        rng = onp.random.default_rng(int(seed))
        x = np.array(rng.chisquare(nu, nsamples) / nu)
        z = random.multivariate_normal(
            key=random.PRNGKey(seed),
            mean=np.zeros(self.input_dim),
            cov=np.identity(self.input_dim),
            shape=(nsamples,),
        )
        samples = mean + z / np.sqrt(x)[:, None]
        return samples


class Uniform:
    """A multivariate uniform distribution."""

    def __init__(self, *ranges):
        """
        Parameters
        ----------
        ranges : list or tuple
            List of maximum and minimum for each dimension.
            The overall dimension is inferred from the number of ranges provided.
        """

        # validate inputs
        ranges = np.atleast_2d(ranges)
        if ranges.shape[1] != 2:
            raise ValueError("ranges must be tuple or list of (min, max)")

        # save min and max of each dimension
        mins, maxes = ranges[:, 0], ranges[:, 1]

        # make sure all the minima are less than the maxima
        if not all(mins < maxes):
            raise ValueError("Range minima must be less than maxima.")

        # save the ranges
        self.mins = mins
        self.maxes = maxes

        # save distribution info
        self.input_dim = ranges.shape[0]
        self._params = ()
        self.info = ("Uniform", (*ranges,))

    def log_prob(self, params: Pytree, inputs: np.ndarray) -> np.ndarray:
        """Calculates log probability density of inputs.

        Parameters
        ----------
        params : Jax Pytree
            Empty pytree -- this distribution doesn't have learnable parameters.
            This parameter is present to ensure a consistent interface.
        inputs : np.ndarray
            Input data for which log probability density is calculated.

        Returns
        -------
        np.ndarray
            Device array of shape (inputs.shape[0],).
        """

        # which inputs are inside the support of the distribution
        mask = (
            ((inputs >= self.mins) & (inputs <= self.maxes)).astype(float).prod(axis=-1)
        )

        # calculate log_prob
        prob = mask / (self.maxes - self.mins).prod()
        prob = np.where(prob == 0, epsilon, prob)
        log_prob = np.log(prob)

        return log_prob

    def sample(self, params: Pytree, nsamples: int, seed: int = None) -> np.ndarray:
        """Returns samples from the distribution.

        Parameters
        ----------
        params : a Jax pytree
            Empty pytree -- this distribution doesn't have learnable parameters.
            This parameter is present to ensure a consistent interface.
        nsamples : int
            The number of samples to be returned.
        seed : int, optional
            Sets the random seed for the samples.

        Returns
        -------
        np.ndarray
            Device array of shape (nsamples, self.input_dim).
        """
        seed = onp.random.randint(1e18) if seed is None else seed
        samples = random.uniform(
            random.PRNGKey(seed),
            shape=(nsamples, len(self.maxes)),
            minval=self.mins,
            maxval=self.maxes,
        )
        return np.array(samples)


class Joint:
    """A joint distribution built from other distributions."""

    def __init__(self, *inputs):
        """
        Parameters
        ----------
        inputs
            A list of distributions, or a Joint info object.
        """

        # if Joint info provided, use that for setup
        if inputs[0] == "Joint info":
            self.dists = [globals()[dist[0]](*dist[1]) for dist in inputs[1]]
        # otherwise, assume it's a list of distributions
        else:
            self.dists = inputs

        # save info
        self._params = [dist._params for dist in self.dists]
        self.input_dim = sum([dist.input_dim for dist in self.dists])
        self.info = ("Joint", ("Joint info", [dist.info for dist in self.dists]))

        # save the indices at which inputs will be split for log_prob
        # they must be concretely saved ahead-of-time so that jax trace
        # works properly when jitting
        self._splits = np.cumsum(np.array([dist.input_dim for dist in self.dists]))[:-1]

    def log_prob(self, params: Pytree, inputs: np.ndarray) -> np.ndarray:
        """Calculates log probability density of inputs.

        Parameters
        ----------
        params : Jax Pytree
            Parameters for the distributions.
        inputs : np.ndarray
            Input data for which log probability density is calculated.

        Returns
        -------
        np.ndarray
            Device array of shape (inputs.shape[0],).
        """

        # split inputs for corresponding distribution
        inputs = np.split(inputs, self._splits, axis=1)

        # calculate log_prob with respect to each sub-distribution,
        # then sum all the log_probs for each input
        log_prob = np.hstack(
            [
                self.dists[i].log_prob(params[i], inputs[i]).reshape(-1, 1)
                for i in range(len(self.dists))
            ]
        ).sum(axis=1)

        return log_prob

    def sample(self, params: Pytree, nsamples: int, seed: int = None) -> np.ndarray:
        """Returns samples from the distribution.

        Parameters
        ----------
        params : a Jax pytree
            Parameters for the distributions.
        nsamples : int
            The number of samples to be returned.
        seed : int, optional
            Sets the random seed for the samples.

        Returns
        -------
        np.ndarray
            Device array of shape (nsamples, self.input_dim).
        """

        seed = onp.random.randint(1e18) if seed is None else seed
        seeds = random.randint(random.PRNGKey(seed), (len(self.dists),), 0, int(1e9))
        samples = np.hstack(
            [
                self.dists[i]
                .sample(params[i], nsamples, seeds[i])
                .reshape(nsamples, -1)
                for i in range(len(self.dists))
            ]
        )

        return samples