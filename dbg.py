#!/usr/bin/python
# -*- coding: utf8 -*-

import os, sys
import datetime, time
from datetime import datetime, timedelta

offset = 0.0

__resource__ = os.path.join(  os.getcwd(), 'resources', 'lib' )
sys.path.insert(0, __resource__)

usr, psw = os.getenv('BSCLOGIN', 'user:pass').split(':')

def mk_info_string (e):
  s =  u'T: %s' % timesmk(e)
  if e['title']['-lang']:
    s += u' lang: %s' % e['title']['-lang']
  if e['title']['#cdata-section']:
    s += u' title: %s' % e['title']['#cdata-section']
  if e['desc']['#cdata-section']:
    s += u' desc: %s' % e['desc']['#cdata-section']
  return s

def timesmk(v):
  ts = v.get('-start', None)
  te = v.get('-stop', None)
  if ts is None or te is None:
    return u''
  ts = datetime.fromtimestamp(time.mktime(time.strptime(ts.split()[0], '%Y%m%d%H%M%S'))) + timedelta(minutes=offset)
  te = datetime.fromtimestamp(time.mktime(time.strptime(te.split()[0], '%Y%m%d%H%M%S'))) + timedelta(minutes=offset)
  return u'%s %s' % (ts.strftime("%H:%M:%S"), te.strftime("%H:%M:%S"))

def get_prog_info(ch):
  s = u''
  pr = ch.get('programme', None)
  if pr is None:
    return s

  if isinstance(pr, list):
    for entry in ch['programme']:
      s += mk_info_string(entry)
  elif isinstance(pr, dict):
    s += mk_info_string(pr)
  return s

if __name__ == '__main__':
  import bsc
  print usr, psw
  b = bsc.dodat(base = 'https://api.iptv.bulsat.com',
                login = {'usr': usr,'pass': psw},
                cachepath = 'data.dat',
                cachetime = 60,
                dbg = True,
                timeout = 0.5)

  for g in b.get_genres():
    print '---------- %s ----------' % g.encode('utf-8', 'replace')
    for ch in b.get_all_by_genre(g):
      info = get_prog_info(ch)
      print ('Name: %s Quality: %s Info: %s' % (ch['title'], ch['quality'], ' '.join(info.split()))).encode('utf-8', 'replace')
