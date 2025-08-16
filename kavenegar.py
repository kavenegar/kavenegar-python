"""Kavenegar REST API – Professional Single-File Python Client

This module is a production-ready, single-file client for the Kavenegar REST API
(https://kavenegar.com/rest.html). It is organized, typed, documented, and
includes pragmatic conveniences such as connection reuse, uniform error
handling, safe API-key masking, and parameter normalization for list/tuple/dict
values that Kavenegar expects as JSON-encoded strings in form data.

Main areas:
- SMS      : send, status, inbox/outbox queries, cancel, counts, etc.
- Verify   : template lookups (OTP), convenience builders.
- Call     : TTS calls, status, outbound/inbound, playback.
- Account  : info, config, (optional) usage & transactions.
- Utils    : bulk helpers, webhook parsing, health check, API key rotation.

Keep or remove optional endpoints based on your account plan.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union

import requests

try:
    import json
except ImportError:  # pragma: no cover
    import simplejson as json  # type: ignore


# =============================
# Constants / Types
# =============================
DEFAULT_TIMEOUT: int = 10

JsonScalar = Union[str, int, float, bool, None]
JsonLike = Union[JsonScalar, Mapping[str, Any], Sequence[Any]]
Params = MutableMapping[str, Union[str, int, float, bool]]


# =============================
# Exceptions
# =============================
class APIException(Exception):
    """Raised when the Kavenegar API returns a non-200 status code."""

    def __init__(self, status: Union[int, str], message: str, *, payload: Optional[Mapping[str, Any]] = None) -> None:
        super().__init__(f"APIException[{status}] {message}")
        self.status = status
        self.message = message
        self.payload = payload or {}


class HTTPException(Exception):
    """Raised for HTTP/network/parsing errors before API handling."""


# =============================
# Client
# =============================
class KavenegarAPI:
    """Kavenegar REST client.

    Docs: https://kavenegar.com/rest.html
    """

    version: str = "v1"
    host: str = "api.kavenegar.com"
    headers: Mapping[str, str] = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "utf-8",
    }

    # -------- Lifecycle --------
    def __init__(
        self,
        apikey: str,
        *,
        timeout: Optional[int] = None,
        proxies: Optional[Mapping[str, str]] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.apikey: str = apikey
        self.apikey_mask: str = self._mask(apikey)
        self.timeout: int = timeout or DEFAULT_TIMEOUT
        self.proxies: Optional[Mapping[str, str]] = proxies
        self._session: requests.Session = session or requests.Session()

    # -------- Magic methods --------
    def __repr__(self) -> str:  # pragma: no cover
        return f"kavenegar.KavenegarAPI({self.apikey_mask!r})"

    def __str__(self) -> str:  # pragma: no cover
        return f"kavenegar.KavenegarAPI({self.apikey_mask})"

    # -------- Private helpers --------
    @staticmethod
    def _mask(key: str) -> str:
        return f"{key[:2]}********{key[-2:]}" if len(key) >= 4 else "********"

    def _build_url(self, action: str, method: str) -> str:
        return f"https://{self.host}/{self.version}/{self.apikey}/{action}/{method}.json"

    @staticmethod
    def _jsonify_params(params: Mapping[str, Any]) -> Params:
        """Convert list/tuple/dict params to JSON strings (Kavenegar quirk)."""
        out: Dict[str, Union[str, int, float, bool]] = {}
        for key, value in params.items():
            if isinstance(value, (dict, list, tuple)):
                out[key] = json.dumps(value)  # type: ignore[assignment]
            else:
                out[key] = value  # type: ignore[assignment]
        return out

    def _post(self, action: str, method: str, params: Optional[Mapping[str, Any]] = None) -> Any:
        url = self._build_url(action, method)
        data = self._jsonify_params(params or {})
        try:
            resp = self._session.post(
                url,
                headers=self.headers,
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,  # type: ignore[arg-type]
            )
            content = resp.content
            try:
                payload = json.loads(content.decode("utf-8"))
            except Exception as e:  # JSON decode or Unicode error
                raise HTTPException(str(e))

            meta = payload.get("return", {})
            status = meta.get("status")
            message = meta.get("message", "")
            if status == 200:
                return payload.get("entries")
            raise APIException(status, message, payload=payload)
        except requests.exceptions.RequestException as e:
            redacted = str(e).replace(self.apikey, self.apikey_mask)
            raise HTTPException(redacted)

    # -------- Config utilities --------
    def mask_apikey(self) -> str:
        return self.apikey_mask

    def set_timeout(self, timeout: int) -> None:
        self.timeout = timeout

    def set_proxies(self, proxies: Optional[Mapping[str, str]]) -> None:
        self.proxies = proxies

    def rotate_api_key(self, new_key: str) -> None:
        self.apikey = new_key
        self.apikey_mask = self._mask(new_key)

    # -------- SMS APIs --------
    def sms_send(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "send", params)

    def sms_sendarray(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "sendarray", params)

    def sms_status(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "status", params)

    def sms_statuslocalmessageid(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "statuslocalmessageid", params)

    def sms_select(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "select", params)

    def sms_selectoutbox(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "selectoutbox", params)

    def sms_latestoutbox(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "latestoutbox", params)

    def sms_countoutbox(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "countoutbox", params)

    def sms_cancel(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "cancel", params)

    def sms_receive(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "receive", params)

    def sms_countinbox(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "countinbox", params)

    def sms_countpostalcode(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "countpostalcode", params)

    def sms_sendbypostalcode(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "sendbypostalcode", params)

    def sms_selectinbox(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "selectinbox", params)

    def sms_archive(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "archive", params)

    # Optional/extended (plan dependent)
    def sms_blacklist(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "blacklist", params)

    def sms_unsubscribe(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("sms", "unsubscribe", params)

    # -------- Verify APIs --------
    def verify_lookup(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("verify", "lookup", params)

    def verify_lookup_with_templated(
        self,
        template: str,
        receptor: str,
        token: str,
        token2: Optional[str] = None,
        token3: Optional[str] = None,
        type_: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {"receptor": receptor, "token": token, "template": template}
        if token2:
            params["token2"] = token2
        if token3:
            params["token3"] = token3
        if type_:
            params["type"] = type_
        return self.verify_lookup(params)

    def verify_lookup_advanced(self, template: str, receptor: str, tokens: Mapping[str, Any]) -> Any:
        params: Dict[str, Any] = {"receptor": receptor, "template": template}
        params.update(tokens)
        return self.verify_lookup(params)

    # Optional/extended (plan dependent)
    def verify_voicecall(self, receptor: str, token: str, template: str) -> Any:
        return self._post("verify", "voicecall", {"receptor": receptor, "token": token, "template": template})

    def verify_call_otp(self, receptor: str, token: str) -> Any:
        return self._post("verify", "callotp", {"receptor": receptor, "token": token})

    # -------- Call APIs --------
    def call_maketts(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "maketts", params)

    def call_status(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "status", params)

    def call_outbound(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "outbound", params)

    def call_cancel(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "cancel", params)

    def call_inbound(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "inbound", params)

    def call_play(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "play", params)

    # Optional/extended (plan dependent)
    def call_transfer(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "transfer", params)

    def call_record(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("call", "record", params)

    # -------- Account APIs --------
    def account_info(self) -> Any:
        return self._post("account", "info")

    def account_config(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("account", "config", params)

    def account_balance(self) -> Optional[Union[int, float, str]]:
        info = self.account_info()
        if isinstance(info, list) and info:
            return info[0].get("remaincredit")
        return None

    # Optional/extended (plan dependent)
    def account_usage(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("account", "usage", params)

    def account_transactions(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("account", "transactions", params)

    def account_webhooks(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("account", "webhooks", params)

    def account_blocked(self, params: Optional[Mapping[str, Any]] = None) -> Any:
        return self._post("account", "blocked", params)

    # -------- Utilities / Helpers --------
    @staticmethod
    def _chunk(seq: Sequence[str], size: int) -> List[List[str]]:
        return [list(seq[i : i + size]) for i in range(0, len(seq), size)]

    def send_bulk_sms(
        self,
        receptors: Sequence[str],
        message: str,
        *,
        sender: Optional[str] = None,
    ) -> Any:
        params: Dict[str, Any] = {"receptor": receptors, "message": message}
        if sender:
            params["sender"] = sender
        return self.sms_send(params)

    def send_bulk_sms_chunked(
        self,
        receptors: Sequence[str],
        message: str,
        *,
        sender: Optional[str] = None,
        chunk_size: int = 200,
    ) -> List[Any]:
        """Send to many receptors in chunks to avoid payload limits."""
        results: List[Any] = []
        for group in self._chunk(list(receptors), max(1, int(chunk_size))):
            results.append(self.send_bulk_sms(group, message, sender=sender))
        return results

    def check_sms_delivery(self, messageid: Union[str, int, Sequence[Union[str, int]]]) -> Any:
        return self.sms_status({"messageid": messageid})

    def parse_webhook(self, payload: Union[str, Mapping[str, Any]]) -> Mapping[str, Any]:
        """Parse JSON webhook payloads (inbound SMS / DLR)."""
        if isinstance(payload, str):
            try:
                return json.loads(payload)
            except Exception as e:
                raise HTTPException(str(e))
        return dict(payload)

    def healthcheck(self) -> Mapping[str, bool]:
        try:
            _ = self.account_info()
            ok_account = True
        except Exception:
            ok_account = False
        try:
            _ = self.sms_latestoutbox()
            ok_sms = True
        except Exception:
            ok_sms = False
        return {"account": ok_account, "sms": ok_sms}


__all__ = [
    "KavenegarAPI",
    "APIException",
    "HTTPException",
    "DEFAULT_TIMEOUT",
]
