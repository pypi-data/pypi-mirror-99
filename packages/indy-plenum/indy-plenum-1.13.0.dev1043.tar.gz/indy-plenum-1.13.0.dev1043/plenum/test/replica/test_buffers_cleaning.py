from plenum.common.event_bus import InternalBus
from plenum.common.startable import Mode
from plenum.common.timer import QueueTimer
from plenum.common.util import get_utc_epoch
from plenum.server.consensus.primary_selector import RoundRobinConstantNodesPrimariesSelector
from plenum.server.database_manager import DatabaseManager
from plenum.server.quorums import Quorums
from plenum.server.replica import Replica
from plenum.test.testing_utils import FakeSomething


def test_ordered_cleaning(tconf):
    global_view_no = 2

    node = FakeSomething(
        name="fake node",
        ledger_ids=[0],
        viewNo=global_view_no,
        utc_epoch=get_utc_epoch,
        get_validators=lambda: [],
        db_manager=DatabaseManager(),
        requests=[],
        mode=Mode.participating,
        timer=QueueTimer(),
        quorums=Quorums(4),
        write_manager=None,
        poolManager=FakeSomething(node_names_ordered_by_rank=lambda: []),
        primaries_selector=RoundRobinConstantNodesPrimariesSelector(["Alpha", "Beta", "Gamma", "Delta"])
    )
    bls_bft_replica = FakeSomething(
        gc=lambda *args: None,
    )

    replica = Replica(node, instId=0, config=tconf, bls_bft_replica=bls_bft_replica)
    replica._consensus_data.view_no = global_view_no
    total = []

    num_requests_per_view = 3
    for viewNo in range(global_view_no + 1):
        for seqNo in range(num_requests_per_view):
            reqId = viewNo, seqNo
            replica._ordering_service._add_to_ordered(*reqId)
            total.append(reqId)

    # gc is called after stable checkpoint, since no request executed
    # in this test starting it manually
    replica._ordering_service.gc(100)
    # Requests with view lower then previous view
    # should not be in ordered
    assert len(replica._ordering_service.ordered) == len(total[num_requests_per_view:])


def test_primary_names_cleaning(tconf):
    node = FakeSomething(
        name="fake node",
        ledger_ids=[0],
        viewNo=0,
        utc_epoch=get_utc_epoch,
        get_validators=lambda: [],
        db_manager=DatabaseManager(),
        requests=[],
        mode=Mode.participating,
        timer=QueueTimer(),
        quorums=Quorums(4),
        write_manager=None,
        poolManager=FakeSomething(node_names_ordered_by_rank=lambda: []),
        primaries_selector=RoundRobinConstantNodesPrimariesSelector(["Alpha", "Beta", "Gamma", "Delta"])
    )
    bls_bft_replica = FakeSomething(
        gc=lambda *args: None,
    )

    replica = Replica(node, instId=0, config=tconf, bls_bft_replica=bls_bft_replica)

    replica.primaryName = "Node1:0"
    assert list(replica.primaryNames.items()) == \
           [(0, "Node1:0")]

    node.viewNo += 1
    replica._consensus_data.view_no = node.viewNo
    replica.primaryName = "Node2:0"
    assert list(replica.primaryNames.items()) == \
           [(0, "Node1:0"), (1, "Node2:0")]

    node.viewNo += 1
    replica._consensus_data.view_no = node.viewNo
    replica.primaryName = "Node3:0"
    assert list(replica.primaryNames.items()) == \
           [(1, "Node2:0"), (2, "Node3:0")]

    node.viewNo += 1
    replica._consensus_data.view_no = node.viewNo
    replica.primaryName = "Node4:0"
    assert list(replica.primaryNames.items()) == \
           [(2, "Node3:0"), (3, "Node4:0")]
