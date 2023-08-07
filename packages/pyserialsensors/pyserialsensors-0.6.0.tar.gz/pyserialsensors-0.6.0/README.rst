===============
pySerialSensors
===============


.. image:: https://img.shields.io/pypi/v/pyserialsensors.svg
        :target: https://pypi.python.org/pypi/pyserialsensors

.. image:: https://img.shields.io/travis/Egenskaber/pyserialsensors.svg
        :target: https://travis-ci.com/Egenskaber/pyserialsensors

.. image:: https://readthedocs.org/projects/pyserialsensors/badge/?version=latest
        :target: https://pyserialsensors.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Egenskaber/pyserialsensors/shield.svg
     :target: https://pyup.io/repos/github/Egenskaber/pyserialsensors/
     :alt: Updates



Serial communication with sensors via I2C, SPI and UART using FTDI USB bridges


* Free software: MIT license
* Documentation: https://pyserialsensors.readthedocs.io.


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
### Rename FTDI
Use tools/renamy.py

Check the result using 
```lsusb -d 0403: -v```

### Known Issues

- After a reconnect the measurement frequency drops due to hard coded frequency in the reconnection code.
