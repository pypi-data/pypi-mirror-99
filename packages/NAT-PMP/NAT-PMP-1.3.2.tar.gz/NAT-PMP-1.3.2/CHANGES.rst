v1.3.2
======

Packaging refresh.

v1.3.1
======

Docstring cleanup.

v1.3.0
======

Client can be invoked with simply ``python -m natpmp``.

v1.2.1
======

Fix badges.

v1.2.0
======

Require Python 3.6 or later.

#1: Add type for port arguments.

1.1
===

Use netifaces for gateway autodetection.

1.0
===

Initial release as "NAT-PMP", based on py-natpmp 0.2.4.

Client may be invoked with simply ``python -m natpmp.client``.

py-natpmp
=========

0.2.4-2 Incorporated changes from coinbend fork. Includes gateway auto-detection via netifaces and NatPMP convenience class.  Thanks to super3 and robertsdotpm, per pull request #8
0.2.4 - removed extraneous opcode on PublicAddressResponse.  Thanks dog-2, per issue #7
0.2.3 - check length on PublicAddressResponse, PortMapResponse.  Thanks to mct, per issue #5.
0.2.2 - changed gateway autodetect, per github issue #1.  thanks to jirib
0.2 - changed useException to use_exception, responseDataClass to response_data_class parameters in function calls for consistency
0.1 - repackaged via setuptools.  Fixed major bug in gateway detection.  Experimental gateway detection support for Windows 7.  Python 2.6 testing.
0.0.1.2 - NT autodetection code.  Thanks to roee shlomo for the gateway detection regex!
0.0.1.1 - Removed broken mutex code
0.0.1   - Initial release

