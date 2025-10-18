import abc

class Commandable:
    @abc.abstractmethod
    def get_command(self):
        raise NotImplementedError()

class Writable:
    @abc.abstractmethod
    def write(self):
        raise NotImplementedError()
    
class CommandableWriter(Commandable, Writable):
    def write(self):
        import subprocess
        proc = subprocess.Popen(self.get_command(), stderr=subprocess.PIPE)
        r = proc.communicate()
        if (proc.returncode != 0):
            print(f'{proc.returncode}: {r[1]}')
            command = self.get_command()
            raise RuntimeError(f'''
 Command Execute Error!
 command: {command}
 returncode: {proc.returncode}
 message: {r[1]}
 ''')
    
class ImageFileToPdfFileWriter(CommandableWriter):
    def __init__(self, from_file, to_file):
        self.from_file = from_file
        self.to_file = to_file
        
    def get_command(self):
        return ['magick', self.from_file, self.to_file]


class PdfFilesToTiffG3FileWriter(CommandableWriter):
    RESOLUTIONS = {
        'normal': '-r204x98',
        'fine': '-r204x196',
        'super': '-r204x392',
    }

    def __init__(self, quality, pdf_files, tiff_file):
        self.quality = quality
        self.pdf_files = pdf_files
        self.tiff_file = tiff_file
        
    def get_command(self):
        return [
            'gs', '-q', '-dNOPAUSE', '-dBATCH',
            '-sDEVICE=tiffg3', '-sPAPERSIZE=a4', '-dFIXEDMEDIA', '-dPDFFitPage', self.RESOLUTIONS[self.quality],
            '-sOutputFile='+self.tiff_file] + self.pdf_files


if __name__ == '__main__':
    import sys

    i2pw = ImageFileToPdfFileWriter(sys.argv[1], '/tmp/junk.pdf')
    i2pw.write()
    i2pw2 = ImageFileToPdfFileWriter(sys.argv[1], '/tmp/junk2.pdf')
    i2pw2.write()

    ps2g3w = PdfFilesToTiffG3FileWriter('fine', ['/tmp/junk.pdf'], '/tmp/junk.tiff')
    ps2g3w.write()
