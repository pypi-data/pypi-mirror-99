from plenum.test.test_node import get_master_primary_node, get_last_master_non_primary_node
from plenum.test.view_change.helper import view_change_in_between_3pc


def slow_nodes(node_set):
    return [get_master_primary_node(node_set),
            get_last_master_non_primary_node(node_set)]


def test_view_change_in_between_3pc_2_of_4_nodes_with_old_primary(
        txnPoolNodeSet, looper, sdk_pool_handle, sdk_wallet_client):
    """
    - Slow processing 3PC messages for 2 of 4 node (2>f)
    - Slow the current Primary node and the last non-primary node (it will not
     be the next primary because of round-robin).
    - do view change
    """
    view_change_in_between_3pc(looper, txnPoolNodeSet,
                               slow_nodes(txnPoolNodeSet),
                               sdk_pool_handle, sdk_wallet_client)


def test_view_change_in_between_3pc_2_of_4_nodes_with_old_primary_long_delay(
        txnPoolNodeSet, looper, sdk_pool_handle, sdk_wallet_client):
    """
    - Slow processing 3PC messages for 2 of 4 node (2>f)
    - Slow the current Primary node and the last non-primary node (it will not
     be the next primary because of round-robin).
    - do view change
    """
    view_change_in_between_3pc(looper, txnPoolNodeSet,
                               slow_nodes(txnPoolNodeSet),
                               sdk_pool_handle, sdk_wallet_client,
                               slow_delay=20)
