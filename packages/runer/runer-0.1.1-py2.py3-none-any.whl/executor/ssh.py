#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2/23/2021
@author: Pytool Li <pytli@celestica.com> 
"""
import os
import sys
import pathlib
from time import sleep
# sudo pip install paramiko
import paramiko
from stat import S_ISDIR
sessions = {
    "name":{
        "conn" : True,
        'ssh': {
            'host': "",
            "user": "",
            "pass": "",


        }
        
    }
}
def get_connection(name:str,*args, **kwargs) -> dict:
    if name in sessions:
        return sessions[name]
    else:
        # create new connection
        # check version 
        if "ssh" in kwargs:
            session = {
                
            }
            host = kwargs.get("host","localhost")
            port = kwargs.get("port",22)
            user = kwargs.get("user","root")
            passwd = kwargs.get("passwd","") 
            c = SSH(host, port, user, passwd)
            print(session)
            if c:
                session["session"] = c
                session["ssh"] = kwargs["ssh"]
                sessions[name] = session
                return session

    return {}
def run(*args, **kwargs):
    s = get_connection(*args, **kwargs)
    if s :
        c  =  s.get("session",None)
        c.run(**kwargs)
        pass

def callback(data:bytes,*args):
    stdin = args[0]
    if data.find(b"dna_2_5_13")>=0:
        data = bytes()
        stdin.channel.send('dsh \n') 
        stdin.channel.send('version \n')
        
    if data.find(b'No version information.') >=0:
        data = bytes()
        stdin.channel.send('pwd\n')
        sleep(0.1) 
        stdin.channel.send('exit\n')
        stdin.channel.send('exit\n')
    return data

class SSH():
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()
        self._sftp = paramiko.SFTPClient.from_transport(self._transport)

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username, password=self._password)
        # erro paramiko.ssh_exception.SSHException: SSH session not active
        transport.set_keepalive(60)
        self._transport = transport

    def get(self, remotepath: str, localpath: str):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        if localpath.endswith('/'):
            localpath = localpath + '/' + os.path.basename(remotepath)
        p = os.path.dirname(localpath)
        if not os.path.exists(p):
            os.makedirs(p)
        self._sftp.get(remotepath, localpath)

    def put(self, localpath: str, remotepath: str):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        if remotepath.endswith('/'):
            remotepath = remotepath + '/' + os.path.basename(localpath)
        self.mkdir_p(os.path.dirname(remotepath).replace("\\", "/"))
        self._sftp.put(localpath, remotepath)

    def mkdir_p(self, remote_directory):
        if remote_directory[0] == '/':
            dir_path = '/'
        else:
            dir_path = ''
        for dir_folder in remote_directory.split("/"):
            if dir_folder == "":
                continue
            dir_path += r"{0}/".format(dir_folder)
            # print(dir_path)
            try:
                self._sftp.listdir(dir_path)
            except IOError:
                self._sftp.mkdir(dir_path)

    def walk(self, remote_dir):
        root = remote_dir
        files = []
        folders = []
        for f in self._sftp.listdir_attr(remote_dir):
            if S_ISDIR(f.st_mode):
                folders.append(f.filename)
            else:
                files.append(f.filename)
        # print (root, folders, files)
        yield root, folders, files
        for folder in folders:
            abs_path = os.path.join(root, folder).replace("\\", "/")
            for x in self.walk(abs_path):
                yield x

    def download_dir(self, remote_dir, local_dir):
        remote_dir = remote_dir.replace("\\", "/")
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        fpath, fname = os.path.split(remote_dir)
        # print(fpath, fname)
        if fpath:
            self._sftp.chdir(fpath)
        parent = fname
        # print(parent)
        try:
            os.mkdir(local_dir)
        except:
            pass
        # r=root, d=directories, f = files
        for root, dirs, files in self.walk(parent):
            try:
                os.mkdir(os.path.join(local_dir, root))
            except:
                pass
            for f in files:
                local_fn = os.path.join(local_dir, root, f).replace("\\", "/")
                remote_fn = os.path.join(root, f).replace("\\", "/")
                self.get(remote_fn, local_fn)

    def upload_dir(self, local_dir, remote_dir):

        local_dir = os.path.expandvars(local_dir).rstrip(
            '\\').rstrip('/')
        remote_dir = os.path.expandvars(remote_dir).rstrip(
            '\\').rstrip('/').replace("\\", "/")
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        for root, dirs, files in os.walk(local_dir):
            print(dirs)
            for dir in dirs:
                try:
                    _d = os.path.join(remote_dir, ''.join(root.rsplit(local_dir))[
                                      1:], dir).replace("\\", "/")
                    print(_d)
                    self.mkdir_p(_d)
                except:
                    pass
            for file in files:
                _l = os.path.join(root, file).replace("\\", "/")
                _r = os.path.join(remote_dir, ''.join(root.rsplit(local_dir))[
                                  1:], file).replace("\\", "/")
                print("[", _l, "==>", _r, "]")
                self.put(_l, _r)

    def upload(self, src: str, dst: str):
        if src.replace("\\", "/").endswith('/'):
            self.upload_dir(src, dst)
        else:
            self.put(src, dst)

    def download(self, src: str, dst: str):
        if src.replace("\\", "/").endswith('/'):
            self.download_dir(src, dst)
        else:
            self.get(src, dst)

    def run_sudo(self, command, timeout=None):
        return self.run('sudo '+command, timeout)

    def run(self, command, timeout=None,sync=True,cb = callback,**kwargs):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(
            command, timeout=timeout)

        # stdoutLines = ""
        # while not stdout.channel.exit_status_ready():
        #     if stdout.channel.recv_ready():
        #         stdoutLines = stdout.readlines()
        data = bytes()
        while not stdout.channel.exit_status_ready():
            # Print stdout data when available
            if stdout.channel.recv_ready():
                # Retrieve the first 1024 bytes
                solo_line = stdout.channel.recv(1)
                if solo_line :
                    if sync:
                        sys.stdout.write(solo_line.decode('utf-8'))
                        sys.stdout.flush()
                    data += solo_line
            if stderr.channel.recv_ready():
                # Retrieve the first 1024 bytes
                solo_line = stderr.channel.recv(1)
                if solo_line:
                    if sync:
                        sys.stdout.write(solo_line.decode('utf-8'))
                        sys.stdout.flush()
                    data += solo_line
            # print(".")
            data=cb(data,stdin,stdout,stderr)
            # if(cmp(solo_line,'uec> ') ==0 ):    #Change Conditionals to your code here
            #     if num_of_input == 1 :
            #     stdin.channel.send('q \n')      # send input commmand , in my code is exit the interactive session, the connect will close.
            #     num_of_input += 1
        # ssh.close()

        data = data.decode('utf-8').strip() + \
            stdout.read().decode('utf-8').strip()
        if len(data) > 0:
            # print(data.strip())
            return 0, data, None

        err = stderr.read().decode('utf-8').strip()
        if len(err) > 0:
            print(err.strip())
            return 1, None, err
        return 2, None, None

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()


if __name__ == "__main__":
    ssh = SSH('10.204.82.96', 22, 'admin', 'admin')
    localpath = 'restful_api_definition.md'
    remotepath = '/home/admin/hello.txt'
    # ssh.put(localpath, remotepath)
    ldir = "data/ff/"
    rdir = "bb/"
    # ssh.upload(ldir, rdir)
    ssh.download(rdir, ldir)

    # # ssh.run('whoami;date')
    # # ssh.run('sleep 18')   # test for 30*60 sec running task
    # ssh.run('whoami;date && ls ')
    # # ssh.run('cd WorkSpace/Python/test;pwd')  #cd需要特别处理
    # ssh.run('pwd')
    # # ssh.run('tree WorkSpace/Python/test')
    # # ssh.run('ls -l')
    # ssh.run('echo "hello python" > python.txt')
    # ssh.run('ls hello')  #显示错误信息
    # rc,out,_=ssh.run('md5sum hello.txt')  #显示错误信息
    # if not rc:
    #     print(out.find("156131b240d9d5ae2b8f4c697768052f3"))
    ssh.close()
