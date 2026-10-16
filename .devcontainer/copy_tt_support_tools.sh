#! /bin/sh

set -eu

if [ ! -e tt ]; then
    cp -R /ttsetup/tt-support-tools tt
fi
