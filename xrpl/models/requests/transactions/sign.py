"""
The sign method takes a transaction in JSON format and a seed value, and returns a
signed binary representation of the transaction. To contribute one signature to a
multi-signed transaction, use the sign_for method instead.

By default, this method is admin-only. It can be used as a public method if the server
has enabled public signing.

Caution:
Unless you run the rippled server yourself, you should do local signing with RippleAPI
instead of using this command. An untrustworthy server could change the transaction
before signing it, or use your secret key to sign additional arbitrary transactions as
if they came from you.

`See sign <https://xrpl.org/sign.html>`_
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from xrpl.models.requests.request import Request, RequestMethod
from xrpl.models.transactions.transaction import REQUIRED, Transaction
from xrpl.models.utils import require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True)
class Sign(Request):
    """
    The sign method takes a transaction in JSON format and a seed value, and returns a
    signed binary representation of the transaction. To contribute one signature to a
    multi-signed transaction, use the sign_for method instead.

    By default, this method is admin-only. It can be used as a public method if the
    server has enabled public signing.

    Caution:
    Unless you run the rippled server yourself, you should do local signing with
    RippleAPI instead of using this command. An untrustworthy server could change the
    transaction before signing it, or use your secret key to sign additional arbitrary
    transactions as if they came from you.

    `See sign <https://xrpl.org/sign.html>`_
    """

    method: RequestMethod = field(default=RequestMethod.SIGN, init=False)
    transaction: Transaction = REQUIRED
    secret: Optional[str] = None
    seed: Optional[str] = None
    seed_hex: Optional[str] = None
    passphrase: Optional[str] = None
    key_type: Optional[str] = None
    offline: bool = False
    build_path: Optional[bool] = None
    fee_mult_max: int = 10
    fee_div_max: int = 1

    def to_dict(self: Sign) -> Dict[str, Any]:
        """
        Returns the dictionary representation of a Sign.

        Returns:
            The dictionary representation of a Sign.
        """
        return_dict = super().to_dict()
        del return_dict["transaction"]
        return_dict["tx_json"] = self.transaction.to_dict()
        return return_dict

    def _get_errors(self: Sign) -> Dict[str, str]:
        errors = super()._get_errors()
        if not self._has_only_one_seed():
            errors[
                "Sign"
            ] = "Must have only one of `secret`, `seed`, `seed_hex`, and `passphrase."

        if self.secret is not None and self.key_type is not None:
            errors["key_type"] = "Must omit `key_type` if `secret` is provided."

        return errors

    def _has_only_one_seed(self: Sign) -> bool:
        present_items = [
            item
            for item in [self.secret, self.seed, self.seed_hex, self.passphrase]
            if item is not None
        ]
        return len(present_items) == 1