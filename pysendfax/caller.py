TEMP_DIR = '/tmp'

class Caller:
    def __init__(self, endpoint, context, number, email, file_upload_objects, quality = 'normal'):
        self.endpoint = endpoint
        self.context = context
        self.number = number
        self.email = email
        self.file_upload_objects = file_upload_objects
        self.quality = quality
        
    def call(self, dry_run = False):
        import agent, os
        agent = agent.Agent(None, file_upload_objects = self.file_upload_objects, quality = self.quality)
        tiff_file = agent.write_tiffg3_file()
        if (os.path.isfile(tiff_file) == False):
            raise RuntimeError(f'''Write tiffg3 File Error!
tiff_file: {tiff_file}
''')
        call_file = agent.write_call_file(
            channel = self.number + '@' + self.endpoint,
            context = self.context,
            faxnumber = self.number, faxfile = tiff_file,
            replyto = self.email, subject = "Send Fax To " + self.number)
        if (dry_run == False):
            agent.mv_call_file(call_file)
            
        
        



