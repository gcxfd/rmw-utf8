#!/usr/bin/env bash

set -e

_DIR=$(dirname $(realpath "$0"))

cd $_DIR

if [ ! -d "sdb" ] ; then
git clone git@github.com:rmw-link/sdb.git --depth 1
fi

cargo build --release
#export RAYON_NUM_THREADS=8
RUST_LOG="sanakirja=debug" RUST_BACKTRACE=1 target/release/train
mv d.zst ../rmw-utf8/src
