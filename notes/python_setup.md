# Python Environment


Install dependencies:

    pip install virtualenv
    
    ./flask/bin/pip install MySQL-python
    ./flask/bin/pip install flask
    ./flask/bin/pip install mock

    # https://nose.readthedocs.org/en/latest/ Source: https://github.com/nose-devs/nose
    ./flask/bin/pip install nose

    # gonna need numpy a lot probably!
    ./flask/bin/pip install numpy
    # scipy is a pain. The following installation method
    # is courtesy of http://www.scipy.org/Installing_SciPy/Linux#head-d437bf93b9d428c6efeb08575f631ddf398374ea
    # the following command installs rather a lot of stuff :-|
    sudo apt-get build-dep python-numpy 
    # the following command does a big build and throws all sorts of errors which dont seem to matter.
    sudo apt-get -b source python-numpy 
    ./flask/bin/pip install scipy 

    # install dependencies for python-recsys
    flask/bin/pip install csc-pysparse networkx divisi2
    # clone python-recsys from Git and set it up in virtualenv
    git clone http://github.com/ocelma/python-recsys
    cd python-recsys
    ../flask/bin/python setup.py install

