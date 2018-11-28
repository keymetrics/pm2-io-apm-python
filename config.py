import socket

class Config:
  publicKey = ""
  privateKey = ""
  name = "name"
  serverName = "serverName"
  version = "0.0.1"
  node = "root.keymetrics.io"

  def __init__(self, public, private, name):
    self.publicKey = public
    self.privateKey = private
    self.name = name

    self.serverName = socket.gethostname()