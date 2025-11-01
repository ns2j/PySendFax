MAIN_HTML = '''
<html>
  <head>
    <title>FAX送信</title>
    <link rel="icon" href="./static/images/favicon.ico">
    <link rel="manifest" href="./manifest">
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <script>
    window.onload = () => {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker
         .register('sw.js', { scope: './'});
      }
    }
    </script>
    <script>
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
      <% if files: %>
      <div>
        共有ファイル
        <% for f in files: %>
        <div>
          <input name="share" type="text" value="{{f}}">
        </div>
        <% end %>
      <% end %>
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
'''

ERROR_PAGE =  '''
<!DOCTYPE html>
<html lang="ja">
  <head>
    <title>fax送信でエラー</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
  </head>
  <body>
<% for m in messages: %>
  {{m}}<br/>
<% end %>
  <a href="./">戻る</a>

  </body>
</html>
'''

SEND_HTML = '''
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
'''
  

