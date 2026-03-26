"""Platform-wide configuration using pydantic settings pattern."""

from pydantic import BaseModel


class MeridianConfig(BaseModel):
    vault_addr: str = "https://vault.meridian.local:8200"
    vault_cacert: str = "/certs/rootCA.pem"
    quickwit_url: str = "https://quickwit.meridian.local:7280"
    victoriametrics_url: str = "https://victoriametrics.meridian.local:8428"
    log_level: str = "INFO"
