from __future__ import print_function
import sys
import multiprocessing
import dill
from tqdm.auto import tqdm
from traceback import format_exc
from pickle import PicklingError, dispatch_table

PY3 = (sys.hexversion >= 0x3000000)

try:
    from cStringIO import StringIO
except ImportError:
    if PY3:
        from io import BytesIO as StringIO
    else:
        from StringIO import StringIO

failed_rv = (lambda *args, **kwargs: None, ())


class Pickler(dill.Pickler):
    """ Overload dill to ignore unpickleble parts of objects.
        You probably didn't want to use these parts anyhow.
        However, if you did, you'll have to find some way to make them pickleble.
    """
    def save(self, obj, save_persistent_id=True):
        """ Copied from pickle and amended. """
        if PY3:
            self.framer.commit_frame()

        # Check for persistent id (defined by a subclass)
        pid = self.persistent_id(obj)
        if pid is not None and save_persistent_id:
            self.save_pers(pid)
            return

        # Check the memo
        x = self.memo.get(id(obj))
        if x is not None:
            self.write(self.get(x[0]))
            return

        rv = NotImplemented
        reduce = getattr(self, "reducer_override", None)
        if reduce is not None:
            rv = reduce(obj)

        if rv is NotImplemented:
            # Check the type dispatch table
            t = type(obj)
            f = self.dispatch.get(t)
            if f is not None:
                f(self, obj)  # Call unbound method with explicit self
                return

            # Check private dispatch table if any, or else
            # copyreg.dispatch_table
            reduce = getattr(self, 'dispatch_table', dispatch_table).get(t)
            if reduce is not None:
                rv = reduce(obj)
            else:
                # Check for a class with a custom metaclass; treat as regular
                # class
                if issubclass(t, type):
                    self.save_global(obj)
                    return

                # Check for a __reduce_ex__ method, fall back to __reduce__
                reduce = getattr(obj, "__reduce_ex__", None)
                try:
                    if reduce is not None:
                        rv = reduce(self.proto)
                    else:
                        reduce = getattr(obj, "__reduce__", None)
                        if reduce is not None:
                            rv = reduce()
                        else:
                            raise PicklingError("Can't pickle %r object: %r" %
                                                (t.__name__, obj))
                except:
                    rv = failed_rv

        # Check for string returned by reduce(), meaning "save as global"
        if isinstance(rv, str):
            try:
                self.save_global(obj, rv)
            except:
                self.save_global(obj, failed_rv)
            return

        # Assert that reduce() returned a tuple
        if not isinstance(rv, tuple):
            raise PicklingError("%s must return string or tuple" % reduce)

        # Assert that it returned an appropriately sized tuple
        l = len(rv)
        if not (2 <= l <= 6):
            raise PicklingError("Tuple returned by %s must have "
                                "two to six elements" % reduce)

        # Save the reduce() output and finally memoize the object
        try:
            self.save_reduce(obj=obj, *rv)
        except:
            self.save_reduce(obj=obj, *failed_rv)


def dumps(obj, protocol=None, byref=None, fmode=None, recurse=True, **kwds):
    """pickle an object to a string"""
    protocol = dill.settings['protocol'] if protocol is None else int(protocol)
    _kwds = kwds.copy()
    _kwds.update(dict(byref=byref, fmode=fmode, recurse=recurse))
    file = StringIO()
    Pickler(file, protocol, **_kwds).dump(obj)
    return file.getvalue()


def chunks(n, *args):
    """ Yield successive n-sized chunks from lists. """
    A = len(args) == 1
    N = len(args[0])
    n = int(round(N/max(1, round(N/n))))
    for i in range(0, N, n) if N else []:
        if A:
            yield args[0][i:i+n]
        else:
            yield [a[i:i+n] for a in args]


class tqdmm(tqdm):
    """ Overload tqdm to make a special version of tqdm functioning as a meter. """

    def __init__(self, *args, **kwargs):
        self._n = 0
        self.disable = False
        if 'bar_format' not in kwargs and len(args) < 16:
            kwargs['bar_format'] = '{n}/{total}'
        super(tqdmm, self).__init__(*args, **kwargs)

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        if not value == self.n:
            self._n = int(value)
            self.refresh()

    def __exit__(self, exc_type=None, exc_value=None, traceback=None):
        if not self.leave:
            self.n = self.total
        super(tqdmm, self).__exit__(exc_type, exc_value, traceback)


def parfor(*args, **kwargs):
    """ @parfor(iterator=None, args=(), kwargs={}, length=None, desc=None, bar=True, qbar=True, rP=1/3, serial=4):
        decorator to parallize for-loops

        required arguments:
            fun:    function taking arguments: iteration from  iterable, other arguments defined in args & kwargs
            iterable: iterable from which an item is given to fun as a first argument

        optional arguments:
            args:   tuple with other unnamed arguments to fun
            kwargs: dict with other named arguments to fun
            length: give the length of the iterator in cases where len(iterator) results in an error
            desc:   string with description of the progress bar
            bar:    bool enable progress bar
            pbar:   bool enable buffer indicator bar
            rP:     ratio workers to cpu cores, default: 1
            nP:     number of workers, default: None, overrides rP if not None
                number of workers will always be at least 2
            serial: switch to serial if number of tasks less than serial, default: 4

        output:       list with results from applying the decorated function to each iteration of the iterator
                      specified as the first argument to the function

        examples:
            << from time import sleep

            <<
            @parfor(range(10), (3,))
            def fun(i, a):
                sleep(1)
                return a*i**2
            fun

            >> [0, 3, 12, 27, 48, 75, 108, 147, 192, 243]

            <<
            @parfor(range(10), (3,), bar=False)
            def fun(i, a):
                sleep(1)
                return a*i**2
            fun

            >> [0, 3, 12, 27, 48, 75, 108, 147, 192, 243]

            <<
            def fun(i, a):
                sleep(1)
                return a*i**2
            pmap(fun, range(10), (3,))

            >> [0, 3, 12, 27, 48, 75, 108, 147, 192, 243]

            equivalent to using the deco module:
            <<
            @concurrent
            def fun(i, a):
                time.sleep(1)
                return a*i**2

            @synchronized
            def run(iterator, a):
                res = []
                for i in iterator:
                    res.append(fun(i, a))
                return res

            run(range(10), 3)

            >> [0, 3, 12, 27, 48, 75, 108, 147, 192, 243]

            all equivalent to the serial for-loop:
            <<
            a = 3
            fun = []
            for i in range(10):
                sleep(1)
                fun.append(a*i**2)
            fun

            >> [0, 3, 12, 27, 48, 75, 108, 147, 192, 243]
        """
    def decfun(fun):
        return pmap(fun, *args, **kwargs)
    return decfun


class parpool(object):
    """ Parallel processing with addition of iterations at any time and request of that result any time after that.
        The target function and its argument can be changed at any time.
    """
    def __init__(self, fun=None, args=None, kwargs=None, rP=None, nP=None, bar=None, qbar=None, terminator=None):
        """ fun, args, kwargs: target function and its arguments and keyword arguments
            rP: ratio workers to cpu cores, default: 1
            nP: number of workers, default, None, overrides rP if not None
            bar, qbar: instances of tqdm and tqdmm to use for monitoring buffer and progress """
        if rP is None and nP is None:
            self.nP = int(multiprocessing.cpu_count())
        elif nP is None:
            self.nP = int(round(rP * multiprocessing.cpu_count()))
        else:
            self.nP = int(nP)
        self.nP = max(self.nP, 2)
        self.fun = fun or (lambda x: x)
        self.args = args or ()
        self.kwargs = kwargs or {}
        if hasattr(multiprocessing, 'get_context'):
            ctx = multiprocessing.get_context('spawn')
        else:
            ctx = multiprocessing
        self.A = ctx.Value('i', self.nP)
        self.E = ctx.Event()
        self.Qi = ctx.Queue(3*self.nP)
        self.Qo = ctx.Queue(3*self.nP)
        self.P = ctx.Pool(self.nP, self._worker(self.Qi, self.Qo, self.A, self.E, terminator))
        self.is_alive = True
        self.res = {}
        self.handle = 0
        self.handles = []
        self.bar = bar
        self.qbar = qbar
        if self.qbar is not None:
            self.qbar.total = 3*self.nP

    @property
    def fun(self):
        return self._fun[1:]

    @fun.setter
    def fun(self, fun):
        funs = dumps(fun, recurse=True)
        self._fun = (fun, hash(funs), funs)

    @property
    def args(self):
        return self._args[1:]

    @args.setter
    def args(self, args):
        argss = dumps(args, recurse=True)
        self._args = (args, hash(argss), argss)

    @property
    def kwargs(self):
        return self._kwargs[1:]

    @kwargs.setter
    def kwargs(self, kwargs):
        kwargss = dumps(kwargs, recurse=True)
        self._kwargs = (kwargs, hash(kwargss), kwargss)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def _getfromq(self):
        """ Get an item from the queue and store it. """
        try:
            err, i, res = self.Qo.get(True, 0.02)
            if not err:
                self.res[i] = dill.loads(res)
            else:
                n, fun, args, kwargs, e = [dill.loads(r) for r in res]
                print('Error from process working on iteration {}:\n'.format(i))
                print(e)
                self.close()
                print('Retrying in main thread...')
                self.res[i] = fun(n, *args, **kwargs)
                raise Exception('Function \'{}\' cannot be executed by parfor, amend or execute in serial.'
                                .format(fun.__name__))
            if self.bar is not None:
                self.bar.update()
            self._qbar_update()
        except multiprocessing.queues.Empty:
            pass

    def __call__(self, n, fun=None, args=None, kwargs=None, handle=None):
        """ Add new iteration, using optional manually defined handle."""
        if self.is_alive and not self.E.is_set():
            n = dumps(n, recurse=True)
            if fun is not None:
                self.fun = fun
            if args is not None:
                self.args = args
            if kwargs is not None:
                self.kwargs = kwargs
            while self.Qi.full():
                self._getfromq()
            if handle is None:
                handle = self.handle
                self.handle += 1
                self.handles.append(handle)
                self.Qi.put((handle, n, self.fun, self.args, self.kwargs))
                self._qbar_update()
                return handle
            elif handle not in self:
                self.handles.append(handle)
                self.Qi.put((handle, n, self.fun, self.args, self.kwargs))
            self._qbar_update()

    def _qbar_update(self):
        if self.qbar is not None:
            try:
                self.qbar.n = self.Qi.qsize()
            except:
                pass

    def __setitem__(self, handle, n):
        """ Add new iteration. """
        self(n, handle=handle)

    def __getitem__(self, handle):
        """ Request result and delete its record. Wait if result not yet available. """
        if handle not in self:
            raise ValueError('No handle: {}'.format(handle))
        while handle not in self.res:
            self._getfromq()
        self.handles.remove(handle)
        return self.res.pop(handle)

    def get_newest(self):
        """ Request the newest key and result and delete its record. Wait if result not yet available. """
        if len(self.handles):
            while not len(self.res):
                self._getfromq()
            key = list(self.res.keys())[0]
            return key, self[key]

    def __delitem__(self, handle):
        self[handle]

    def __contains__(self, handle):
        return handle in self.handles

    def __repr__(self):
        if self.is_alive:
            return '{} with {} workers.'.format(self.__class__, self.nP)
        else:
            return 'Closed {}'.format(self.__class__)

    def close(self):
        if self.is_alive:
            self.is_alive = False
            self.E.set()
            self.P.close()
            while self.A.value:
                self._empty_queue(self.Qi)
                self._empty_queue(self.Qo)
            self._empty_queue(self.Qi)
            self._empty_queue(self.Qo)
            self.P.join()
            self._close_queue(self.Qi)
            self._close_queue(self.Qo)
            self.res = {}
            self.handle = 0
            self.handles = []

    @staticmethod
    def _empty_queue(Q):
        if not Q._closed:
            while not Q.empty():
                try:
                    Q.get(True, 0.02)
                except multiprocessing.queues.Empty:
                    pass

    @staticmethod
    def _close_queue(Q):
        if not Q._closed:
            while not Q.empty():
                try:
                    Q.get(True, 0.02)
                except multiprocessing.queues.Empty:
                    pass
            Q.close()
        Q.join_thread()

    class _worker(object):
        """ Manages executing the target function which will be executed in different processes. """
        def __init__(self, Qi, Qo, A, E, terminator, cachesize=48):
            self.cache = []
            self.Qi = Qi
            self.Qo = Qo
            self.A = A
            self.E = E
            self.terminator = dumps(terminator, recurse=True)
            self.cachesize = cachesize

        def add_to_q(self, value):
            while not self.E.is_set():
                try:
                    self.Qo.put(value, timeout=0.1)
                    break
                except multiprocessing.queues.Full:
                    continue

        def __call__(self):
            while not self.E.is_set():
                i, n, Fun, Args, Kwargs = [None]*5
                try:
                    i, n, Fun, Args, Kwargs = self.Qi.get(True, 0.02)
                    fun = self.get_from_cache(*Fun)
                    args = self.get_from_cache(*Args)
                    kwargs = self.get_from_cache(*Kwargs)
                    self.add_to_q((False, i, dumps(fun(dill.loads(n), *args, **kwargs), recurse=True)))
                except multiprocessing.queues.Empty:
                    continue
                except:
                    self.add_to_q((True, i, (n, Fun[1], Args[1], Kwargs[1], dumps(format_exc(), recurse=True))))
                    self.E.set()
            terminator = dill.loads(self.terminator)
            if terminator is not None:
                terminator()
            with self.A.get_lock():
                self.A.value -= 1

        def get_from_cache(self, h, ser):
            if len(self.cache):
                hs, objs = zip(*self.cache)
                if h in hs:
                    return objs[hs.index(h)]
            obj = dill.loads(ser)
            self.cache.append((h, obj))
            while len(self.cache) > self.cachesize:
                self.cache.pop(0)
            return obj


def pmap(fun, iterable=None, args=None, kwargs=None, length=None, desc=None, bar=True, qbar=False, terminator=None,
         rP=1, nP=None, serial=4):
    """ map a function fun to each iteration in iterable
            best use: iterable is a generator and length is given to this function

        fun:    function taking arguments: iteration from  iterable, other arguments defined in args & kwargs
        iterable: iterable from which an item is given to fun as a first argument
        args:   tuple with other unnamed arguments to fun
        kwargs: dict with other named arguments to fun
        length: give the length of the iterator in cases where len(iterator) results in an error
        desc:   string with description of the progress bar
        bar:    bool enable progress bar
        pbar:   bool enable buffer indicator bar
        terminator: function which is executed in each worker after all the work is done
        rP:     ratio workers to cpu cores, default: 1
        nP:     number of workers, default, None, overrides rP if not None
        serial: switch to serial if number of tasks less than serial, default: 4
    """
    args = args or ()
    kwargs = kwargs or {}
    try:
        length = len(iterable)
    except:
        pass
    if length and length < serial:  # serial case
        return [fun(c, *args, **kwargs) for c in tqdm(iterable, total=length, desc=desc, disable=not bar)]
    else:                           # parallel case
        with tqdmm(total=0, desc='Task buffer', disable=not qbar, leave=False) as qbar,\
             tqdm(total=length, desc=desc, disable=not bar) as bar:
            with parpool(fun, args, kwargs, rP, nP, bar, qbar, terminator) as p:
                length = 0
                for i, j in enumerate(iterable):  # add work to the queue
                    p[i] = j
                    if bar.total is None or bar.total < i+1:
                        bar.total = i+1
                    length += 1
                return [p[i] for i in range(length)]  # collect the results
