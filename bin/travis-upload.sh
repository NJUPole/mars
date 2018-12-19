#!/bin/bash

if [ "$TRAVIS_TAG" ]; then
  echo "[distutils]"                                  > ~/.pypirc
  echo "index-servers ="                             >> ~/.pypirc
  echo "    pypi"                                    >> ~/.pypirc
  echo "[pypi]"                                      >> ~/.pypirc
  echo "repository=https://test.pypi.org/legacy/"  >> ~/.pypirc
  echo "username=pyodps"                             >> ~/.pypirc
  echo "password=$PASSWD"                            >> ~/.pypirc

  sudo chmod 777 bin/*
  docker run --rm -v `pwd`:/io $DOCKER_IMAGE $PRE_CMD /io/bin/travis-build-wheels.sh
  ls dist/
#
  python -m pip install twine
#
#  python setup.py bdist_wheel
#
#  for whl in wheelhouse/*.whl; do
#	auditwheel repair $whl -w dist/
#  done
#  rm dist/*-linux*.whl

  python -m twine upload -r pypi --skip-existing dist/*.whl;
else
  echo "Not on a tag, won't deploy to pypi";
fi
