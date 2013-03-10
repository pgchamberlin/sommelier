# Python Environment


Install dependencies:

    pip install virtualenv
    

    ./flask/bin/pip install MySQL-python
    ./flask/bin/pip install flask
    ./flask/bin/pip install mock
    # https://nose.readthedocs.org/en/latest/ Source: https://github.com/nose-devs/nose
    ./flask/bin/pip install nose
    ./flask/bin/pip install numpy
    # scipy is a pain. The following installation method
    # is courtesy of http://www.scipy.org/Installing_SciPy/Linux#head-d437bf93b9d428c6efeb08575f631ddf398374ea
    # the following command installs rather a lot of stuff :-|
    sudo apt-get build-dep python-numpy 
    # the following command does a big build and throws all sorts of errors which dont seem to matter.
    sudo apt-get -b source python-numpy 
    ./flask/bin/pip install scipy 

