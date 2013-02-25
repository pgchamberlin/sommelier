## MySQLdb setup

This document is based on advice retrieved from http://codeinthehole.com/writing/how-to-set-up-mysql-for-python-on-ubuntu/

The instructions assume the user is running Ubuntu Linux.

## Install pip

We need pip to be installed to manage python packages

    sudo apt-get install python-pip
    pip install -U pip

## Install mysql-python

The package MySQLdb depends on both libmysqlclient-dev and python-dev:

    sudo apt-get install libmysqlclient-dev python-dev

Now we can install MySQLdb

    pip install MySQL-python

## MySQL

    CREATE USER 'sommelier'@'localhost' IDENTIFIED BY 'vinorosso';
    GRANT ALL ON wine.* TO 'sommelier'@'localhost';

