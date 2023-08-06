import time
import threading
from .MessageListener import MessageListener
from .MessageProducer import MessageProducer
from hkube_python_wrapper.util.logger import log
from hkube_python_wrapper.util.DaemonThread import DaemonThread

class StreamingManager(DaemonThread):
    threadLocalStorage = threading.local()

    def __init__(self, errorHandler):
        self.errorHandler = errorHandler
        self.messageProducer = None
        self._messageListeners = dict()
        self._inputListener = []
        self.listeningToMessages = False
        self._isStarted = False
        self.parsedFlows = {}
        self.defaultFlow = None
        DaemonThread.__init__(self, "StreamingManager")

    def setParsedFlows(self, flows, defaultFlow):
        self.parsedFlows = flows
        self.defaultFlow = defaultFlow

    def setupStreamingProducer(self, onStatistics, producerConfig, nextNodes, nodeName):
        self.messageProducer = MessageProducer(producerConfig, nextNodes, nodeName)
        self.messageProducer.registerStatisticsListener(onStatistics)
        if (nextNodes):
            self.messageProducer.start()

    def setupStreamingListeners(self, listenerConfig, parents, nodeName):
        log.debug("parents {parents}", parents=str(parents))
        for parent in parents:
            parentName = parent['nodeName']
            remoteAddress = parent['address']
            remoteAddressUrl = 'tcp://{host}:{port}'.format(host=remoteAddress['host'], port=remoteAddress['port'])

            if (parent['type'] == 'Add'):
                if(self._messageListeners.get(parentName) is None):
                    self._messageListeners[parentName] = dict()
                options = {}
                options.update(listenerConfig)
                options['remoteAddress'] = remoteAddressUrl
                options['messageOriginNodeName'] = parentName
                listener = MessageListener(options, nodeName, self.errorHandler)
                listener.registerMessageListener(self._onMessage)
                self._messageListeners[parentName][remoteAddressUrl] = listener

            if (parent['type'] == 'Del'):
                listeners = self._messageListeners.get(parentName)
                if(listeners):
                    listener = listeners.get(remoteAddressUrl)
                    if(listener):
                        listener.close(force=False)
                        listeners.pop(remoteAddressUrl)

    def registerInputListener(self, onMessage):
        self._inputListener.append(onMessage)

    def _onMessage(self, messageFlowPattern, msg, origin):
        self.threadLocalStorage.messageFlowPattern = messageFlowPattern
        for listener in self._inputListener:
            try:
                listener(msg, origin)
            except Exception as e:
                log.error("hkube_api message listener through exception: {e}", e=str(e))
        self.threadLocalStorage.messageFlowPattern = []

    def run(self):
        while(self.listeningToMessages):
            for listeners in list(self._messageListeners.values()):
                for listener in list(listeners.values()):
                    listener.fetch()
            time.sleep(0.001) # free some cpu

    def startMessageListening(self):
        self.listeningToMessages = True
        if(self._isStarted is False):
            self._isStarted = True
            self.start()

    def sendMessage(self, msg, flowName=None):
        if (self.messageProducer is None):
            raise Exception('Trying to send a message from a none stream pipeline or after close had been applied on algorithm')
        if (self.messageProducer.nodeNames):
            parsedFlow = None
            if (flowName is None):
                if hasattr(self.threadLocalStorage, 'messageFlowPattern') and self.threadLocalStorage.messageFlowPattern:
                    parsedFlow = self.threadLocalStorage.messageFlowPattern
                else:
                    if (self.defaultFlow is None):
                        raise Exception("Streaming default flow is None")
                    flowName = self.defaultFlow
            if not (parsedFlow):
                parsedFlow = self.parsedFlows.get(flowName)
            if (parsedFlow is None):
                raise Exception("No such flow " + flowName)
            self.messageProducer.produce(parsedFlow, msg)

    def stopStreaming(self, force=True):
        if (self.listeningToMessages):
            self.listeningToMessages = False
            for listeners in list(self._messageListeners.values()):
                for listener in list(listeners.values()):
                    listener.close(force)
            self._messageListeners = dict()

        self._inputListener = []
        if (self.messageProducer is not None):
            self.messageProducer.close(force)
            self.messageProducer = None

        self.join()

    def clearMessageListeners(self):
        self._messageListeners = dict()
