import types

import pytest

from stp_core.loop.eventually import eventually
from plenum.common.constants import DOMAIN_LEDGER_ID
from plenum.common.util import updateNamedTuple
from plenum.test.helper import sdk_send_random_requests, \
    sdk_send_random_and_check
from plenum.test.test_node import getNonPrimaryReplicas, \
    getPrimaryReplica


@pytest.fixture(scope="module")
def setup(tconf, looper, txnPoolNodeSet, sdk_pool_handle, sdk_wallet_client):
    # Patch the 3phase request sending method to send incorrect digest and
    pr, otherR = getPrimaryReplica(txnPoolNodeSet, instId=0), \
                 getNonPrimaryReplicas(txnPoolNodeSet, instId=0)

    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, tconf.Max3PCBatchSize)
    stateRoot = pr._ordering_service.get_state_root_hash(DOMAIN_LEDGER_ID, to_str=False)

    origMethod = pr._ordering_service.create_3pc_batch
    malignedOnce = None

    def badMethod(self, ledgerId):
        nonlocal malignedOnce
        pp = origMethod(ledgerId)
        if not malignedOnce:
            pp = updateNamedTuple(pp, digest=pp.digest + '123')
            malignedOnce = True
        return pp

    pr._ordering_service.create_3pc_batch = types.MethodType(badMethod, pr._ordering_service)
    sdk_send_random_requests(looper, sdk_pool_handle, sdk_wallet_client,
                             tconf.Max3PCBatchSize)
    return pr, otherR, stateRoot


@pytest.fixture(scope="module")
def reverted(setup, looper):
    pr, otherR, oldStateRoot = setup

    def chkStateRoot(root):
        for r in [pr] + otherR:
            r._ordering_service.get_state_root_hash(DOMAIN_LEDGER_ID, to_str=False) == root

    looper.run(eventually(chkStateRoot, oldStateRoot))


@pytest.fixture(scope="module")
def viewChanged(reverted, looper, txnPoolNodeSet):
    def chk():
        for n in txnPoolNodeSet:
            assert n.viewNo == 1
            assert all([r.primaryName for r in n.replicas.values()])

    looper.run(eventually(chk, retryWait=1, timeout=15))


def testTreeStateRevertedAfterBatchRejection(reverted):
    """"
    After a batch is rejected, all nodes revert their trees to last known
    correct state
    """


def testViewChangeAfterBatchRejected(viewChanged):
    """"
    After a batch is rejected and each batch that was created based on the
    rejected batch is discarded, the discarded batches are tried again
    """


def testMoreBatchesWillBeSentAfterViewChange(reverted, viewChanged,
                                             txnPoolNodeSet,
                                             sdk_pool_handle, sdk_wallet_client,
                                             tconf, looper):
    """
    After retrying discarded batches, new batches are sent
    :return:
    """
    sdk_send_random_and_check(looper, txnPoolNodeSet, sdk_pool_handle,
                              sdk_wallet_client, tconf.Max3PCBatchSize)
