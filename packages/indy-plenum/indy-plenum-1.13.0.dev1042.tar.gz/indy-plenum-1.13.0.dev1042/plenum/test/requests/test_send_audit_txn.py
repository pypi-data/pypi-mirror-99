import json
import time
import pytest

from plenum.test.helper import sdk_get_and_check_replies
from plenum.test.pool_transactions.helper import sdk_sign_and_send_prepared_request

from plenum.common.exceptions import RequestNackedException
from plenum.common.constants import TXN_TYPE, AUDIT, CURRENT_PROTOCOL_VERSION
from plenum.common.types import OPERATION, f


def test_send_audit_txn(looper, sdk_wallet_client, sdk_pool_handle):
    req = {
        OPERATION: {
            TXN_TYPE: AUDIT,
            'data': 'data1'
        },
        f.IDENTIFIER.nm: sdk_wallet_client[1],
        f.REQ_ID.nm: int(time.time()),
        f.PROTOCOL_VERSION.nm: CURRENT_PROTOCOL_VERSION
    }

    rep = sdk_sign_and_send_prepared_request(looper, sdk_wallet_client, sdk_pool_handle, json.dumps(req))
    with pytest.raises(RequestNackedException) as e:
        sdk_get_and_check_replies(looper, [rep])
    e.match('External audit requests are not allowed')
