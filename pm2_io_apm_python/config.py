import socket

class Config:
  publicKey = ""
  privateKey = ""
  name = "name"
  serverName = "serverName"
  version = "0.0.1"
  node = ""

  def __init__(self, public, private, name, node = "api.cloud.pm2.io"):
    self.publicKey = public
    self.privateKey = private
    self.name = name
    self.node = node

    self.serverName = socket.gethostname()
