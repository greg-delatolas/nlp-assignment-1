from . import clslib, experiment, utils

# The Bayesian error-analysis helpers require optional JAX/NumPyro packages.
# Keep the core classification code importable when those extras are absent.
try:
    from . import analysis
except ModuleNotFoundError as error:
    if error.name not in {"jax", "numpyro", "arviz"}:
        raise
    analysis = None
