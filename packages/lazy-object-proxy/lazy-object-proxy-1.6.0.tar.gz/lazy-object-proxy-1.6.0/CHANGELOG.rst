
Changelog
=========

1.6.0 (2021-03-22)
------------------

* Added support for async special methods (``__aiter__``, ``__anext__``,
  ``__await__``, ``__aenter__``, ``__aexit__``).
  These are used in the ``async for``, ``await` and ``async with`` statements.

  Note that ``__await__`` returns a wrapper that tries to emulate the crazy
  stuff going on in the ceval loop, so there will be a small performance overhead.
* Added the ``__resolved__`` property. You can use it to check if the factory has
  been called.

1.5.2 (2020-11-26)
------------------

* Added Python 3.9 wheels.
* Removed Python 2.7 Windows wheels
  (not supported on newest image with Python 3.9).

1.5.1 (2020-07-22)
------------------

* Added ARM64 wheels (manylinux2014).

1.5.0 (2020-06-05)
------------------

* Added support for ``__fspath__``.
* Dropped support for Python 3.4.

1.4.3 (2019-10-26)
------------------

* Added binary wheels for Python 3.8.
* Fixed license metadata.

1.4.2 (2019-08-22)
------------------

* Included a ``pyproject.toml`` to allow users install the sdist with old python/setuptools, as the
  setuptools-scm dep will be fetched by pip instead of setuptools.
  Fixes `#30 <https://github.com/ionelmc/python-lazy-object-proxy/issues/30>`_.

1.4.1 (2019-05-10)
------------------

* Fixed wheels being built with ``-coverage`` cflags. No more issues about bogus ``cext.gcda`` files.
* Removed useless C file from wheels.
* Changed ``setup.py`` to use setuptools-scm.

1.4.0 (2019-05-05)
------------------

* Fixed ``__mod__`` for the slots backend. Contributed by Ran Benita in
  `#28 <https://github.com/ionelmc/python-lazy-object-proxy/pull/28>`_.
* Dropped support for Python 2.6 and 3.3. Contributed by "hugovk" in
  `#24 <https://github.com/ionelmc/python-lazy-object-proxy/pull/24>`_.

1.3.1 (2017-05-05)
------------------

* Fix broken release (``sdist`` had a broken ``MANIFEST.in``).

1.3.0 (2017-05-02)
------------------

* Speed up arithmetic operations involving ``cext.Proxy`` subclasses.

1.2.2 (2016-04-14)
------------------

* Added `manylinux <https://www.python.org/dev/peps/pep-0513/>`_ wheels.
* Minor cleanup in readme.

1.2.1 (2015-08-18)
------------------

* Fix a memory leak (the wrapped object would get bogus references). Contributed by Astrum Kuo in
  `#10 <https://github.com/ionelmc/python-lazy-object-proxy/pull/10>`_.

1.2.0 (2015-07-06)
------------------

* Don't instantiate the object when __repr__ is called. This aids with debugging (allows one to see exactly in
  what state the proxy is).

1.1.0 (2015-07-05)
------------------

* Added support for pickling. The pickled value is going to be the wrapped object *without* any Proxy container.
* Fixed a memory management issue in the C extension (reference cycles weren't garbage collected due to improper
  handling in the C extension). Contributed by Alvin Chow in
  `#8 <https://github.com/ionelmc/python-lazy-object-proxy/pull/8>`_.

1.0.2 (2015-04-11)
-----------------------------------------

* First release on PyPI.
