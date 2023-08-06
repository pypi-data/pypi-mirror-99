#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2/23/2021
@author: Pytool Li <pytli@celestica.com> 
"""

from sys import setswitchinterval
from .shell import run as shell_run
from .ssh import SSH
from config import config
g_bmc = None
g_come = None

TYPE_EXEC_SHELL = "shell"
TYPE_EXEC_BMC = "bmc"
TYPE_EXEC_COME = "come"
TYPE_EXEC_SSH = "ssh"
TYPE_EXEC_IPMI = "ipmi"
TYPE_EXEC_RESTFUL = "restful"
TYPE_EXEC_RESTFUL_CMD = "restful_cmd"


def ssh_session(type):
    host = config["ssh"][type]["SSH_HOST"]
    port = config["ssh"][type]["SSH_PORT"]
    user = config["ssh"][type]["SSH_USER"]
    passwd = config["ssh"][type]["SSH_PASSWD"]
    return SSH(host, port, user, passwd)

def upload(localpath, remotepath, t=TYPE_EXEC_BMC,host=None, port=22, user='root', passwd=None):
    global g_bmc, g_come
    if t == TYPE_EXEC_BMC:
        if g_bmc == None:
            try:
                g_bmc = ssh_session(t)
            except:
                g_bmc = None
                return (-127, None, "connect err!")
        return g_bmc.upload(localpath, remotepath)
    elif t == TYPE_EXEC_COME:
        if g_come == None:
            try:
                g_come = ssh_session(t)
            except:
                g_come = None
                return (-127, None, "connect err!")

        return g_come.upload(localpath, remotepath)
    elif t == TYPE_EXEC_SSH:
        if not host == None:
            ssh = SSH(host, port, user, passwd)
            ssh.upload(localpath, remotepath)
            ssh.close()
            return 

def run(cmd, t=TYPE_EXEC_SHELL, sudo=False, host=None, port=22, user='root', passwd=None):
    '''
        t: [ "bmc","come","ssh","ipmi", "restful_cmd","restful"]
    '''
    global g_bmc, g_come
    if t == TYPE_EXEC_SHELL:
        # print(cmd)
        return shell_run(cmd, sudo=sudo)
    elif t == TYPE_EXEC_BMC:
        if g_bmc == None:
            try:
                g_bmc = ssh_session(t)
            except:
                g_bmc = None
                return (-127, None, "connect err!")
        return g_bmc.run(cmd)
    elif t == TYPE_EXEC_COME:
        if g_come == None:
            try:
                g_come = ssh_session(t)
            except:
                g_come = None
                return (-127, None, "connect err!")

        return g_come.run(cmd)
    elif t == TYPE_EXEC_SSH:
        if not host == None:
            ssh = SSH(host, port, user, passwd)
            rc, stdout, stderr = ssh.run(cmd)
            ssh.close()
            return (rc, stdout, stderr)
    elif t == TYPE_EXEC_IPMI:
        pass
    elif t == TYPE_EXEC_RESTFUL_CMD:
        rc, stdout, stderr = shell_run(cmd, sudo=sudo)
        if rc == 0:
            import json
            ret_dict = json.loads(stdout)
            if ret_dict['status'] == 'ERROR':
                # raise Exception(ret_dict['message'])
                return (-126, None, ret_dict['message'])
            return rc, ret_dict['data'], None
        return rc, stdout, stderr
    elif t == TYPE_EXEC_RESTFUL:
        pass
    return (-127, None, None)

