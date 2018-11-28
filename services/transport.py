import urllib
from urllib.request import Request, urlopen
import websocket
import json
import time

class Transporter:
  opened = False

  def __init__(self, config, actionService):
    # TODO: check config before construct
    self.config = config
    self.actionService = actionService

  def getServer(self):
    req = Request('https://' + self.config.node + '/api/node/verifyPM2', bytearray(json.dumps({
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
      print("endpoint:", self.endpoint)
    except urllib.error.HTTPError as e:
      print(e.read())

  def connect(self):
    print('Connecting to endpoint', self.endpoint)
    #websocket.enableTrace(True)
    #self.endpoint = "ws://localhost:8080/"
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
    print('Opened')
    self.opened = True

  def wsOnMessage(self, message):
    # parse
    data = json.loads(message)
    print(data)
    if (data['channel'] == 'trigger:action'):
      print(self.actionService.getActions())
      print("Call action " + data['payload']['action_name'])
      self.send("trigger:action:success", {
        'success': True,
        'id': data['payload']['process_id'],
        'action_name': data['payload']['action_name']
      })
      ret = self.actionService.callAction(data['payload']['action_name'], data['payload']['opts'])
      print("Sending " + ret + " to server")
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
    print(message)

  def wsOnError(self, error):
    print('WS error')
    print(error)

  def wsOnClose(self):
    print('### closed')

  def send(self, channel, obj):
    if not self.opened:
      return
    self.ws.send(json.dumps({
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
    }))
