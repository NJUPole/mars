#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y atlas-devel

# Compile wheels
PYBIN=/opt/python/${PYVER}/bin
"${PYBIN}/pip" install -r /io/requirements-dev.txt
"${PYBIN}/pip" install -r /io/requirements-extra.txt

cd /io
"${PYBIN}/python" setup.py bdist_wheel


# Bundle external shared libraries into the wheels
for whl in dist/*.whl; do
    auditwheel repair "$whl" -w dist/
done

# Install packages and test
#for PYBIN in /opt/python/*/bin/; do
#    "${PYBIN}/pip" install python-manylinux-demo --no-index -f /io/wheelhouse
#    (cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
#done