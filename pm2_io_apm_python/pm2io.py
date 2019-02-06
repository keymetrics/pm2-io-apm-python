import threading

from .services import actions
from .services import metrics
from .services import status
from .services import transport

from .classes import metric as mmetric
from .classes import action as maction

from .features import notifier
from .features.tracing import tracing

class Pm2Io:
  metricManager = mmetric
  actionManager = maction

  def __init__(self, config):
    self.config = config

    # init action service
    self.actionService = actions.Actions()

    # init metrics service
    self.metricService = metrics.Metrics()

    # init transporter
    self.transporter = transport.Transporter(config, self.actionService)

    # init notifier
    self.notifier = notifier.Notifier(self.transporter)

    # init tracing
    self.tracing = tracing.Tracing(self.transporter)

  def start(self):
    # start status interval thread
    threading.Thread(target=self.statusInterval, args=(
      self.config,
      self.transporter,
      self.metricService,
      self.actionService,
    )).start()

    self.transporter.getServer()
    threading.Thread(target=self.transporter.connect).start()

  def stop(self):
    # stop threads

  def statusInterval(self, config, t, m, a):
    while (True):
      # automatic wait 1 sec (cpu calculation)
      t.send('status', status.Status(config, m, a).data)