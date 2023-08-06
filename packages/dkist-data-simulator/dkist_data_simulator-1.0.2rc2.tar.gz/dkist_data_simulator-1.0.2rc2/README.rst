A header generator and FITS file creator for DKIST data
-------------------------------------------------------

This package is designed to generate sets of FITS files which represent DKIST level 0 and level 1 data.
These generated data should not be considered as a promise of what will be delivered when real data is obtained, these products are still a work in progress.

Using
-----

Generating Pesudo Random Data
#############################

The simplest way to generate data is to to use the `dkist_data_simulator.spec122.Spec122Dataset` or `dkist_data_simulator.spec214.Spec214Dataset` classes.

To generate a header::

  >>> from dkist_data_simulator.spec122 import Spec122Dataset
  >>> ds = Spec122Dataset(dataset_shape=(1, 512, 512), array_shape=(1, 512, 512), time_delta=10)
  >>> ds.header()

A complete list of headers for all frames in the dataset can be generated with the ``generate_headers`` method.

It is also possible to iterate over a dataset, this changes the ``.index`` property.

This can be used to generate a sequence of headers one at a time::

  >>> header_generator = (d.header() for d in ds)

It can also be used to generate files in memory::

  >>> import io
  >>> file_generator = (d.file(io.BytesIO()) for d in ds)


Customising the Generated Data
##############################

To customise the data being generated, subclass a dataset.
To add new headers, either the ``add_constant_key`` method, or the ``add_generator_function`` methods can be used in the constructor.
Also a shorthand way of having a function generate key values is to use the `dkist_data_simulator.dataset.key_function` decorator.

  >>> from dkist_data_simulator.dataset import key_function
  >>> from dkist_data_simulator.spec122 import Spec122Dataset
  >>> class ExampleDataset(Spec122Dataset):
  ...     def __init__(self, *args, **kwargs):
  ...         super().__init__(*args, **kwargs)
  ...         # Add a header key with a given, fixed value over all headers
  ...         self.add_constant_key("INSTRUME", "Example")
  ...         # Add a header key with a given, single random value over all headers
  ...         self.add_constant_key("EXPER_ID")
  ...
  ...     @key_function("FRAMEVOL")
  ...     def framevol(self, key):
  ...         return 10


To remove a key from a generated header (for instance to generate invalid data), overload the ``header()`` method and remove keys before returning::

  >>> class InvalidDataset(Spec122Dataset):
  ...     def header(self, *args, **kwargs):
  ...         header = super().header(*args, **kwargs)
  ...         header.pop("NAXIS")
  ...         return header


License
-------

This project is Copyright (c) AURA / NSO and licensed under
the terms of the BSD 3-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.


Contributing
------------

We love contributions! dkist-data-simulator is open source,
built on open source, and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by
`Adrienne Lowe <https://github.com/adriennefriend>`_ for a
`PyCon talk <https://www.youtube.com/watch?v=6Uj746j9Heo>`_, and was adapted by
dkist-data-simulator based on its use in the README file for the
`MetPy project <https://github.com/Unidata/MetPy>`_.
