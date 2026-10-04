#!/bin/sh
# Starts the local server. No network.
dir=${0%/*}
exec python3 "$dir/server.py"
