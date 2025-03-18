import asyncio

from kavenegar import AsyncKavenegarAPI


async def main():
    api = AsyncKavenegarAPI(
        "546277302B414658322B70326F3449524438446B71774553724379464F7955636656352B4F7845736138343D"
    )
    res = await api.verify_lookup(
        {
            "receptor": "+989180065034",
            "token": "1234",
            "token2": "test",
            "token10": "سعید غفاری",
            "template": "DriverStopped",
        }
    )
    print(res)


asyncio.run(main())
