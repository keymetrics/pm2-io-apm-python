import json
import os
import psutil
import sys
import time
import platform
import cpuinfo

start_time = time.time()
memory = psutil.virtual_memory().total

cpu = cpuinfo.get_cpu_info()

class Status:
  data = {
    "process": [
      {
        "pid": os.getpid(),
        "name": "Python App", # init
        "server": "",
        "interpreter": sys.executable,
        "created_at": 0, # init
        "exec_mode": "fork_mode",
        "pm_uptime": 0, # init
        "status": "online",
        "pm_id": 0,
        "cpu": 0, # init
        "rev": "",
        "memory": 0, #  init
        "node_env": "production",
        "axm_actions": [
          {
            "action_name": "km:heapdump",
            "action_type": "internal"
          },
          {
            "action_name": "km:cpu:profiling:start",
            "action_type": "internal"
          },
          {
            "action_name": "km:cpu:profiling:stop",
            "action_type": "internal"
          },
          {
            "action_name": "Get env",
            "action_type": ""
          }
        ],
        "axm_monitor": {
          "test": {
            "name": "test",
            "value": 2,
            "type": "metric",
            "historic": True,
            "unit": "unit",
            "agg_type": "avg"
          }
        },
        "axm_options": {
          "custom_probes": True,
          "profiling": False,
          "heapdump": False,
          "apm": {
            "type": "python",
            "version": "0.0.1"
          }
        }
      }
    ],
    "server": {
      "loadavg": [], # init
      "total_mem": 0, # init
      "cpu": {
        "number": 0, # init
        "info": "N/A" # init
      },
      "uptime": 0, # init
      "interaction": True,
      "pm2_version": "0.0.1",
      "node_version": "python" + platform.python_version(),
    }
  }

  def __init__(self, config, metricService, actionService):
    process = psutil.Process(os.getpid())

    self.data['process'][0]['name'] = config.name
    self.data['process'][0]['memory'] = process.memory_info().rss
    self.data['process'][0]['cpu'] = process.cpu_percent(1)
    self.data['process'][0]['created_at'] = start_time * 1000
    self.data['process'][0]['pm_uptime'] = start_time * 1000
    self.data['server']['loadavg'] = os.getloadavg()
    self.data['server']['uptime'] = time.time() - psutil.boot_time()
    self.data['server']['total_mem'] = memory
    self.data['server']['cpu']['info'] = cpu['brand']
    self.data['server']['cpu']['number'] = cpu['count']

    self.data['process'][0]['axm_monitor'] = metricService.getMetrics()
    self.data['process'][0]['axm_actions'] = actionService.getActions()