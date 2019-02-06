class Notifier:
  def __init__(self, transporter):
    self.transporter = transporter

  def log(self, s):
    self.transporter.send('logs', s)

  def error(self, message, stack):
    self.transporter.send('process:exception', {
      'message': message,
      'stack': stack
    })
