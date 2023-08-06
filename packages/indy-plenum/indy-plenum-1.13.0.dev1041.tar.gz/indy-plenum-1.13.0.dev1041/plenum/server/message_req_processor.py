from typing import Dict, List

from plenum.common.constants import LEDGER_STATUS, CONSISTENCY_PROOF, PROPAGATE
from plenum.common.messages.node_messages import MessageReq, MessageRep
from plenum.common.metrics_collector import measure_time, MetricsName, NullMetricsCollector
from plenum.common.types import f
from stp_core.common.log import getlogger
from plenum.server.message_handlers import LedgerStatusHandler, ConsistencyProofHandler, PropagateHandler

logger = getlogger()


class MessageReqProcessor:
    # This is a mixin, it's mixed with node.
    def __init__(self, metrics=NullMetricsCollector):
        self.metrics = metrics
        self.handlers = {
            LEDGER_STATUS: LedgerStatusHandler(self),
            CONSISTENCY_PROOF: ConsistencyProofHandler(self),
            PROPAGATE: PropagateHandler(self)
        }

    @measure_time(MetricsName.PROCESS_MESSAGE_REQ_TIME)
    def process_message_req(self, msg: MessageReq, frm):
        # Assumes a shared memory architecture. In case of multiprocessing,
        # RPC architecture, use deques to communicate the message and node will
        # maintain a unique internal message id to correlate responses.
        msg_type = msg.msg_type
        handler = self.handlers[msg_type]
        resp = handler.serve(msg)

        if not resp:
            return

        with self.metrics.measure_time(MetricsName.SEND_MESSAGE_REP_TIME):
            self.sendToNodes(MessageRep(**{
                f.MSG_TYPE.nm: msg_type,
                f.PARAMS.nm: msg.params,
                f.MSG.nm: resp
            }), names=[frm, ])

    @measure_time(MetricsName.PROCESS_MESSAGE_REP_TIME)
    def process_message_rep(self, msg: MessageRep, frm):
        msg_type = msg.msg_type
        if msg.msg is None:
            logger.debug('{} got null response for requested {} from {}'.
                         format(self, msg_type, frm))
            return
        handler = self.handlers[msg_type]
        handler.process(msg, frm)

    @measure_time(MetricsName.SEND_MESSAGE_REQ_TIME)
    def request_msg(self, typ, params: Dict, frm: List[str] = None):
        self.sendToNodes(MessageReq(**{
            f.MSG_TYPE.nm: typ,
            f.PARAMS.nm: params
        }), names=frm)
