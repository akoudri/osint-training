#!/bin/bash

# Activation
ssh -i tunnel.pem -D 8123 -N -f ubuntu@52.59.249.251
# Désactivation
# ss -lntp + kill

