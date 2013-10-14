portcullis - prototype
==========

Follow these steps to get a local proxy running that interacts with cloud files:
1. Download the following fork of pyrox, that includes a starting crypto filter: https://github.com/jfwood/pyrox
1. Follow these steps to build pyrox: https://github.com/zinic/pyrox#building-pyrox
1. Create and configure a pyrox config file on your local box:
    1. From your local pyrox repo...
    1. cp examples/config/pyrox.conf /etc/pyrox  (you might need to chown this pyrox folder and file)
    1. Edit /etc/pyrox/pyrox.conf as follows:
        1. Set: upstream_hosts = storage101.dfw1.clouddrive.com:443
        1. Set: upstream = u   and    downstream = u
        1. Set: u = pyrox.portcullis.crypto_filter.CryptoFilter
        1. Set: use_singletons = True
1. Run pyrox as: DEBUG=true ./pyrox_dev.sh start
1. Follow the steps in the 'cloudfiles.sh' script file, then run the various cURL commands it contains.

