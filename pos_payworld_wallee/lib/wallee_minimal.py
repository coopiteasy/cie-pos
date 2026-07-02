# SPDX-FileCopyrightText: 2026 Vincent Haulotte
# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Minimal Wallee REST client embedded for Odoo deployments.

This is not a full copy of the official Wallee Python SDK. It implements only
what the POS terminal integration needs:
- create a transaction
- perform the transaction on a payment terminal by identifier

It follows the authentication pattern used by the official SDK: HS256 JWT signed
with the base64-decoded application user's authentication key.
"""
import base64
import hashlib
import hmac
import json
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

DEFAULT_HOST = "https://app-wallee.com/api/v2.0"
DEFAULT_TIMEOUT = 25
PERFORM_TRANSACTION_TIMEOUT = 90
USER_AGENT = "Odoo-pos-payworld-wallee/16.0"
MAX_ERROR_MESSAGE_LENGTH = 500


class WalleeApiError(Exception):
    """Raised when Wallee returns an HTTP/API error."""

    def __init__(self, message, status=None, body=None):
        super().__init__(message)
        self.status = status
        self.body = body


def _b64url(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _json_dumps(data):
    return json.dumps(data, separators=(",", ":"), ensure_ascii=False)


class WalleeMinimalClient(object):
    API_PATH = "/api/v2.0"

    def __init__(
        self,
        user_id,
        authentication_key,
        host=DEFAULT_HOST,
        timeout=DEFAULT_TIMEOUT,
    ):
        self.user_id = int(user_id)
        self.authentication_key = authentication_key
        self.host = (host or DEFAULT_HOST).rstrip("/")
        self.timeout = timeout

    def create_transaction(self, space_id, transaction_create, expand=None):
        return self._request(
            "POST",
            "/payment/transactions",
            space_id=space_id,
            body=transaction_create,
            query=self._expand_query(expand),
            timeout=self.timeout,
            expected=(200, 201),
        )

    def perform_transaction_by_identifier(
        self, space_id, identifier, transaction_id, language=None, expand=None
    ):
        query = [("transactionId", int(transaction_id))]
        if language:
            query.append(("language", language))
        query.extend(self._expand_query(expand))
        return self._request(
            "POST",
            "/payment/terminals/by-identifier/%s/perform-transaction"
            % quote(str(identifier), safe=""),
            space_id=space_id,
            query=query,
            timeout=PERFORM_TRANSACTION_TIMEOUT,
            expected=(200,),
        )

    def _expand_query(self, expand):
        if not expand:
            return []
        return [("expand", item) for item in expand]

    def _request(
        self,
        method,
        resource_path,
        space_id=None,
        query=None,
        body=None,
        timeout=None,
        expected=(200,),
    ):
        query = query or []
        query_string = urlencode(query, doseq=True)
        url = self.host + resource_path
        if query_string:
            url += "?" + query_string

        data = None
        headers = {
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
            "x-meta-sdk-version": "embedded-minimal",
            "x-meta-sdk-language": "python",
            "x-meta-sdk-provider": "wallee",
        }
        if space_id is not None:
            headers["Space"] = str(int(space_id))
        if body is not None:
            data = _json_dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"

        headers["Authorization"] = "Bearer %s" % self._jwt(url, method.upper())
        request = Request(url, data=data, headers=headers, method=method.upper())

        try:
            with urlopen(request, timeout=timeout or self.timeout) as response:
                raw = response.read().decode("utf-8")
                status = response.getcode()
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise WalleeApiError(
                "Wallee HTTP %s: %s" % (exc.code, raw[:MAX_ERROR_MESSAGE_LENGTH]),
                status=exc.code,
                body=raw,
            ) from exc
        except URLError as exc:
            raise WalleeApiError("Unable to reach Wallee: %s" % exc) from exc

        if status not in expected:
            raise WalleeApiError(
                "Unexpected Wallee HTTP %s: %s"
                % (status, raw[:MAX_ERROR_MESSAGE_LENGTH]),
                status=status,
                body=raw,
            )
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except ValueError:
            return {"raw": raw}

    def _jwt(self, full_url, method):
        # Official SDK signs requestPath = /api/v2.0 + path/query after host.
        relative = full_url.replace(self.host, "", 1)
        request_path = self.API_PATH + relative
        payload = {
            "sub": self.user_id,
            "iat": int(time.time()),
            "requestPath": request_path,
            "requestMethod": method,
        }
        header = {"alg": "HS256", "typ": "JWT", "ver": 1}
        signing_input = "%s.%s" % (
            _b64url(_json_dumps(header).encode("utf-8")),
            _b64url(_json_dumps(payload).encode("utf-8")),
        )
        secret = base64.b64decode(self.authentication_key)
        signature = hmac.new(
            secret, signing_input.encode("ascii"), hashlib.sha256
        ).digest()
        return "%s.%s" % (signing_input, _b64url(signature))
