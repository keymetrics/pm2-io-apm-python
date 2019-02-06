import urllib
from urllib.request import Request, urlopen
import websocket
import json
import time
import datetime

class Transporter:
  opened = False

  def __init__(self, config, actionService):
    # TODO: check config before construct
    self.config = config
    self.actionService = actionService

  def getServer(self):
    req = Request(self.config.node + '/api/node/verifyPM2', bytearray(json.dumps({
      'public_id': self.config.publicKey,
      'private_id': self.config.privateKey,
      'data': {
        'MACHINE_NAME': self.config.serverName,
        'PM2_VERSION': self.config.version,
        'HOSTNAME': self.config.serverName,
      }
    }), 'utf8'))
    req.add_header('Content-Type', 'application/json')
    try:
      a = urlopen(req).read()
      res = json.loads(a)
      self.endpoint = res['endpoints']['ws']
      if not self.endpoint:
        print("No endpoint available for this public/private key")
    except urllib.error.HTTPError:
      print("No endpoint available for this public/private key")
      pass

  def connect(self):
    self.ws = websocket.WebSocketApp(self.endpoint, header={
      'X-KM-PUBLIC': self.config.publicKey,
      'X-KM-SECRET': self.config.privateKey,
      'X-KM-SERVER': self.config.serverName,
      'X-PM2-VERSION': self.config.version,
      'X-PROTOCOL-VERSION': '1',
    },
    on_open = self.wsOnOpen,
    on_message = self.wsOnMessage,
    on_error = self.wsOnError,
    on_close = self.wsOnClose)
    self.ws.run_forever()

  def wsOnOpen(self):
    self.opened = True

  def wsOnMessage(self, message):
    # parse
    data = json.loads(message)
    if (data['channel'] == 'trigger:action'):
      self.send("trigger:action:success", {
        'success': True,
        'id': data['payload']['process_id'],
        'action_name': data['payload']['action_name']
      })
      ret = self.actionService.callAction(data['payload']['action_name'], data['payload']['opts'])
      self.send("axm:reply", {
        'action_name': data['payload']['action_name'],
        'return': ret
      })
    elif (data['channel'] == 'trigger:pm2:action'):
      self.ws.send(json.dumps({
        'channel': 'trigger:pm2:result',
        'payload': {
          'ret': {
            'err': None
          }
        }
      }))

  def wsOnError(self, error):
    self.opened = False

  def wsOnClose(self):
    self.opened = False
    self.connect()

  def sendJson(self, obj):
    if not self.opened:
      return
    try:
      self.ws.send(json.dumps(obj))
    except (ConnectionResetError):
      pass

  def send(self, channel, obj):
    self.sendJson({
      'channel': channel,
      'payload': {
        'at': int(round(time.time() * 1000)),
        'data': obj,
        'process': {
          'pm_id': 0,
          'name': self.config.name,
          'server': self.config.serverName,
          'rev': None
        },
        'server_name': self.config.serverName,
        'protected': False,
        'internal_ip': 'WIP'
      }
    })
