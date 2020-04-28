#!/usr/bin/env python3.6
"""
this is the Xprojects's deamon,every project show start by Xdaemon.py.
Xdaemon.py show be chmoded by "chmod a+x Xdaemon.py"  before use it.
"""


import os
import sys
import time
import atexit
import subprocess

file_pid= './dbscale.pid'
user="dbscale_internal"
password="bgview@2018"
port=3307
host='127.0.0.1'

#log= open(file_log,'a')
try:
  pid=os.fork()
  if pid >0 :
    sys.exit(0)
except OSError,e:
  sys.stderr.write("fork #1 failed:%d (%s)\n" % (e.errno,e.strerror))
  sys.exit(1)

os.setsid()
try:
  pid = os.fork()
  if pid > 0:
    sys.exit(0)
except OSError, e:
  sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
  sys.exit(1)

sys.stdout.flush()
sys.stderr.flush()
si = file('/dev/null', 'r')
so = file('/dev/null', 'a+')
se = file('/dev/null', 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())


# 0 means dbscale runs ok
def check_dbscale_login():
  retry_times=100
  checkCMD = "mysql -h{h} -p{p} -P{P} -u{u} --connect-timeout=5 -e 'dbscale show version' >dbscale_daemon.log 2>&1 ; echo $?".format(h=host, p=password, P=port, u=user)
  while retry_times > 0 :
    pro=commands.getoutput(checkCMD)
    if pro == '0':
      return 0
    else:
      retry_times = retry_times - 1
      time.sleep(3)
  return 1

# 0 means dbscale runs ok
def check_dbscale_pid():
  if os.path.isfile(file_pid) == False:
    return 1
  dbscalePID = commands.getoutput('cat ./dbscale.pid')
  checkCMD = "ps -A|awk  '$1~/^{pid}$/'|grep -c dbscale".format(pid=dbscalePID)
  pro=commands.getoutput(checkCMD)
  if pro == '0':
    return 1
  return 0


while True:
  if check_dbscale_pid() == 0:      # dbscale pid is ok
    if check_dbscale_login() == 0:  # dbscale login is ok
      time.sleep(3)
      continue
  os.system('./dbscale-service.sh stop')
  os.system('killall -9 dbscale')
  time.sleep(60);
  os.system('./dbscale-service.sh start')