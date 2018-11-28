#!/usr/bin/env python3

from classes import config
from classes import metric as mmetric
from classes import action as maction
from services import transport
from services import status
from services import metrics
from services import actions

import time
import threading
import random
import os
import json

def statusInterval(config, t, m, a):
  while (True):
    t.send('status', status.Status(config, m, a).data)

def loopLog(t):
  while (True):
    time.sleep(2)
    t.send('logs', 'I am eating cats')

def cpuLoop():
  i = 0
  while (True):
    i += 1
    if (i == 100000000):
      time.sleep(4)
      i = 0

def randomMetric(metric):
  while True:
    v = random.randint(1, 1000)
    print('Set to: ' + str(v))
    metric.setValue(v)
    time.sleep(1)

def start(config):
  m = metrics.Metrics()
  a = actions.Actions()

  t = transport.Transporter(config, a)
  t.getServer()
  threading.Thread(target=t.connect).start()
  threading.Thread(target=statusInterval, args=(config, t,m,a,)).start()
  threading.Thread(target=loopLog, args=(t,)).start()

  #threading.Thread(target=cpuLoop).start()
  time.sleep(2)
  myMetric = mmetric.Metric('truc', 't', 'v')
  def metricFunc(data):
    return "Hey!\n"
  myAction = maction.Action('Hello', metricFunc)
  m.addMetric(myMetric)
  a.addAction(myAction)
  threading.Thread(target=randomMetric, args=(myMetric,)).start()

  

if __name__ == '__main__':
  start(config.Config("yrohq7oisb0ksb6", "vq7zhtduf7hiihb"))