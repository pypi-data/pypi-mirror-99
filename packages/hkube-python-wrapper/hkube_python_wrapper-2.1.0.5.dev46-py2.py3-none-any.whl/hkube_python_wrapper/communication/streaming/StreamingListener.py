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
            for listeners in list(messageListeners.values()):
                for listener in list(listeners.values()):
                    listener.fetch()
            time.sleep(0.008) # free some cpu

    def stop(self, force=True):
        self._listeningToMessages = False
        messageListeners = self._messageListeners()
        for listeners in list(messageListeners.values()):
            for listener in list(listeners.values()):
                listener.close(force)
