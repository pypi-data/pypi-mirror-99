import time

from collections import OrderedDict, defaultdict

from typing import Union

from orderedset import OrderedSet
from plenum.common.constants import PROPAGATE, THREE_PC_PREFIX
from plenum.common.messages.internal_messages import RequestPropagates
from plenum.common.messages.node_messages import Propagate
from plenum.common.metrics_collector import MetricsCollector, NullMetricsCollector, MetricsName
from plenum.common.request import Request, ReqKey
from plenum.common.types import f
from plenum.server.quorums import Quorum
from stp_core.common.log import getlogger

logger = getlogger()


class ReqState:
    """
    Object to store the state of the request.
    """

    def __init__(self, request: Request):
        self.request = request
        self.forwarded = False
        # forwardedTo helps in finding to how many replicas has this request
        # been forwarded to, helps in garbage collection
        self.forwardedTo = 0
        self.propagates = {}
        self.finalised = None
        self.executed = False
        self.added_ts = time.perf_counter()
        self.finalised_ts = None
        self.unordered_by_replicas_num = 0

    def req_with_acceptable_quorum(self, quorum: Quorum):
        digests = defaultdict(set)
        # this is workaround because we are getting a propagate from
        # somebody with non-str (byte) name
        for sender, req in filter(lambda x: isinstance(
                x[0], str), self.propagates.items()):
            digests[req.digest].add(sender)
            if quorum.is_reached(len(digests[req.digest])):
                return req

    def set_finalised(self, req):
        # TODO: make it much explicitly and simpler
        # !side affect! if `req` is an instance of a child of `Request` class
        # here we construct the parent from child it is rather implicit that
        # `finalised` contains not the same type than `propagates` has

        # That is needed to create payload digest before cloning req to finalised
        req.payload_digest

        self.finalised = Request.fromState(req.__getstate__())
        self.added_ts = None
        self.finalised_ts = time.perf_counter()


class Requests(OrderedDict):
    """
    Storing client request object corresponding to each client and its
    request id. Key of the dictionary is a Tuple2 containing identifier,
    requestId. Used when Node gets an ordered request by a replica and
    needs to execute the request. Once the ordered request is executed
    by the node and returned to the transaction store, the key for that
    request is popped out
    """
    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.finalised_count = 0

    def add(self, req: Request):
        """
        Add the specified request to this request store.
        """
        key = req.key
        if key not in self:
            self[key] = ReqState(req)
        return self[key]

    def forwarded(self, req: Request) -> bool:
        """
        Returns whether the request has been forwarded or not
        """
        return self[req.key].forwarded

    def ordered_by_replica(self, request_key):
        """
        Should be called by each replica when request is ordered or replica is removed.
        """
        state = self.get(request_key)
        if not state:
            return
        state.unordered_by_replicas_num -= 1

    def mark_as_forwarded(self, req: Request, to: int):
        """
        Works together with 'mark_as_executed' and 'free' methods.

        It marks request as forwarded to 'to' replicas.
        To let request be removed, it should be marked as executed and each of
        'to' replicas should call 'free'.
        """
        self[req.key].forwarded = True
        self[req.key].forwardedTo = to
        self[req.key].unordered_by_replicas_num = to

    def add_propagate(self, req: Request, sender: str):
        """
        Add the specified request to the list of received
        PROPAGATEs.

        :param req: the REQUEST to add
        :param sender: the name of the node sending the msg
        """
        data = self.add(req)
        data.propagates[sender] = req

    def votes(self, req) -> int:
        """
        Get the number of propagates for a given reqId and identifier.
        """
        try:
            votes = len(self[req.key].propagates)
        except KeyError:
            votes = 0
        return votes

    def req_with_acceptable_quorum(self, req: Request, quorum: Quorum):
        state = self[req.key]
        return state.req_with_acceptable_quorum(quorum)

    def set_finalised(self, req: Request):
        state = self[req.key]
        if not state.finalised:
            self.finalised_count += 1
        state.set_finalised(req)

    def mark_as_executed(self, req: Request):
        """
        Works together with 'mark_as_forwarded' and 'free' methods.

        It makes request to be removed if all replicas request was
        forwarded to freed it.
        """
        state = self[req.key]
        state.executed = True
        self._clean(state)

    def free(self, request_key):
        """
        Works together with 'mark_as_forwarded' and
        'mark_as_executed' methods.

        It makes request to be removed if all replicas request was
        forwarded to freed it and if request executor marked it as executed.
        """
        state = self.get(request_key)
        if not state:
            return
        state.forwardedTo -= 1
        self._clean(state)

    def force_free(self, request_key):
        state = self.get(request_key)
        if not state:
            return
        if state.finalised:
            self.finalised_count -= 1
        self.pop(request_key, None)

    def _clean(self, state):
        if state.executed and state.forwardedTo <= 0:
            if state.finalised:
                self.finalised_count -= 1
            self.pop(state.request.key, None)

    def has_propagated(self, req: Request, sender: str) -> bool:
        """
        Check whether the request specified has already been propagated.
        """
        return req.key in self and sender in self[req.key].propagates

    def is_finalised(self, reqKey: str) -> bool:
        return reqKey in self and self[reqKey].finalised

    def digest(self, reqKey: str) -> str:
        if reqKey in self:
            return self[reqKey].request.digest


class Propagator:
    MAX_REQUESTED_KEYS_TO_KEEP = 1000

    def __init__(self, metrics: MetricsCollector = NullMetricsCollector()):
        self.requests = Requests()
        self.requested_propagates_for = OrderedSet()
        self.metrics = metrics

    # noinspection PyUnresolvedReferences
    def propagate(self, request: Request, clientName):
        """
        Broadcast a PROPAGATE to all other nodes

        :param request: the REQUEST to propagate
        """
        if self.requests.has_propagated(request, self.name):
            logger.trace("{} already propagated {}".format(self, request))
        else:
            with self.metrics.measure_time(MetricsName.SEND_PROPAGATE_TIME):
                self.requests.add_propagate(request, self.name)
                propagate = self.createPropagate(request, clientName)
                logger.debug("{} propagating request {} from client {}".format(self, request.key, clientName),
                             extra={"cli": True, "tags": ["node-propagate"]})
                self.send(propagate)

    @staticmethod
    def createPropagate(
            request: Union[Request, dict], client_name) -> Propagate:
        """
        Create a new PROPAGATE for the given REQUEST.

        :param request: the client REQUEST
        :return: a new PROPAGATE msg
        """
        if not isinstance(request, (Request, dict)):
            logger.error("{}Request not formatted properly to create propagate"
                         .format(THREE_PC_PREFIX))
            return
        logger.trace("Creating PROPAGATE for REQUEST {}".format(request))
        request = request.as_dict if isinstance(request, Request) else \
            request
        if isinstance(client_name, bytes):
            client_name = client_name.decode()
        return Propagate(request, client_name)

    # noinspection PyUnresolvedReferences
    def canForward(self, request: Request):
        """
        Determine whether to forward client REQUESTs to replicas, based on the
        following logic:

        - If exactly f+1 PROPAGATE requests are received, then forward.
        - If less than f+1 of requests then probably there's no consensus on the
            REQUEST, don't forward.
        - If more than f+1 then already forwarded to replicas, don't forward

        Even if the node hasn't received the client REQUEST itself, if it has
        received enough number of PROPAGATE messages for the same, the REQUEST
        can be forwarded.

        :param request: the client REQUEST
        """

        if self.requests.forwarded(request):
            return 'already forwarded'

        # If not enough Propagates, don't bother comparing
        if not self.quorums.propagate.is_reached(self.requests.votes(request)):
            return 'not finalised'

        req = self.requests.req_with_acceptable_quorum(request,
                                                       self.quorums.propagate)
        if req:
            self.requests.set_finalised(req)
            return None
        else:
            return 'not finalised'

    # noinspection PyUnresolvedReferences
    def forward(self, request: Request):
        """
        Forward the specified client REQUEST to the other replicas on this node

        :param request: the REQUEST to propagate
        """
        key = request.key
        num_replicas = self.replicas.num_replicas
        logger.debug('{} forwarding request {} to {} replicas'
                     .format(self, key, num_replicas))
        self.replicas.send_to_internal_bus(ReqKey(key))
        self.monitor.requestUnOrdered(key)
        self.requests.mark_as_forwarded(request, num_replicas)

    # noinspection PyUnresolvedReferences
    def recordAndPropagate(self, request: Request, clientName):
        """
        Record the request in the list of requests and propagate.

        :param request:
        :param clientName:
        """
        self.requests.add(request)
        self.propagate(request, clientName)
        self.tryForwarding(request)

    def tryForwarding(self, request: Request):
        """
        Try to forward the request if the required conditions are met.
        See the method `canForward` for the conditions to check before
        forwarding a request.
        """
        cannot_reason_msg = self.canForward(request)
        if cannot_reason_msg is None:
            # If haven't got the client request(REQUEST) for the corresponding
            # propagate request(PROPAGATE) but have enough propagate requests
            # to move ahead
            self.forward(request)
        else:
            logger.trace("{} not forwarding request {} to its replicas "
                         "since {}".format(self, request, cannot_reason_msg))

    def request_propagates(self, request_list: RequestPropagates):
        """
        Request PROPAGATEs for the given request keys. Since replicas can
        request PROPAGATEs independently of each other, check if it has
        been requested recently
        :param req_keys:
        :return:
        """
        req_keys = request_list.bad_requests
        i = 0
        for digest in req_keys:
            if digest not in self.requested_propagates_for:
                if digest not in self.requests:
                    # Request from all nodes
                    self.request_msg(PROPAGATE, {f.DIGEST.nm: digest})
                else:
                    # Request from nodes that didn't send
                    send_to = [conn for conn in self.nodestack.connecteds if
                               conn not in self.requests[digest].propagates.keys()]
                    self.request_msg(PROPAGATE, {f.DIGEST.nm: digest}, frm=send_to)

                self._add_to_recently_requested(digest)
                i += 1
            else:
                logger.debug('{} already requested PROPAGATE recently for {}'.
                             format(self, digest))
        return i

    def _add_to_recently_requested(self, key):
        while len(
                self.requested_propagates_for) > self.MAX_REQUESTED_KEYS_TO_KEEP:
            self.requested_propagates_for.pop(last=False)
        self.requested_propagates_for.add(key)
