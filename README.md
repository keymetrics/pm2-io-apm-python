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

## License

Commercial
