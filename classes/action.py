class Action:
  data = {
    'action_name': 'none',
    'action_type': ''
  }

  def __init__(self, name, callback):
    self.data['action_name'] = name
    self.callback = callback

  def getName(self):
    return self.data['action_name']
