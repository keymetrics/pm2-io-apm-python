from opencensus.trace import config_integration
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import always_on
from opencensus.common.utils import check_str_length

from . import exporter

class Tracing:
  def __init__(self, transporter):
    self.transporter = transporter
    self.exporter = exporter.CustomExporter(transporter)
    config_integration.trace_integrations(['httplib'])
    self.tracer = Tracer(exporter=self.exporter, sampler=always_on.AlwaysOnSampler())