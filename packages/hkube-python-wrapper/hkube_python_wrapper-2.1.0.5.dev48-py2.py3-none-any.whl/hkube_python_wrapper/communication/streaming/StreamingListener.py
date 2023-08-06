import time
from hkube_python_wrapper.util.DaemonThread import DaemonThread

class StreamingListener(DaemonThread):

    def __init__(self, messageListeners):
        self._listeningToMessages = True
        self._messageListeners = messageListeners
        DaemonThread.__init__(self, "StreamingListener")

    def run(self):
        while(self._listeningToMessages):
            messageListeners = self._messageListeners()
            for listener in list(messageListeners.values()):
                listener.fetch()
            # time.sleep(0.010) # free some cpu

    def stop(self, force=True):
        messageListeners = self._messageListeners()
        for listener in list(messageListeners.values()):
            listener.close(force)
        self._listeningToMessages = False
