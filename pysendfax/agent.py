TEMP_DIR = '/tmp'
TIFF_DIR = '/var/spool/asterisk'
OUTGOING_DIR = '/var/spool/asterisk/outgoing'

import writer, os, sys

class Agent:

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
    
    def __init__(self, src_files = [], file_upload_objects = [], quality = 'normal'):
        import time
        self.src_files = src_files
        self.file_upload_objects = file_upload_objects
        self.quality = quality
        self.basename = str(int(time.time()))
        if (file_upload_objects):
            self.src_files += [ f for f in self._generate_src_files() if f]
        print(self.src_files, file=sys.stderr)

    def write_upload_file_to_temp(file_upload_objects):
        for i, fuo in enumerate(file_upload_objects):
            dst_file = TEMP_DIR + "/" + fuo.raw_filename
            if os.path.exists(dst_file):
              os.remove(dst_file)
            fuo.save(dst_file)
            yield dst_file
      
    def _generate_src_files(self):
        for i, fuo in enumerate(self.file_upload_objects):
            print(vars(fuo), file=sys.stderr)
            name, ext = os.path.splitext(fuo.raw_filename)
            filename = self._get_filename_without_extension(TEMP_DIR) + str(i) + '_fuo' + ext
            fuo.save(filename)
            print(filename, file=sys.stderr)
            yield filename
            
            
    def _get_filename_without_extension(self, dir):
        return os.path.join(dir, self.basename)
        
    def _generate_written_pdf_files(self):
        for i, src_file in enumerate(self.src_files):
            dst_file = self._get_filename_without_extension(TEMP_DIR) + str(i) + '.pdf'
            i2pw = writer.ImageFileToPdfFileWriter(src_file, dst_file)
            i2pw.write()
            yield dst_file
            
    def write_tiffg3_file(self):
        pdf_files = [f for f in self._generate_written_pdf_files() if f]

        tiff_file = self._get_filename_without_extension(TIFF_DIR) + '.outgoing.tiff'
        ps2g3w = writer.PdfFilesToTiffG3FileWriter(self.quality,
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
