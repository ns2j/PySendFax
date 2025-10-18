#! /usr/bin/python3

from bottle import route, run, template, request

@route('/')
def home():
  return template('''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>fax送信</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <script>
    function init() {
      //document.querySelector('#dropable').addEventListener('drop', (event) => alert('ok'))
      console.log(document.querySelector('#dropable'))
    }
    function dropHandler(ev) {
      console.log(ev)
      const container = new DataTransfer()
      if (ev.dataTransfer.items) {
        [...ev.dataTransfer.items].forEach((item, i) => {
          console.log(item)
          const file = item.getAsFile()
          console.log(file)
          container.items.add(file)
        })
        document.querySelector('#fileinput').files = container.files
	ev.preventDefault()
      } else {
        [...ev.dataTransfer.files].forEach((file, i) => {
          console.log(file)
        })
      }
      ev.preventDefault()
    }
    function dragoverHandler(ev) {
      ev.preventDefault()
    }
  </script>
  <body onload="init()">
    <form action="./send" method="post" enctype="multipart/form-data">
      <div>
        <label>fax番号: </label>
        <input type="text" id="number" name="number">
      </div>
      <div>
        <label>自分のemail</label>
        <input type="text" id="email" name="email">
      </div>
      <div>
        <label>品質</label>
        <select id="qualiity" name="quality">
          <option>normal</option>
          <option>fine</option>
          <option>super</option>
        </select>
      </div>
      <div>
        <label>pdfファイル: </label>
        <input id="fileinput" type="file" id="file" name="file" multiple>
      </div>
      <div id="dropable" style="width: 100%; height: 10em; background-color: #aaaaaa" ondrop="dropHandler(event)" ondragover="dragoverHandler(event)">
         <h1>ここにファイルドロップ</h1>
      </div>
      <input type="submit" value="fax送信">
    </form>
  </body>

</html>
''')

ERROR_PAGE =  '''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>fax送信でエラー</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />  </head>
  <body>
<% for m in messages: %>
  {{m}}<br/>
<% end %>
  <a href="./">戻る</a>

  </body>
</html>
'''


@route('/send', method='POST')
def send():
  import caller, re

  print(request.forms.number)
  if (re.match(r'^([0-9]|-)+$', request.forms.number) == None):
    return template(ERROR_PAGE, messages = ['不正な電話番号'])

  files = request.files.getall('file')
  print(files)
  print(context)
  print(endpoint)
  c = caller.Caller(endpoint, context, 
         request.forms.number.replace('-', ''),
         request.forms.email, files, quality = request.forms.quality)
  try:
    #c.call(dry_run = True)
    c.call()
  except Exception as e:
    return template(ERROR_PAGE, messages = f"Error: {e=}".split('\n'))

  return template('''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>fax送信試行</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />  </head>
  <body>
  fax送信試行します。<br>
  e-mailを確認してください。e-mailアドレスは、{{email}}です。<br>
  <a href="./">戻る</a>

  </body>
</html>
''', email = request.forms.email)
  

@route('/hello/<name>')
def greet(name):
  return template('<b>Hello {{name}}</b>!', name=name)


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("host")
parser.add_argument("port")
parser.add_argument("endpoint")
parser.add_argument("context")

args = parser.parse_args()

context = args.context
endpoint = args.endpoint

run(host=args.host, port=args.port)

