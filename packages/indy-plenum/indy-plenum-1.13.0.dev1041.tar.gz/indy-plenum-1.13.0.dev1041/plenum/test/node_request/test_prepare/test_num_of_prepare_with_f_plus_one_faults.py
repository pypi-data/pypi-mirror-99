from functools import partial

import pytest
from plenum.common.util import getNoInstances
from stp_core.common.util import adict
from plenum.test import waits

from plenum.test.malicious_behaviors_node import makeNodeFaulty, \
    delaysPrePrepareProcessing, \
    changesRequest
from plenum.test.node_request.node_request_helper import checkPrePrepared

nodeCount = 7
# f + 1 faults, i.e, num of faults greater than system can tolerate
faultyNodes = 3
whitelist = ['InvalidSignature',
             'cannot process incoming PREPARE']
delayPrePrepareSec = 60


@pytest.fixture(scope="module")
def setup(txnPoolNodeSet):
    # Making nodes faulty such that no primary is chosen
    E = txnPoolNodeSet[-3]
    G = txnPoolNodeSet[-2]
    Z = txnPoolNodeSet[-1]
    for node in E, G, Z:
        makeNodeFaulty(node,
                       changesRequest, partial(delaysPrePrepareProcessing,
                                               delay=delayPrePrepareSec))
    return adict(faulties=(E, G, Z))


@pytest.fixture(scope="module")
def afterElection(setup):
    for n in setup.faulties:
        for r in n.replicas.values():
            assert not r.isPrimary


@pytest.fixture(scope="module")
def preprepared1WithDelay(looper, txnPoolNodeSet, propagated1, faultyNodes):
    timeouts = waits.expectedPrePrepareTime(len(txnPoolNodeSet)) + delayPrePrepareSec
    checkPrePrepared(looper,
                     txnPoolNodeSet,
                     propagated1,
                     range(getNoInstances(len(txnPoolNodeSet))),
                     faultyNodes,
                     timeout=timeouts)


def testNumOfPrepareWithFPlusOneFaults(
        afterElection, noRetryReq, preprepared1WithDelay):
    pass
