from plenum.test.test_node import get_master_primary_node, get_first_master_non_primary_node
from plenum.test.view_change.helper import view_change_in_between_3pc


def slow_nodes(node_set):
    return [get_master_primary_node(node_set),
            get_first_master_non_primary_node(node_set)]


def test_view_change_in_between_3pc_2_of_4_nodes_with_old_and_new_primary(
        txnPoolNodeSet, looper, sdk_pool_handle, sdk_wallet_client):
    """
    - Slow processing 3PC messages for 2 of 4 node (2>f)
    - Slow both current and next primaries
    - do view change
    """
    view_change_in_between_3pc(looper, txnPoolNodeSet,
                               slow_nodes(txnPoolNodeSet),
                               sdk_pool_handle, sdk_wallet_client)


def test_view_change_in_between_3pc_2_of_4_nodes_with_old_and_new_primary_long_delay(
        txnPoolNodeSet, looper, sdk_pool_handle, sdk_wallet_client):
    """
    - Slow processing 3PC messages for 2 of 4 node (2>f)
    - Slow both current and next primaries
    - do view change
    """
    view_change_in_between_3pc(looper, txnPoolNodeSet,
                               slow_nodes(txnPoolNodeSet),
                               sdk_pool_handle, sdk_wallet_client,
                               slow_delay=20)
