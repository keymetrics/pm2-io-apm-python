class Metrics:
  listMetric = {}

  def addMetric(self, metric):
    self.listMetric[metric.getName()] = metric.getData()

  def getMetrics(self):
    return self.listMetric