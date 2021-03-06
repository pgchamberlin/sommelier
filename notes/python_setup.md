We need pip to be installed to manage python packages

    sudo apt-get install python-pip
    pip install -U pip

Vitualenv enables us to install modules and packages local to our
project, so we dont need to expose our system-level python
installation to incompatible or otherwise obnoxious packages
that might destabilize our other project, or OS in general

    pip install virtualenv
    virtualenv flask

MySQL-python will enable us to query data (very useful!) - helpful advice retrieved from http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/

There are some additional dependencies with MySQL-python that need to be installed at a system level

    sudo apt-get install libmysqlclient-dev python-dev

Documentation on working with MySQLdb is at: http://mysql-python.sourceforge.net/MySQLdb.html

Now we can install MySQL-python in our virtualenv using a local pip

    ./flask/bin/pip install MySQL-python

Flask itself is our web framework of choice

    ./flask/bin/pip install flask

Mock will be useful for unit testing

    ./flask/bin/pip install mock

nose will serve as our test runner
https://nose.readthedocs.org/en/latest/ Source: https://github.com/nose-devs/nose

    ./flask/bin/pip install nose

Scipy is a pain. The following installation method is courtesy of: http://www.scipy.org/Installing_SciPy/Linux#head-d437bf93b9d428c6efeb08575f631ddf398374ea

This installs rather a lot of stuff, the dependencies of NumPy, globally :-|

    sudo apt-get build-dep python-numpy 

The following command does a big build and throws all sorts of errors, which are apparently fine to ignore.

    sudo apt-get -b source python-numpy 
    ./flask/bin/pip install scipy 

Install dependencies for python-recsys

    flask/bin/pip install csc-pysparse networkx divisi2

Clone python-recsys from Git and set it up in virtualenv

    git clone http://github.com/ocelma/python-recsys
    cd python-recsys
    ../flask/bin/python setup.py install

Install matplotlib for graphing test results.

N.b. this is not subsequently installed in the virtualenv, but
that isnt a problem as the graphing can be done without
invoking any of our virtualenv

    sudo apt-get install python-matplotlib
