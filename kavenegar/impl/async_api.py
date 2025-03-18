from typing import Optional, Any, Dict

import aiohttp
from aiohttp.typedefs import StrOrURL

import json

from ..exceptions import APIException, HTTPException
from .base import KavenegarAPIBase


class AsyncKavenegarAPI(KavenegarAPIBase):
    """
    ### Async version of kavenegar api

    https://kavenegar.com/rest.html
    """

    def __init__(
        self,
        apikey: str,
        timeout: Optional[int] = None,
        proxy: Optional[StrOrURL] = None,
    ):
        super().__init__(apikey, timeout)
        self.proxy = proxy
        self._session = aiohttp.ClientSession(
            headers=self.headers, timeout=aiohttp.ClientTimeout(self.timeout)
        )

    async def _request(
        self, action: str, method: str, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = self._pars_params_to_json(params)
        url = "https://{}/{}/{}/{}/{}.json".format(
            self.host, self.version, self.apikey, action, method
        )
        try:
            async with self._session.post(
                url, data=params, proxy=self.proxy
            ) as response:
                try:
                    response_data = await response.json()
                    if response_data["return"]["status"] == 200:
                        return response_data["entries"]
                    else:
                        raise APIException(
                            "APIException[{}] {}".format(
                                response_data["return"]["status"],
                                response_data["return"]["message"],
                            )
                        )
                except json.JSONDecodeError as e:
                    raise HTTPException(str(e))
        except aiohttp.ClientError as e:
            message = str(e).replace(self.apikey, self.apikey_mask)
            raise HTTPException(message)

    async def sms_send(self, params: Optional[Dict[str, Any]] = None) -> dict[str, Any]:
        return await self._request("sms", "send", params)

    async def sms_sendarray(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "sendarray", params)

    async def sms_status(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "status", params)

    async def sms_statuslocalmessageid(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "statuslocalmessageid", params)

    async def sms_select(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "select", params)

    async def sms_selectoutbox(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "selectoutbox", params)

    async def sms_latestoutbox(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "latestoutbox", params)

    async def sms_countoutbox(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "countoutbox", params)

    async def sms_cancel(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "cancel", params)

    async def sms_receive(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "receive", params)

    async def sms_countinbox(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "countinbox", params)

    async def sms_countpostalcode(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "countpostalcode", params)

    async def sms_sendbypostalcode(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("sms", "sendbypostalcode", params)

    async def verify_lookup(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("verify", "lookup", params)

    async def call_maketts(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("call", "maketts", params)

    async def call_status(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("call", "status", params)

    async def account_info(self) -> dict[str, Any]:
        return await self._request("account", "info")

    async def account_config(
        self, params: Optional[Dict[str, Any]] = None
    ) -> dict[str, Any]:
        return await self._request("account", "config", params)
