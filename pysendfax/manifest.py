MANIFEST = '''
{
    "name": "PySendFax",
    "short_name": "PySendFax",
    "lang": "ja-JP",
    "start_url": "./",
    "display": "standalone",
    "background_color": "white",
    "theme_color": "white",
    "icons":[
    {
    "src":"static/images/icon-192x192.png",
    "sizes":"192x192",
    "type":"image/png"
    },
    {
    "src":"static/images/icon-512x512.png",
    "sizes":"512x512",
    "type":"image/png"
    }],
    "share_target": {
      "action": "./file-collector",
      "method": "POST",
      "enctype": "multipart/form-data",
      "params": {
         "title": "name",
         "text": "description",
         "url": "link",
         "files": [
          {
            "name": "images",
            "accept": ["application/pdf", "image/jpeg", "image/png"]
          }
         ]
      }
    }
}
'''
