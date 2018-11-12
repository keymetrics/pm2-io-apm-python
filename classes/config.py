class Config:
  publicKey = ""
  privateKey = ""
  name = "name"
  serverName = "serverName"
  version = "0.0.1"
  node = "root.keymetrics.io"

  def __init__(self, public, private):
    self.publicKey = public
    self.privateKey = private