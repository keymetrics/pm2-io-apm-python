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
    print("searching action " + actionName)
    for action in self.actions:
      if (action.getName() == actionName):
        print("got")
        return action.callback(data)