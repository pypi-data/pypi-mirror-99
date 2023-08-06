
from Orange.widgets.utils.concurrent import FutureWatcher, ThreadExecutor

from PyQt5.QtCore import pyqtSlot
import concurrent.futures
import zerorpc

SERVER_ADDRESS = "tcp://127.0.0.1:9138"


class RpcClient():

    def __init__(self):
        # Async
        self.executor = ThreadExecutor()
        self.future = None

    def requestData(self, method, callback, d=None):
        if self.future is not None:
            # First make sure any pending tasks are cancelled.
            self.future.cancel()
            self.future = None

        self.future = self.executor.submit(self.getData, method, d)
        # Setup the FutureWatcher to notify us of completion
        self.watcher = FutureWatcher(self.future)
        # by using FutureWatcher we ensure `dataReceived` slot will be
        # called from the main GUI thread by the Qt's event loop
        self.watcher.done.connect(self.rpcDataReceived)
        self.callback = callback


    def getData(self, method, d):

      c = zerorpc.Client(timeout=90, heartbeat=45)
      c.connect(SERVER_ADDRESS)
      data = getattr(c, method)(d);
      return data

    @pyqtSlot(concurrent.futures.Future)
    def rpcDataReceived(self, f):
      self.future = None
      try:
        results = f.result()
        self.callback(results);
        self.error();
      except Exception as ex:
        print(ex)
        self.error("{!r}".format(ex))

