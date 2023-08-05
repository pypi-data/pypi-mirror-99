=======================================
ChainsAddiction 
=======================================

ChainsAddiction is a tool for simple training discrete-time Hidden Markov
Models. It is written in C and features a numpy-based Python extension
module.

Installation
=======================================

Clone this repository, change to its root directory and issue

.. code-block:: bash

    pip install .

On macOS this should work perfectly find. On GNU/Linux it might happend that
you see an error related to missing a Python.h file. If you see such an error,
you probabliy missing you distributions Python development package. In most
cases this package is named either `python3-dev` or `python3-devel`. You need
to install it with your package manager. On Fedora, for example, this would
look like:

.. code-block:: bash

    sudo yum install python3-devel


Working with chainsaddiction 
=======================================
Calling chainsaddiction from Python is simple as pie. You just need to import
it:

.. code-block:: python

    import chainsaddiction as ca
    ca.hmm_poisson_fit_em(trainig_data, m_states, init_means, init_tpm,
                          int_sd, max_iter=1000, tol=1e-5)

Notes
---------------------------------------
* Currently only algorithms for Poisson-distributed HMMs are implemented.
* ChainsAddiction does not support Python 2. Specifically, it requires `Python >= 3.7` and `numpy >= 1.16`.
