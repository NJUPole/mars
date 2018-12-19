#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y atlas-devel

# Compile wheels
PYBIN=/opt/python/${PYVER}/bin
"${PYBIN}/pip" install -r /io/requirements-dev.txt
"${PYBIN}/pip" install -r /io/requirements-extra.txt
"${PYBIN}/python" /io/setup.py bdist_wheel -d /io/dist


# Bundle external shared libraries into the wheels
for whl in /io/dist/*.whl; do
    auditwheel repair "$whl" -w /io/dist/
done

# Install packages and test
#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
#done