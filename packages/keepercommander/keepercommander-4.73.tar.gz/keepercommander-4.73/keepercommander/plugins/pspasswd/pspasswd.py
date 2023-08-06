# -*- coding: utf-8 -*-
#  _  __  
# | |/ /___ ___ _ __  ___ _ _ ®
# | ' </ -_) -_) '_ \/ -_) '_|
# |_|\_\___\___| .__/\___|_|
#              |_|            
#
# Keeper Commander 
# Copyright 2018 Keeper Security Inc.
# Contact: ops@keepersecurity.com
#

import subprocess, re


def rotate(record, newpassword):
    """ Grab any required fields from the record """
    host = record.get('cmdr:host')
    user = record.login

    result = False

    # the characters below mess with windows command line
    i = subprocess.call('pspasswd \\\\{0} {1} "{2}"'.format(host, user, newpassword.replace('"', '""')), shell = True)

    if i == 0:
        print('Password changed successfully')
        record.password = newpassword
        result = True
    else:
        print('Password change failed')

    return result


def adjust(newpassword):
    return re.sub('[<>&|]', '', newpassword)
