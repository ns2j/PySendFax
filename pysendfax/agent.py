TEMP_DIR = '/tmp'
TIFF_DIR = '/var/spool/asterisk'
OUTGOING_DIR = '/var/spool/asterisk/outgoing'

class Agent:
    import writer, os, time

    OUTGOING_MESSAGE = '''Channel: PJSIP/{channel}
WaitTime: 30
MaxRetries: 2
RetryTime: 300
Archive: yes
Context: {context}
Extension: send
Priority: 1
Set: FAXFILE={faxfile}
Set: FAXNUMBER={faxnumber}
Set: REPLYTO={replyto}
Set: SUBJECT={subject}
'''
    
    def __init__(self, src_files, quality='normal', file_upload_objects = None):
        self.src_files = src_files
        self.quality = quality
        self.basename = str(int(self.time.time()))
        print(file_upload_objects)
        if (file_upload_objects):
            self.src_files = [ f for f in self._generate_src_files(file_upload_objects) if f]
    def _generate_src_files(self, file_upload_objects):
        for i, fuo in enumerate(file_upload_objects):
            print(fuo)
            name, ext = self.os.path.splitext(fuo.raw_filename)
            filename = self._get_filename_without_extension(TEMP_DIR) + str(i) + ext
            fuo.save(filename)
            yield filename
            
            
    def _get_filename_without_extension(self, dir):
        return self.os.path.join(dir, self.basename)
        
    def _generatewrited_pdf_files(self):
        for i, src_file in enumerate(self.src_files):
            dst_file = self._get_filename_without_extension(TEMP_DIR) + str(i) + '.pdf'
            i2pw = self.writer.ImageFileToPdfFileWriter(src_file, dst_file)
            i2pw.write()
            yield dst_file
            
            
    def write_tiffg3_file(self):
        pdf_files = [f for f in self._generatewrited_pdf_files() if f]

        tiff_file = self._get_filename_without_extension(TIFF_DIR) + '.outgoing.tiff'
        ps2g3w = self.writer.PdfFilesToTiffG3FileWriter(self.quality,
                                                        pdf_files, tiff_file)
        ps2g3w.write()
        return tiff_file
        
    def write_call_file(self, **params):
        temp_file = self._get_filename_without_extension(TEMP_DIR) + '.call'
        with open(temp_file, 'w') as f:
            f.write(self.OUTGOING_MESSAGE.format(**params))
        return temp_file
    def mv_call_file(self, from_call_file):
        import shutil
        to_call_file = self._get_filename_without_extension(OUTGOING_DIR) + '.call'
        shutil.move(from_call_file, to_call_file)
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint")
    parser.add_argument("context")
    parser.add_argument("number")
    parser.add_argument("email")
    parser.add_argument("files", nargs="+")
    parser.add_argument("-q", "--quality", default="fine")
    parser.add_argument("-d", "--dry-run", default=False)
    
    args = parser.parse_args()
    print(args)


    agent = Agent(args.files)
    tiff_file = agent.write_tiffg3_file()
    call_file = agent.write_call_file(
        channel = args.number + '@' + args.endpoint,
        context = args.context,
        faxnumber = args.number, faxfile = tiff_file,
        replyto = args.email, subject = "Send Fax To " + args.number)


    agent.mv_call_file(call_file)
