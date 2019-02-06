class Metric:
  data = {
    'name': '', # user
    'category': '', # user
    'unit': '', # user
    'value': 0,
    'aggregation': 'avg',
    'historic': True
  }
  def __init__(self, name, category, unit):
    self.data['name'] = name
    self.data['category'] = category
    self.data['unit'] = unit

  def setValue(self, value):
    self.data['value'] = value

  def getName(self):
    return self.data['name']

  def getData(self):
    return self.data