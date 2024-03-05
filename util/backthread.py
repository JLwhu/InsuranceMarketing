import threading

from PyQt6.QtCore import QObject, pyqtSignal

from util.MailProcess import MailProcess
import ctypes

class BackThread(threading.Thread, QObject):
    def __init__(self, imap_ssl_host, smtp_host, username, password, subject_string):  #target,
        threading.Thread.__init__(self)
        QObject.__init__(self)
        self.imap_ssl_host = imap_ssl_host
        self.smpt_host = smtp_host
        self.username = username
        self.password = password
        self.subject_string = subject_string

        self.mp = MailProcess()
        self.mp.progress_signal.connect(self.sendProgressMsg)


        #self.multiprocess = MultiProcess()
        #self.multiprocess.progress_signal.connect(self.sendProgressMsg)

    return_progress = pyqtSignal(str)
    cnt =0
    result = ""

    # function using _stop function
    # function using _stop function
    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def run(self):

        self.result = self.call_func(self.imap_ssl_host, self.smpt_host, self.username, self.password, self.subject_string)

    def getResult(self):  # getResult方法可获得func函数return的结果
        threading.Thread.join(self)
        return self.result

    def sendProgressMsg(self,progressstr):
        #self.result = progressstr
        #self.return_value.emit(progressstr)
        self.return_progress.emit(progressstr)

        #self.change_value.emit(2)

    def call_func(self, imap_ssl_host, smtp_host, username, password, subject_string):
        self.mp.readNewEmail_IMAP(imap_ssl_host, smtp_host, username, password, subject_string)





