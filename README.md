# dpp-devid

Scripts to onboard a device using DPP with Device certificates. This requires the fork of hostap with support for iDevID which is available here.

    https://github.com/ranganathanm/hostap  

Please clone and build it. This repository publishes a user interface, certificates and script to test out DPP.

Configurator: Install zbar-tools (for reading qr codes -- configurator only)

        sudo apt-get install zbar-tools
        sudo apt-get install libzbar-dev

COnfigurator: Install the python wrapper for zbar and the python image library to read qr codes (configurator only )

        pip install Pillow
        pip install zbarlight

Configurator: Install pyside (for GUI -- configurator only)

         sudo apt-get install python-pyside

Configurator and Enrolle: Install netifaces to read the network interface MAC address

        pip install netifaces

Enrollee: copy wpa_supplicant.example into wpa_supplicant.orig, Edit wpa_supplicant.orig 
and point it at the DevId certificate. 

         cd scripts/enrollee 
	 cp wpa_supplicant.example wpa_supplicant.orig

Enrollee: Start the enrolle as follows. 

         cd scripts/enrollee 
         # preserve the contents of wpa_supplicant so we can see what DPP did
         cp wpa_supplicant.conf.orig wpa_supplicant.conf
         # Start the enrollee
         sudo python enrollee.py --if wlan1 --pkey /home/pi/dpp-devid/test/DevID50/DevIDSecrets/IDevID50.key.der --cf ./wpa_supplicant.conf



## Notes ##

If you are using a raspberry Pi3 to test this out, please use a USB wireless card. The on board wireless 
card does not support DPP.


## Copyrights and Disclaimers ##

The following disclaimer applies to all code that was written by employees
of the National Institute of Standards and Technology.

This software was developed by employees of the National Institute of
Standards and Technology (NIST), an agency of the Federal Government
and is being made available as a public service. Pursuant to title 17
United States Code Section 105, works of NIST employees are not subject
to copyright protection in the United States.  This software may be
subject to foreign copyright.  Permission in the United States and in
foreign countries, to the extent that NIST may hold copyright, to use,
copy, modify, create derivative works, and distribute this software
and its documentation without fee is hereby granted on a non-exclusive
basis, provided that this notice and disclaimer of warranty appears in
all copies.

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND,
EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED
TO, ANY WARRANTY THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE,
AND FREEDOM FROM INFRINGEMENT, AND ANY WARRANTY THAT THE DOCUMENTATION
WILL CONFORM TO THE SOFTWARE, OR ANY WARRANTY THAT THE SOFTWARE WILL
BE ERROR FREE.  IN NO EVENT SHALL NIST BE LIABLE FOR ANY DAMAGES,
INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL
DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY CONNECTED WITH
THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR
OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY
OR OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT
OF THE RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.

[See official statements here](https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software)


Specific copyrights for code that has been re-used from other open 
source projects are noted in the source files as appropriate.
Please acknowledge our work if you re-use this code or design.

