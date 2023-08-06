from datetime import datetime
from typing import Optional

import attr


@attr.dataclass(frozen=True, slots=True)
class FasilitasLayanan:
    fasilitas_layanan_id: str
    nama: str
    create_date: datetime
    last_update: datetime
    expired_date: Optional[datetime]
    last_sync: datetime

    def __str__(self):
        return self.nama
