import abc
import threading

from .abstract import QueryResult
from .exceptions import BaseException
from .types import Status


# TODO: remove this to a common util
def _parameter_is_empty(func):
    import inspect
    sig = inspect.signature(func)
    # params = sig.parameters
    # todo: add more check to parameter, such as `default parameter`,
    #  `positional-only`, `positional-or-keyword`, `keyword-only`, `var-positional`, `var-keyword`
    # if len(params) == 0:
    #     return True
    # for param in params.values():
    #     if (param.kind == inspect.Parameter.POSITIONAL_ONLY or
    #         param.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD) and \
    #             param.default == inspect._empty:
    #         return False
    return len(sig.parameters) == 0


class AbstractFuture:
    @abc.abstractmethod
    def result(self, **kwargs):
        '''Return deserialized result.

        It's a synchronous interface. It will wait executing until
        server respond or timeout occur(if specified).

        This API is thread-safe.
        '''
        raise NotImplementedError()

    @abc.abstractmethod
    def cancel(self):
        '''Cancle gRPC future.

        This API is thread-safe.
        '''
        raise NotImplementedError()

    @abc.abstractmethod
    def done(self):
        '''Wait for request done.

        This API is thread-safe.
        '''
        raise NotImplementedError()


class Future(AbstractFuture):
    def __init__(self, future, done_callback=None, pre_exception=None):
        self._future = future
        self._done_cb = done_callback  # keep compatible (such as Future(future, done_callback)), deprecated later
        self._done_cb_list = []
        self.add_callback(done_callback)
        self._condition = threading.Condition()
        self._canceled = False
        self._done = False
        self._response = None
        self._results = None
        self._exception = pre_exception

        # self.__init()

    def add_callback(self, func):
        self._done_cb_list.append(func)

    def __del__(self):
        self._future = None

    @abc.abstractmethod
    def on_response(self, response):
        ''' Parse response from gRPC server and return results.
        '''
        raise NotImplementedError()

    def __init(self):
        ''' Register request done callback of gRPC future
        Callback function can be executed in individual subthread of gRPC, so
        there need to notify main thread when callback function finished.
        '''

        def async_done_callback(future):
            with self._condition:
                # delete gRCP future manually
                # self._future.__del__()
                # self._future = None

                # If user specify done callback function, execute it.
                try:
                    self._response = future.result()
                    self._results = self.on_response(self._response)
                    if self._done_cb:
                        if isinstance(self._results, tuple):
                            self._done_cb(*self._results)
                        elif self._results is not None:
                            self._done_cb(self._results)
                        else:
                            self._done_cb()
                except Exception as e:
                    self._exception = e
                finally:
                    self._done = True
                    self._condition.notify_all()

        if self._future:
            self._future.add_done_callback(async_done_callback)

    def result(self, **kwargs):
        self.exception()
        with self._condition:
            # future not finished. wait callback being called.
            to = kwargs.get("timeout", None)
            if self._future and not self._future.done() or not self._response:
                self._response = self._future.result(timeout=to)
                self._results = self.on_response(self._response)

                for cb in self._done_cb_list:
                    if cb:
                        # necessary to check parameter signature of cb?
                        if isinstance(self._results, tuple):
                            cb(*self._results)
                        elif _parameter_is_empty(cb):
                            cb()
                        elif self._results is not None:
                            cb(self._results)
                        else:
                            raise BaseException(1, "callback function is not legal!")

            self._condition.notify_all()

        self.exception()
        if kwargs.get("raw", False) is True:
            # just return response object received from gRPC
            return self._response

        if self._results:
            return self._results
        else:
            return self.on_response(self._response)

    # def result(self, **kwargs):
    #     self.exception()
    #     with self._condition:
    #         # future not finished. wait callback being called.
    #         to = kwargs.get("timeout", None)
    #         if not self._future.done() or not self._response:
    #             self._response = self._future.result(timeout=to)
    #         # if not self._done and not self._canceled:
    #         #     to = kwargs.get("timeout", None)
    #         #     self._condition.wait(to)
    #         #
    #         #     if not self._done and not self._canceled:
    #         #         self._condition.notify_all()
    #         # raise FutureTimeoutError("Wait timeout")

    #         self._condition.notify_all()

    #     self.exception()
    #     if kwargs.get("raw", False) is True:
    #         # just return response object received from gRPC
    #         return self._response

    #     if self._results:
    #         return self._results
    #     else:
    #         return self.on_response(self._response)

    def cancel(self):
        with self._condition:
            if self._future:
                self._future.cancel()
            # if not self._canceled or self._done:
            #     self._future.cancel()
            #     self._canceled = True
            self._condition.notify_all()

    def is_done(self):
        return self._done

    def done(self):
        # self.exception()
        with self._condition:
            if self._future and not self._future.done():
                try:
                    self._future.result()
                except Exception as e:
                    self._exception = e

            self._condition.notify_all()

    def exception(self):
        if self._exception:
            raise self._exception
        if self._future and not self._future.done():
            self._future.exception()


class SearchFuture(Future):
    def __init__(self, future, done_callback=None, auto_id=True, pre_exception=None):
        super().__init__(future, done_callback, pre_exception)
        self._auto_id = auto_id

    def on_response(self, response):
        if response.status.error_code == 0:
            return QueryResult(response, self._auto_id)

        status = response.status
        raise BaseException(status.error_code, status.reason)


class InsertFuture(Future):
    def on_response(self, response):
        status = response.status
        if status.error_code == 0:
            return list(range(response.rowID_begin, response.rowID_end))
            # return list(response.entity_id_array)

        status = response.status
        raise BaseException(status.error_code, status.reason)


class CreateIndexFuture(Future):
    def on_response(self, response):
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)

        return Status(response.error_code, response.reason)


class CreateFlatIndexFuture(AbstractFuture):
    def __init__(self, res, done_callback=None, pre_exception=None):
        self._results = res
        self._done_cb = done_callback
        self._done_cb_list = []
        self.add_callback(done_callback)
        self._condition = threading.Condition()
        self._exception = pre_exception

    def add_callback(self, func):
        self._done_cb_list.append(func)

    def __del__(self):
        self._results = None

    def on_response(self, response):
        pass

    def result(self, **kwargs):
        self.exception()
        with self._condition:
            for cb in self._done_cb_list:
                if cb:
                    # necessary to check parameter signature of cb?
                    if isinstance(self._results, tuple):
                        cb(*self._results)
                    elif _parameter_is_empty(cb):
                        cb()
                    elif self._results is not None:
                        cb(self._results)
                    else:
                        raise BaseException(1, "callback function is not legal!")
            return self._results

    def cancel(self):
        with self._condition:
            self._condition.notify_all()

    def is_done(self):
        return True

    def done(self):
        with self._condition:
            self._condition.notify_all()

    def exception(self):
        if self._exception:
            raise self._exception


class FlushFuture(Future):
    def on_response(self, response):
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)


class LoadCollectionFuture(Future):
    def on_response(self, response):
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)


class LoadPartitionsFuture(Future):
    def on_response(self, response):
        if response.error_code != 0:
            raise BaseException(response.error_code, response.reason)
