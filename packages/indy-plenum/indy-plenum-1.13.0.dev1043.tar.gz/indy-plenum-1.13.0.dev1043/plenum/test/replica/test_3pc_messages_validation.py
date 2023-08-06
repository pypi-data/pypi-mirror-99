import pytest

from plenum.common.config_helper import PNodeConfigHelper
from plenum.common.startable import Mode
from plenum.server.replica_validator_enums import INCORRECT_PP_SEQ_NO, OLD_VIEW, ALREADY_ORDERED, STASH_WATERMARKS, \
    STASH_CATCH_UP, STASH_VIEW_3PC
from plenum.test.helper import checkDiscardMsg, generate_state_root, create_prepare
from plenum.test.test_node import TestNode
from plenum.test.testing_utils import FakeSomething


@pytest.fixture(scope='function')
def test_node(
        tdirWithPoolTxns,
        tdirWithDomainTxns,
        poolTxnNodeNames,
        tdirWithNodeKeepInited,
        tdir,
        tconf,
        allPluginsPath):

    node_name = poolTxnNodeNames[0]
    config_helper = PNodeConfigHelper(node_name, tconf, chroot=tdir)
    node = TestNode(
        node_name,
        config_helper=config_helper,
        config=tconf,
        pluginPaths=allPluginsPath)
    view_no = 1
    node.view_changer = FakeSomething(view_no=view_no,
                                      view_change_in_progress=False)
    for r in node.replicas.values():
        r._consensus_data.view_no = view_no
    node.mode = Mode.participating
    yield node
    node.onStopping() # TODO stop won't call onStopping as we are in Stopped state


def test_discard_process_three_phase_msg(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    view_no = test_node.viewNo
    pp_seq_no = 0  # should start with 1
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    checkDiscardMsg([replica.stasher, ], msg, INCORRECT_PP_SEQ_NO)


def test_discard_process_three_phase_msg_for_old_view(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    view_no = test_node.viewNo - 1
    pp_seq_no = replica.last_ordered_3pc[1] + 1
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    checkDiscardMsg([replica.stasher, ], msg, OLD_VIEW)


def test_discard_process_three_phase_already_ordered_msg(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    replica.last_ordered_3pc = (test_node.viewNo, 100)
    replica._checkpointer.update_watermark_from_3pc()
    view_no = test_node.viewNo
    pp_seq_no = replica.h
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    checkDiscardMsg([replica.stasher, ], msg, ALREADY_ORDERED)


def test_process_three_phase_msg_with_catchup_stash(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    old_catchup_stashed_msgs = replica.stasher.stash_size(STASH_CATCH_UP)
    test_node.mode = Mode.syncing  # catchup in process
    view_no = test_node.viewNo
    pp_seq_no = replica.last_ordered_3pc[1] + 1
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    assert old_catchup_stashed_msgs + 1 == replica.stasher.stash_size(STASH_CATCH_UP)


def test_process_three_phase_msg_and_stashed_future_view(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    old_stashed_future_view_msgs = replica.stasher.stash_size(STASH_VIEW_3PC)
    view_no = test_node.viewNo + 1
    pp_seq_no = replica.last_ordered_3pc[1] + 1
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    assert old_stashed_future_view_msgs + 1 == replica.stasher.stash_size(STASH_VIEW_3PC)


def test_process_three_phase_msg_and_stashed_for_next_checkpoint(test_node, looper):
    sender = "NodeSender"
    inst_id = 0
    replica = test_node.replicas[inst_id]
    old_stashed_watermarks_msgs = replica.stasher.stash_size(STASH_WATERMARKS)
    view_no = test_node.viewNo
    pp_seq_no = replica.H + 1
    msg = create_prepare((view_no, pp_seq_no), generate_state_root(), inst_id)
    replica._external_bus.process_incoming(msg, sender)
    assert old_stashed_watermarks_msgs + 1 == replica.stasher.stash_size(STASH_WATERMARKS)
