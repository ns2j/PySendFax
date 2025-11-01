#! /usr/bin/python3

from bottle import Bottle, default_app, static_file, route, run, template, request, response
import os, sys
import html, manifest, sw

@route('/static/<file_path:path>')
def server_static(file_path):
  return static_file(file_path, root=os.path.dirname(__file__) + '/static/')


@route('/')
def home():
  return template(html.MAIN_HTML, files=None)


@route('/send', method='POST')
def send():
  import caller, re

  print(request.forms.number)
  if (re.match(r'^([0-9]|-)+$', request.forms.number) == None):
    return template(html.ERROR_PAGE, messages = ['不正な電話番号'])

  shares = request.forms.getall('share')
  print(shares, file=sys.stderr)
  uploads = request.files.getall('file')
  print(uploads, file=sys.stderr)
  uploads = list(filter(lambda x: True if x.raw_filename else False, uploads))
  print(uploads, file=sys.stderr)
  print(context)
  print(endpoint)
  c = caller.Caller(endpoint, context, 
         request.forms.number.replace('-', ''),
         request.forms.email,
	 shares, uploads,
	 request.forms.quality)
  try:
    #c.call(dry_run = True)
    c.call()
  except Exception as e:
    return template(html.ERROR_PAGE, messages = f"Error: {e=}".split('\n'))

  return template(html.SEND_HTML, email = request.forms.email)
  
@route('/file-collector', method='POST')
def colect_file():
  uploads = request.files.getall('images')
  print(vars(request.files), file=sys.stderr)
  print(uploads, file=sys.stderr)
  from agent import Agent
  files = [ f for f in Agent.write_upload_file_to_temp(uploads) if f ]
  print(uploads, file=sys.stderr)
  return template(html.MAIN_HTML, files = files)

@route('/manifest')
def get_manifest():
  return template(manifest.MANIFEST)

@route('/sw.js')
def get_sw_js():
  response.content_type='text/javascript'
  return template(sw.SW_JS)

@route('/hello/<name>')
def greet(name):
  return template('<b>Hello {{name}}</b>!', name=name)

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("host")
  parser.add_argument("port")
  parser.add_argument("endpoint")
  parser.add_argument("context")
  parser.add_argument("-a", "--app", default = "/")

  args = parser.parse_args()

  context = args.context
  endpoint = args.endpoint
   
  root = Bottle()
  root.mount(args.app, default_app())
  root.run(host=args.host, port=args.port)

