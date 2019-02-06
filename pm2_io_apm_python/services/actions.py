class Actions:
  actions = []

  def addAction(self, action):
    self.actions.append(action)

  def getActions(self):
    actions = []
    for action in self.actions:
      actions.append(action.data)
    return actions

  def callAction(self, actionName, data):
    for action in self.actions:
      if (action.getName() == actionName):
        return action.callback(data)