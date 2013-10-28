import threading
import multiprocessing
import multiprocessing.queues
import lirc
import pifacecommon.interrupts


class IREvent(object):
    """An IR event."""
    def __init__(self, ir_code):
        self.ir_code = ir_code


class IRFunctionMap(pifacecommon.interrupts.FunctionMap):
    """Maps an IR code to callback function."""
    def __init__(self, ir_code, callback):
        self.ir_code = ir_code
        super(IRFunctionMap, self).__init__(callback)


class IREventListener(object):
    """Listens for IR events and calls the registered functions. `prog`
    specifies

    >>> def print_ir_code(event):
    ...     print(event.ir_code)
    ...
    >>> listener = pifacecad.IREventListener(prog="myprogram")
    >>> listener.register('one', print_ir_code)
    >>> listener.activate()
    """

    TERMINATE_SIGNAL = "astalavista"

    def __init__(self, prog, lircrc=None):
        self.prog = prog
        self.lircrc = lircrc
        self.ir_function_maps = list()
        self.event_queue = multiprocessing.queues.SimpleQueue()
        self.detector = multiprocessing.Process(
            target=watch_ir_events, args=(self.event_queue,))
        self.dispatcher = threading.Thread(
            target=pifacecommon.interrupts.handle_events, args=(
                self.ir_function_maps,
                self.event_queue,
                _event_matches_ir_function_map,
                IREventListener.TERMINATE_SIGNAL))

    def register(self, ir_code, callback):
        """Registers an ir_code to a callback function.

        :param ir_code: The IR code.
        :type ir_code: int
        :param callback: The function to run when event is detected.
        :type callback: function
        """
        self.ir_function_maps.append(IRFunctionMap(ir_code, callback))

    def activate(self):
        """When activated the :class:`IREventListener` will run callbacks
        associated with IR codes.
        """
        lirc.init(self.prog, self.lircrc)
        self.dispatcher.start()
        self.detector.start()

    def deactivate(self):
        """When deactivated the :class:`IREventListener` will not run
        anything.
        """
        self.event_queue.put(self.TERMINATE_SIGNAL)
        self.dispatcher.join()
        self.detector.terminate()  # maybe use a message queue instead?
        lirc.deinit()


def _event_matches_ir_function_map(event, ir_function_map):
    return event.ir_code == ir_function_map.ir_code


def watch_ir_events(event_queue):
    """Waits for IR code events and places them on the event queue.

    :param event_queue: A queue to put events on.
    :type event_queue: :py:class:`multiprocessing.Queue`
    """
    while True:
        for ir_code in lirc.nextcode():
            event_queue.put(IREvent(ir_code))
