from typing import Optional

import pytest
import time

from plenum.server.batch_handlers.three_pc_batch import ThreePcBatch
from plenum.server.request_handlers.handler_interfaces.write_request_handler import WriteRequestHandler
from plenum.test.testing_utils import FakeSomething

from plenum.common.txn_util import reqToTxn

from common.exceptions import LogicError

from plenum.common.request import Request
from plenum.common.util import randomString
from plenum.common.constants import TARGET_NYM, NODE, DOMAIN_LEDGER_ID, TXN_PAYLOAD, TXN_PAYLOAD_TYPE, \
    TXN_METADATA_TIME, TXN_METADATA, TXN_TYPE, CURRENT_TXN_PAYLOAD_VERSIONS, TXN_VERSION

from plenum.server.batch_handlers.domain_batch_handler import DomainBatchHandler
from plenum.server.request_handlers.node_handler import NodeHandler
from plenum.server.database_manager import DatabaseManager
from plenum.server.request_managers.write_request_manager import WriteRequestManager
from unittest.mock import Mock, call


@pytest.fixture(scope='function')
def db():
    return DatabaseManager()


@pytest.fixture(scope='function')
def write_req_manager(db):
    manager = WriteRequestManager(db)

    write_req_handler = NodeHandler(db, None)
    batch_req_handler = DomainBatchHandler(db)

    manager.register_req_handler(write_req_handler)
    manager.register_batch_handler(batch_req_handler)

    # We do not need to check request handler workability
    handler = manager.request_handlers[NODE][0]
    handler.static_validation = lambda request: 1
    handler.dynamic_validation = lambda request, req_pp_time: 1
    handler.update_state = lambda txn, updated_state, request, is_committed: 1
    handler.apply_request = lambda request, batch_ts, prev_result: (1, 1, 1)
    handler.apply_forced_request = lambda request: 1
    handler.transform_txn_for_ledger = lambda txn: 1

    # Same for batches
    handler = manager.batch_handlers[DOMAIN_LEDGER_ID][0]
    handler.post_batch_applied = lambda batch, prev_handler_result: 1
    handler.commit_batch = lambda batch, prev_handler_result=None: 1
    handler.post_batch_rejected = lambda ledger_id, prev_handler_result: 1

    return manager


@pytest.fixture(scope='function')
def node_req():
    return Request(identifier=randomString(),
                   reqId=5,
                   operation={'type': NODE,
                              'dest': randomString(),
                              TARGET_NYM: randomString(),
                              'data': {}
                              }
                   )


@pytest.fixture(scope='function')
def three_pc_batch():
    return ThreePcBatch(DOMAIN_LEDGER_ID, 0, 0, 1, time.time(),
                        randomString(),
                        randomString(),
                        ['d1', 'd2', 'd3'],
                        'pp_digest',
                        primaries=['a', 'b', 'c'])


def test_write_request_manager_fails_to_handle(write_req_manager: WriteRequestManager,
                                               node_req):
    node_req.operation['type'] = 999

    with pytest.raises(LogicError):
        write_req_manager.static_validation(node_req)

    with pytest.raises(LogicError):
        write_req_manager.dynamic_validation(node_req, 0)

    with pytest.raises(LogicError):
        write_req_manager.update_state(reqToTxn(node_req))

    with pytest.raises(LogicError):
        write_req_manager.apply_request(node_req, None)

    with pytest.raises(LogicError):
        write_req_manager.apply_forced_request(node_req)

    with pytest.raises(LogicError):
        write_req_manager.transform_txn_for_ledger(reqToTxn(node_req))


def test_write_request_manager_handles_request(write_req_manager: WriteRequestManager,
                                               node_req):
    write_req_manager.static_validation(node_req)
    write_req_manager.dynamic_validation(node_req, 0)
    write_req_manager.update_state(reqToTxn(node_req))
    write_req_manager.apply_request(node_req, None)
    write_req_manager.apply_forced_request(node_req)
    write_req_manager.transform_txn_for_ledger(reqToTxn(node_req))


def test_write_request_manager_chain_of_responsib_apply(write_req_manager: WriteRequestManager,
                                                        node_req, db):
    write_req_manager.request_handlers[NODE] = []
    handlers = write_req_manager.request_handlers[NODE]
    check_list = [FakeSomething(), FakeSomething(), FakeSomething()]
    node_req.check_list = check_list
    for check in check_list:
        check.check_field = False

    def modify_check_list(request, batch_ts, prev_result):
        assert not all(check.check_field for check in check_list)
        f_check = next(check for check in request.check_list if check.check_field is False)
        f_check.check_field = True
        return 1, 1, 1

    for i in range(3):
        handler = NodeHandler(db, None)
        handler.apply_request = modify_check_list
        handlers.append(handler)

    write_req_manager.apply_request(node_req, 0)

    assert all(check.check_field for check in check_list)


def test_write_request_manager_fails_to_handle_batches(write_req_manager: WriteRequestManager,
                                                       three_pc_batch):
    nonexistent_lid = 999
    three_pc_batch.ledger_id = nonexistent_lid

    with pytest.raises(LogicError):
        write_req_manager.post_apply_batch(three_pc_batch)

    with pytest.raises(LogicError):
        write_req_manager.post_batch_rejected(three_pc_batch)

    with pytest.raises(LogicError):
        write_req_manager.commit_batch(three_pc_batch)


def test_write_request_manager_handles_batches(write_req_manager: WriteRequestManager,
                                               three_pc_batch):
    write_req_manager.post_apply_batch(three_pc_batch)
    write_req_manager.commit_batch(three_pc_batch)
    write_req_manager.post_batch_rejected(three_pc_batch.ledger_id)


def test_write_request_manager_chain_of_responsib_batch(write_req_manager: WriteRequestManager,
                                                        three_pc_batch, db):
    write_req_manager.batch_handlers[DOMAIN_LEDGER_ID] = []
    handlers = write_req_manager.batch_handlers[DOMAIN_LEDGER_ID]

    check_list = [FakeSomething(), FakeSomething(), FakeSomething()]

    def modify_check_list():
        assert not all(check.check_field for check in check_list)
        f_check = next(check for check in check_list if check.check_field is False)
        f_check.check_field = True

    def modify_check_list_post_apply(batch, prev_result):
        modify_check_list()
        return 1, 1, 1

    def modify_check_list_commit(batch, prev_handler_result=None):
        modify_check_list()
        return 1, 1, 1

    def modify_check_list_post_rejected(lid, prev_result):
        modify_check_list()
        return 1, 1, 1

    for i in range(3):
        handler = DomainBatchHandler(db)
        handler.post_batch_applied = modify_check_list_post_apply
        handler.commit_batch = modify_check_list_commit
        handler.post_batch_rejected = modify_check_list_post_rejected
        handlers.append(handler)

    for check in check_list:
        check.check_field = False
    write_req_manager.post_apply_batch(three_pc_batch)
    assert all(check.check_field for check in check_list)

    for check in check_list:
        check.check_field = False
    write_req_manager.commit_batch(three_pc_batch)
    assert all(check.check_field for check in check_list)

    for check in check_list:
        check.check_field = False
    write_req_manager.post_batch_rejected(three_pc_batch.ledger_id)
    assert all(check.check_field for check in check_list)


def test_write_request_manager_restore_state(write_req_manager: WriteRequestManager,
                                             three_pc_batch, db):
    txn_type = "TXN_TYPE"
    ledger_id = 1

    class MockHandler(WriteRequestHandler):
        def __init__(self):
            super().__init__(db, txn_type, ledger_id)
            self.last_update_state_call = None

        def static_validation(self, request: Request):
            pass

        def additional_dynamic_validation(self, request: Request, req_pp_time: Optional[int]):
            pass

        def update_state(self, txn, prev_result, request, is_committed=False):
            self.last_update_state_call = txn, prev_result, request, is_committed

    handler_current = MockHandler()
    handler_prev_version = MockHandler()
    version = "version1"
    txn = {TXN_PAYLOAD: {TXN_PAYLOAD_TYPE: txn_type,
                         TXN_VERSION: CURRENT_TXN_PAYLOAD_VERSIONS[txn_type]},
           TXN_METADATA: {TXN_METADATA_TIME: 0}}
    write_req_manager.register_req_handler(handler_current)
    write_req_manager.register_req_handler_with_version(handler_prev_version, version)

    write_req_manager.restore_state(txn, ledger_id)
    assert handler_current.last_update_state_call == (txn, None, None, True)
    assert handler_prev_version.last_update_state_call is None

    handler_current.last_update_state_call = None
    db.set_txn_version_controller(FakeSomething(get_pool_version=lambda a: version,
                                                update_version=lambda a: None))

    write_req_manager.restore_state(txn, ledger_id)
    assert handler_current.last_update_state_call is None
    assert handler_prev_version.last_update_state_call == (txn, None, None, True)
