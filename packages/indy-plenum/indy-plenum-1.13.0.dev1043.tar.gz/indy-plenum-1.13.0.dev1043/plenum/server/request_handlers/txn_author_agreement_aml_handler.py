from typing import Optional

from common.serializers.serialization import pool_state_serializer, config_state_serializer
from plenum.common.constants import CONFIG_LEDGER_ID, TXN_AUTHOR_AGREEMENT_AML, AML, AML_VERSION
from plenum.common.exceptions import InvalidClientRequest
from plenum.common.request import Request
from plenum.common.txn_util import get_payload_data, get_seq_no, get_txn_time
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_handlers.handler_interfaces.write_request_handler import WriteRequestHandler
from plenum.server.request_handlers.static_taa_helper import StaticTAAHelper
from plenum.server.request_handlers.utils import encode_state_value


class TxnAuthorAgreementAmlHandler(WriteRequestHandler):
    state_serializer = pool_state_serializer

    def __init__(self, database_manager: DatabaseManager):
        super().__init__(database_manager, TXN_AUTHOR_AGREEMENT_AML, CONFIG_LEDGER_ID)

    def static_validation(self, request: Request):
        operation, identifier, req_id = request.operation, request.identifier, request.reqId
        if len(operation[AML]) == 0:
            raise InvalidClientRequest(identifier, req_id,
                                       "TXN_AUTHOR_AGREEMENT_AML request "
                                       "must contain at least one acceptance mechanism")

    def additional_dynamic_validation(self, request: Request, req_pp_time: Optional[int]):
        operation, identifier, req_id = request.operation, request.identifier, request.reqId
        version = operation.get(AML_VERSION)
        if StaticTAAHelper.get_taa_aml_data(self.state, version, isCommitted=False) is not None:
            raise InvalidClientRequest(identifier, req_id,
                                       "Version of TAA AML must be unique and it cannot be modified")

    def update_state(self, txn, prev_result, request, is_committed=False):
        self._validate_txn_type(txn)
        payload = get_payload_data(txn)
        seq_no = get_seq_no(txn)
        txn_time = get_txn_time(txn)
        self._update_txn_author_agreement_acceptance_mechanisms(payload, seq_no, txn_time)

    def _update_txn_author_agreement_acceptance_mechanisms(self, payload, seq_no, txn_time):
        serialized_data = encode_state_value(payload, seq_no, txn_time, serializer=config_state_serializer)
        version = payload[AML_VERSION]
        self.state.set(StaticTAAHelper.state_path_taa_aml_latest(), serialized_data)
        self.state.set(StaticTAAHelper.state_path_taa_aml_version(version), serialized_data)

    def authorize(self, request):
        StaticTAAHelper.authorize(self.database_manager, request)
