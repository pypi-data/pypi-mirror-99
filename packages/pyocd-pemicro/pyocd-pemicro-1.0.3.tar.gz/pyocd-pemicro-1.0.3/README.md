Python PyOCD_PEMicro plugin debug probes support
================================================

The simple PyOCD debug probe plugin for PEMicro debug probes - Multilink/FX, Cyclone/FX. The purpose of this plugin is 
keep separately this support because is using PyPemicro package which is designed for Python 3.x without backward compatibility for Python2.x. 
The PyOCD use this support only with Python 3.x and higher, for Python 2.x the PeMicro won't be supported.

The package is tested only with Multilink/FX and Cyclone/FX probes on NXP ARM microcontrollers.

The PEMicro company helps with this development, so big Thanks to them (www.pemicro.com).

Author: Petr Gargulak, petr.gargulak@nxp.com (NXP 2020, www.nxp.com)

Note
----
This package is just plugin to full PyOCD package - It doesn't work standalone!


Dependencies
------------
six
pypemicro
logging
time


Installation
------------
Directly from www.pypi.org:

``` bash
    $ pip install pyocd_pemicro
