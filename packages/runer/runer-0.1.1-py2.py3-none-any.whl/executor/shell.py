#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2/23/2021
@author: Pytool Li <pytli@celestica.com> 
"""
import os
import sys
import time
import shlex
import signal
import tempfile
import subprocess

_plat = sys.platform.lower()
iswindows = 'win32' in _plat or 'win64' in _plat
isosx     = 'darwin' in _plat
ishaiku = 'haiku1' in _plat
islinux   = not(iswindows or isosx or ishaiku)

envset = False
def setup_environment_variables():
    global envset
    if not envset:
        envset = True
        if getattr(sys, 'frozen', False):
            application_path = getattr(
                sys, '_MEIPASS', os.path.dirname(sys.executable))
        else:
            # application_path = os.path.dirname(__file__)
            application_path = os.path.abspath(".")

        os.environ['PATH'] = os.path.join(application_path, 'bin') + os.pathsep + os.path.join(
            application_path, 'utility') + os.pathsep + os.environ['PATH']
        # print(os.environ["PATH"])

def multi_run():
    def deal_with_stdout():
        for line in p.stdout:
            print(line)

    from subprocess import Popen, PIPE, STDOUT
    from threading import Thread
    p = Popen(["tail", "-f", "/tmp/file"], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    t = Thread(target=deal_with_stdout, daemon=True)
    t.start()
    t.join()

def callback(p):
    # if p.decode().find("rsync")>=0:
    #     print(p)
    return p


def run(cmd, timeout=60,sudo = False,cb = callback):
    setup_environment_variables()
    (rc, stdout, stderr) = (-1, '', '')
    # cmd = cmd.split()
    while True:
        try:        
            if sudo:
            # cmd.insert(0, 'sudo env PATH=$PATH')
                cmd = "sudo env PATH=$PATH "+ cmd
                p = subprocess.Popen(cmd, stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            else:
                p = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        except Exception as e:
            #   log.critical('Caught {e!s} executing {cmd}'.format(**locals()))
            raise e

        if not iswindows:
            import fcntl
            fcntl.fcntl(p.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
            fcntl.fcntl(p.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
        outs = bytes()
        
        if timeout:
            elapsed = 0
            while p.poll() is None :
                while True:
                    out = p.stdout.read(1)
                    if out is not None and out != b'':
                        sys.stdout.write(out.decode('utf-8'))
                        sys.stdout.flush()
                        outs= outs+out
                    else:
                        break
                while True:
                    err = p.stderr.read(1)
                    if err is not None and err != b'':
                        sys.stdout.write(err.decode('utf-8'))
                        sys.stdout.flush()
                        outs= outs+err
                    else:
                        break
                outs = cb(outs)
                # TIMEDOUT
                time.sleep(0.1)
                elapsed = elapsed + 1
                if elapsed >=  timeout*10:
                    # kill all processes that are in the same child process group
                    # which kills the process tree
                    # pgid = os.getpgid(p.pid)    
                    # os.killpg(pgid, signal.SIGKILL)
                    # p.wait()
                    # sys.exit(TIMEOUT_ERROR)
                    break
                
        (stdout, stderr) = p.communicate()
        stdout = outs.decode('utf-8')+stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        # print("error:",stderr)
        # print("out:",stdout)
        rc = p.wait()

        # log.info('with sudo={sudo}, {cmd} returned: {rc}, {stdout!r}, {stderr!r}'.format(sudo=sudo, **locals()))
        if rc == 0:
            sudo = bool(sudo)
            break
        else:
            if sudo is None:
                sudo = True
            else:
                break
    return (rc, stdout, stderr)


def run1(cmd, timeout=120,sudo = False):
    """Run cmd on host
    :param cmd: cmd to be executed
    :param timeout: time to wait for the cmd to complete, 0 for unlimited.
                    After timeout completes, the cmd is killed.
    :return:
    """
    setup_environment_variables()
    # Initialize temp file for stdout. Will be removed when closed.
    outfile = tempfile.SpooledTemporaryFile()
    errfile = tempfile.SpooledTemporaryFile()
    if sudo:
        cmd = "sudo env PATH=$PATH " +cmd
    try:
        # Invoke process
        proc = subprocess.Popen(cmd,stdout=outfile,
                                stderr=errfile, shell=True)
        # Wait for process completion
        # Poll for completion if wait time was set
        if timeout:
            while proc.poll() is None and timeout > 0:
                time.sleep(1)
                timeout -= 1
                # It is needed to print it with sys.stdout otherwise
                # if using print the information is printed after
                # the cmd is killed
                sys.stdout.write(".")
                sys.stdout.flush()
                # Kill process if wait time exceeded
                if timeout <= 0 and not proc.poll():
                    terminate_process(proc.pid, sudo=True)
                    break
            # print("")
        (stdout, stderr) = proc.communicate()
        # Read stdout from file
        outfile.seek(0)
        stdout = outfile.read().decode('utf-8')
        errfile.seek(0)
        stderr = errfile.read().decode('utf-8')
        outfile.close()
        errfile.close()

    except:
        raise

    finally:
        # Make sure the file is closed
        outfile.close()
        errfile.close()

    rc = proc.returncode

    return rc, stdout.strip(), stderr.strip()


def terminate_process(process_pid, sudo=False):
    """ Terminate a running process for a given PID number
    For a given PID, tries to terminate a process by using operating system
    native tools such as "kill" in Linux or "taskkill" in Windows.
    Args:
        process_pid: PID of the process to be terminated
    Returns:
        retcode: When successful returns 0, otherwise the exit code of the
                 utility used to terminate the process.
    """
    retcode = -1

    sudo = "sudo" if sudo else ""
    cmd = "{0} kill -9 {1}".format(sudo, process_pid)

    stdout, stderr, retcode = run(cmd)

    return retcode



import time
from subprocess import Popen, PIPE, STDOUT

def timeout_run(proc, timeout, note='unnamed process', full_output=False):
  start = time.time()
  if timeout is not None:
    while time.time() - start < timeout and proc.poll() is None:
      time.sleep(0.1)
    if proc.poll() is None:
      proc.kill() # XXX bug: killing emscripten.py does not kill it's child process!
      raise Exception("Timed out: " + note)
  out = proc.communicate()
  return '\n'.join(out) if full_output else out[0]

def run_js(filename, engine=None, args=[], check_timeout=False, stdout=PIPE, stderr=None, cwd=None, full_output=False):
  if type(engine) is not list:
    engine = [engine]
  cmd = engine + [filename] + (['--'] if 'd8' in engine[0] else []) + args
  return timeout_run(
    Popen(
      cmd,
      stdout=stdout,
      stderr=stderr,
      cwd=cwd),
    15*60 if check_timeout else None,
    'Execution',
    full_output=full_output)

if __name__ == "__main__":
    cmd = 'ls'
    returncode,stdout, stderr = run(cmd)
    # if returncode != 0:
    devices = stdout.split("\n")
    print(devices, len(devices))
    for line in devices:
        if line:
            print(line)
    print("----")
