from plenum.server.node import Node
from plenum.test.delayers import cDelay, pDelay, ppDelay
from plenum.test.helper import sdk_send_random_and_check, \
    sdk_send_random_requests, sdk_get_replies, sdk_check_reply
from plenum.test.node_catchup.helper import ensure_all_nodes_have_same_data
from plenum.test.stasher import delay_rules
from plenum.test.test_node import ensureElectionsDone, getPrimaryReplica, check_not_in_view_change
from plenum.test.view_change.helper import ensure_view_change
from stp_core.loop.eventually import eventually


def test_no_propagate_request_on_different_last_ordered_on_backup_before_vc(looper, txnPoolNodeSet,
                                                                            sdk_pool_handle, sdk_wallet_client):
    '''
    1. Send random request
    2. Make 3 node on backup instance slow in getting commits
    3. Send random request
    4. do view change
    5. reset delays
    => we expect that all nodes and all instances have the same last ordered
    '''
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)
    slow_instance = 1
    slow_nodes = txnPoolNodeSet[1:4]
    fast_nodes = [n for n in txnPoolNodeSet if n not in slow_nodes]
    nodes_stashers = [n.nodeIbStasher for n in slow_nodes]
    last_view_no = txnPoolNodeSet[0].viewNo
    master_pp_seq_no = txnPoolNodeSet[0].master_replica.last_ordered_3pc[1]
    backup_last_pp_seq_no = txnPoolNodeSet[0].replicas[slow_instance].last_ordered_3pc[1]
    with delay_rules(nodes_stashers, cDelay(instId=slow_instance)):
        # send one request
        sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                                  sdk_wallet_client, 1)
        master_pp_seq_no += 1
        looper.run(
            eventually(check_last_ordered,
                       fast_nodes,
                       slow_instance,
                       (last_view_no, backup_last_pp_seq_no + 1)))
        check_last_ordered(slow_nodes, slow_instance, (last_view_no, backup_last_pp_seq_no))

        # trigger view change on all nodes
        ensure_view_change(looper, txnPoolNodeSet)
        # wait for view change done on all nodes
        ensureElectionsDone(looper, txnPoolNodeSet)
        master_pp_seq_no += 1

    primary = getPrimaryReplica(txnPoolNodeSet, slow_instance).node
    non_primaries = [n for n in txnPoolNodeSet if n is not primary]

    # Backup primary replica set new_view and seq_no == 1, because of primary batch
    looper.run(eventually(check_last_ordered, non_primaries,
                          slow_instance,
                          (last_view_no + 1, 2)))

    looper.run(eventually(check_last_ordered, [primary],
                          slow_instance,
                          (last_view_no + 1, 2)))

    looper.run(eventually(check_last_ordered, txnPoolNodeSet,
                          txnPoolNodeSet[0].master_replica.instId,
                          (last_view_no + 1, master_pp_seq_no)))

    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)
    master_pp_seq_no += 1
    assert all(0 == node.spylog.count(node.request_propagates)
               for node in txnPoolNodeSet)


def test_no_propagate_request_on_different_prepares_on_backup_before_vc(looper, txnPoolNodeSet,
                                                                        sdk_pool_handle, sdk_wallet_client):
    '''
    1. Send random request
    2. Make 3 node on backup instance slow in getting prepares
    3. Send random request
    4. do view change
    5. reset delays
    => we expect that all nodes and all instances have the same last ordered
    '''
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)
    slow_instance = 1
    slow_nodes = txnPoolNodeSet[1:3]
    fast_nodes = [n for n in txnPoolNodeSet if n not in slow_nodes]
    nodes_stashers = [n.nodeIbStasher for n in slow_nodes]
    last_view_no = txnPoolNodeSet[0].viewNo
    master_pp_seq_no = txnPoolNodeSet[0].master_replica.last_ordered_3pc[1]
    backup_last_pp_seq_no = txnPoolNodeSet[0].replicas[slow_instance].last_ordered_3pc[1]
    with delay_rules(nodes_stashers, pDelay(instId=slow_instance)):
        with delay_rules(nodes_stashers, ppDelay(instId=slow_instance)):
            # send one request
            sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                                      sdk_wallet_client, 1)
            master_pp_seq_no += 1
            looper.run(
                eventually(is_prepared,
                           fast_nodes,
                           backup_last_pp_seq_no + 1,
                           slow_instance))

            # trigger view change on all nodes
            ensure_view_change(looper, txnPoolNodeSet)
            # wait for view change done on all nodes
            ensureElectionsDone(looper, txnPoolNodeSet)
            master_pp_seq_no += 1

    primary = getPrimaryReplica(txnPoolNodeSet, slow_instance).node
    non_primaries = [n for n in txnPoolNodeSet if n is not primary]

    looper.run(eventually(check_last_ordered, non_primaries,
                          slow_instance,
                          (last_view_no + 1, 2)))

    looper.run(eventually(check_last_ordered, [primary],
                          slow_instance,
                          (last_view_no + 1, 2)))

    # 2 batches will be reordered after view_change and another one is from primaries batch
    looper.run(eventually(check_last_ordered, txnPoolNodeSet,
                          txnPoolNodeSet[0].master_replica.instId,
                          (last_view_no + 1, master_pp_seq_no)))

    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)
    master_pp_seq_no += 1
    looper.run(
        eventually(check_last_ordered,
                   txnPoolNodeSet,
                   slow_instance,
                   (txnPoolNodeSet[0].viewNo, 3)))
    assert all(0 == node.spylog.count(node.request_propagates)
               for node in txnPoolNodeSet)


def test_no_propagate_request_on_different_last_ordered_on_master_before_vc(looper, txnPoolNodeSet,
                                                                            sdk_pool_handle, sdk_wallet_client):
    ''' Send random request and do view change then fast_nodes (1, 4 - without
    primary after next view change) are already ordered transaction on master
    and slow_nodes are not. Check ordering on slow_nodes.'''
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, 1)
    master_instance = txnPoolNodeSet[0].master_replica.instId
    slow_nodes = txnPoolNodeSet[1:3]
    fast_nodes = [n for n in txnPoolNodeSet if n not in slow_nodes]
    nodes_stashers = [n.nodeIbStasher for n in slow_nodes]
    old_last_ordered = txnPoolNodeSet[0].master_replica.last_ordered_3pc
    batches_count = old_last_ordered[1]
    with delay_rules(nodes_stashers, cDelay()):
        # send one request
        requests = sdk_send_random_requests(looper, sdk_pool_handle,
                                            sdk_wallet_client, 1)
        batches_count += 1
        last_ordered_for_slow = slow_nodes[0].master_replica.last_ordered_3pc
        old_view_no = txnPoolNodeSet[0].viewNo
        looper.run(
            eventually(check_last_ordered,
                       fast_nodes,
                       master_instance,
                       (old_view_no, batches_count)))

        # trigger view change on all nodes
        ensure_view_change(looper, txnPoolNodeSet)
        looper.run(eventually(check_not_in_view_change, txnPoolNodeSet))
    # wait for view change done on all nodes
    ensureElectionsDone(looper, txnPoolNodeSet, customTimeout=60)

    batches_count += 1

    replies = sdk_get_replies(looper, requests)
    for reply in replies:
        sdk_check_reply(reply)

    # a new primary will send a PrePrepare for the new view
    looper.run(eventually(check_last_ordered, txnPoolNodeSet,
                          master_instance,
                          (old_view_no + 1, batches_count)))
    ensure_all_nodes_have_same_data(looper, txnPoolNodeSet)
    assert all(0 == node.spylog.count(node.request_propagates)
               for node in txnPoolNodeSet)


def is_prepared(nodes: [Node], ppSeqNo, instId):
    for node in nodes:
        replica = node.replicas[instId]
        assert (node.viewNo, ppSeqNo) in replica._ordering_service.prepares or \
               (node.viewNo, ppSeqNo) in replica._ordering_service.sent_preprepares


def check_last_ordered(nodes: [Node],
                       instId,
                       last_ordered=None):
    if last_ordered is None:
        last_ordered = nodes[0].replicas[instId].last_ordered_3pc
    for node in nodes:
        assert node.replicas[instId].last_ordered_3pc == last_ordered, "Node {}, instance {}".format(node.name, instId)
