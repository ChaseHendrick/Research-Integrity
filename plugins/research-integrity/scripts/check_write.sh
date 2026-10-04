#!/bin/sh
# Starts the write check. No network.
dir=${0%/*}
exec python3 "$dir/check_write.py"
