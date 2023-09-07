import logging
import os
class FixedSizeRotatingFileHandler(logging.FileHandler):
    def __init__(self, filename, mode='a+', maxBytes=0, encoding=None, delay=0):
        logging.FileHandler.__init__(self, filename, mode, encoding, delay)
        self.maxBytes = maxBytes

    def emit(self, record):
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:  # Are we rolling over?
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, os.SEEK_END)  # Go to the end of the file
            if self.stream.tell() + len(msg) > self.maxBytes:
                # Figure out how much we need to trim from the start
                trim_length = len(msg)
                self.stream.seek(0)  # Go to the start
                self.stream.read(trim_length)  # "read out" the part we want to trim
                remaining_log = self.stream.read()  # save the remaining log content
                self.stream.seek(0)
                self.stream.truncate()  # empty the file
                self.stream.write(remaining_log)
            self.stream.write(msg)
            self.stream.flush()
        else:
            logging.FileHandler.emit(self, record)


