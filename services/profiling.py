import signal
import inspect
import cProfile
import pstats
import io
import json
import os
import time
import operator
from itertools import chain

class Profiling:

  def __init__(self):
    self.pr = cProfile.Profile()

  def start(self):
    print('Start PROOOOOOOFILIIIIIIING')
    self.pr.enable()

  def stop(self):
    print('Stop PROOOOOOOFILIIIIIIING')
    self.pr.disable()
    ps = pstats.Stats(self.pr).strip_dirs().sort_stats('cumulative')
    f = open("p5.json", "w")
    f.write(json.dumps(json_stats(ps)))
    f.close()
    #for stat in ps.get_print_list([]):
    #  print('')
    #  print('')
    #  if type(stat) is list:
    #    for sta in stat:
    #      print('')
    #      print(sta)
    #print(s.getvalue())


keyfmt = '{0}:{1}({2})'.format

def _replace_keys(d):
  return dict((keyfmt(*k), v) for k, v in d.items())

def json_stats(stats):
    """
    Convert the all_callees data structure to something compatible with
    JSON. Mostly this means all keys need to be strings.
    """

    stats.calc_callees()
    rstats = _replace_keys(stats.all_callees)

    nstats = []

    # find root then getStat
    for k, v in rstats.items():
      print('New loop')
      print(len(nstats))
      print('')
      print('')
      #if (k == "~:0(<built-in method builtins.exec>)"):
      nstats.append(getStat(rstats, k, v, []))
      #nstats = getStat(rstats, k, v, [])

    f = open("p5.json", "w")
    f.write(json.dumps(nstats))
    f.close()

    # remove anything that both never called anything and was never called
    # by anything.
    # this is profiler cruft.
    #no_calls = set(k for k, v in nstats.items() if not v['children'])
    #called = set(chain.from_iterable(
    #    d['children'].keys() for d in nstats.values()))
    #cruft = no_calls - called

    #for c in cruft:
    #    del nstats[c]

    return nstats

def getStat(stats, k, v, dontUse):
  print('')
  #print('Gettin stats for:')
  print(k)
  #print(v)
  nstats = {
    'name': k
  }
  dontUse.append(k)
  #nstats['children'] = dict(
  #    (keyfmt(*ck), list(cv)) for ck, cv in v.items())
  print(v)
  cstats = _replace_keys(stats[k])
  #print(cstats)
  #nstats['stats'] = list(stats[k])
  if (len(cstats) != 0 and k in cstats):
    print(cstats)
    nstats['stats'] = cstats[k]
  nstats['callers'] = []
  for cv in cstats:
    if not cv in dontUse:
      nstats['callers'].append(getStat(stats, cv, stats[cv], dontUse))

  if len(nstats['callers']) == 0:
    nstats.pop('callers')

  return nstats