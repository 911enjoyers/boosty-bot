import struct
from datetime import datetime
from typing import Callable

from bruhsty.service import proto
from bruhsty.service.otp import CodeAlreadyUsedError, CodeInvalidError
from bruhsty.service.otp.errors import CodeExpiredError
from bruhsty.storage.verification_codes.models import Code, CodeCreate


class OTPService:
    def __init__(
        self,
        random: Callable[[int], bytes],
        codes_store: proto.CodeStorage,
    ) -> None:
        self.random = random
        self.codes_store = codes_store

    async def generate_otp(self, telegram_id: int, user_email: str) -> Code:
        otp_bytes = self.random(4)  # создал 6 рандомных байтов
        otp_tuple = struct.unpack("I", otp_bytes)
        otp_str = "".join(otp_tuple)
        short_otp_str = otp_str[:6]
        otp = short_otp_str.rjust(6, "0")
        code = await self.codes_store.create(CodeCreate(telegram_id, user_email, otp))
        return code

    async def validate_otp(self, telegram_id: int, user_email: str, otp: str) -> None:
        query = (Code.user_id == telegram_id) & (Code.email == user_email) & (Code.code == otp)
        codes = self.codes_store.find_all(query)
        if not codes:
            raise CodeInvalidError(otp, user_email, telegram_id)

        first_code = codes[0]
        if first_code.used_at is not None:
            raise CodeAlreadyUsedError(otp, user_email, telegram_id, first_code.used_at)

        if first_code.valid_until < datetime.now():
            raise CodeExpiredError(otp, user_email, telegram_id, first_code.valid_until)

        await self.codes_store.update(first_code.id, used_at=datetime.now())
