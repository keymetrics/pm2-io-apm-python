# pm2-io-apm-python

## Getting started

```python
from pm2_io_apm_python import pm2io
from pm2_io_apm_python import config

pm2 = pm2io.Pm2Io(config.Config("public_key", "secret_key", "Python app demo"))
pm2.start()
```

## Add action

```python
pm2.actionService.addAction(
  pm2.actionManager.Action("i'm an action", lambda data: "i'm the answer\n")
)
```

## Add metric

```python
randMetric = pm2.metricManager.Metric('random', 'r', 'rand')
pm2.metricService.addMetric(randMetric)

randMetric.setValue(random.randint(1, 1000))
```

## Logging

```python
pm2.notifier.log("Completely started")
```

## Tracing
We are using OpenCensus for Transaction Tracing in Python. You can check integrations available on [https://github.com/census-instrumentation/opencensus-python#integration](OpenCensus python integration).

The exporter is automatically configured when you init the agent with httplib integration.

### Example (MySQL)

#### Install

```python
pip install opencensus-ext-mysql
```

#### Add tracing

```python
from opencensus.trace import config_integration

config_integration.trace_integrations(['httplib', 'mysql'])
```