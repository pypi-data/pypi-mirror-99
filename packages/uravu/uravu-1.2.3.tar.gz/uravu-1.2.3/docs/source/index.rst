.. uravu documentation master file, created by
   sphinx-quickstart on Fri Feb 21 09:20:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

making Bayesian modelling easy(er)
==================================

:py:mod:`uravu` is about the relationship between some data and a function that may be used to describe the data.

The aim of :py:mod:`uravu` is to make using the **amazing** Bayesian inference libraries that are available in Python as easy as :func:`scipy.optimize.curve_fit`.
Therefore enabling many more to make use of these exciting tools and powerful libraries.
Plus, we have some nice plotting functionalities available in the :py:mod:`~uravu.plotting` module, capable of generating publication quality figures.

.. image:: sample_fig.png
  :alt: An example of the type of figures that uravu can produce. Showing straight line distribution with increasing uncertainty.

In an effort to make the :py:mod:`uravu` API friendly to those new to Bayesian inference, :py:mod:`uravu` is *opinionated*, making assumptions about priors amoung other things.
However, we have endevoured to make it straightforward to ignore these opinions.

In addition to the library and API, we also have some `basic tutorials`_ discussing how Bayesian inference methods can be used in the analysis of data.

:py:mod:`uravu` is under active development, more details of which can be found on `Github`_.

Bayesian inference in Python
----------------------------

There are a couple of fantastic Bayesian inference libraries available in Python that :py:mod:`uravu` makes use of:

- :py:mod:`emcee`: enables the use of the `Goodman & Weare’s Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler`_ to evaluate the structure of the model parameter posterior distributions,
- :py:mod:`dynesty`: implements the `nested sampling`_ and `dynamic nested sampling`_ algorithms for evidence estimation.

Where :py:attr:`function` is some user-defined function, :py:attr:`abscissa` is x-data, :py:attr:`ordinate` is y-data, and :py:attr:`ordinate_error` is y-uncertainty, getting an :py:class:`uravu.relationship.Relationship` running is as simple as.

.. code-block:: python

   from uravu.relationship import Relationship

   modeller = Relationship(function, abscissa, ordinate, ordinate_error=ordinate_error)
   modeller.max_likelihood('mini')
   modeller.mcmc()
   modeller.nested_sampling()

.. _basic tutorials: ./tutorials.html
.. _Github: https://github.com/arm61/uravu
.. _Goodman & Weare’s Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler: https://doi.org/10.2140/camcos.2010.5.65
.. _nested sampling: https://doi.org/10.1063/1.1835238
.. _dynamic nested sampling: https://doi.org/10.1007/s11222-018-9844-0

.. toctree::
   :hidden:
   :maxdepth: 2

   installation
   getting_started.ipynb
   tutorials
   faq
   api

Searching
=========

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
