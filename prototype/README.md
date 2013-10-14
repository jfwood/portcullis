portcullis - prototype
==========

Follow these steps to get a local proxy running that interacts with cloud files:

1) Download the following fork of pyrox, that includes a starting crypto filter: https://github.com/jfwood/pyrox

2) Create and configure a pyrox config file on your local box:
  a) From your local pyrox repo...
  b) cp examples/config/pyrox.conf /etc/pyrox  (you might need to chown this pyrox folder and file)
  c) Edit /etc/pyrox/pyrox.conf as follows:
     i)   Set: upstream_hosts = storage101.dfw1.clouddrive.com:443
     ii)  Set: upstream = u   and    downstream = u
     iii) Set: u = pyrox.portcullis.crypto_filter.CryptoFilter
     iv)  Set: use_singletons = True

3) Run pyrox as: DEBUG=true ./pyrox_dev.sh start

4) Follow the steps in the 'cloudfiles.sh' script file, then run the various cURL commands it contains.

