from pydantic import BaseModel
from typing import Optional, List, Literal


class ServerSetups(BaseModel):
    port: int
    address: str
    protocol: Literal["pop3","pop3s","imap","imaps","smtp","smtps"]
    isSecure: bool
    readTimeout: Optional[int]
    writeTimeout: Optional[int]
    connectionTimeout: Optional[int]
    serverStartupTimeout: Optional[int]
    isDynamicPort: Optional[bool]

class CurrentConfiguration(BaseModel):
    defaultHostname: Optional[str] = None
    portOffset: Optional[str] = None
    serverSetups: Optional[List[ServerSetups]] = None

class Message(BaseModel):
    message: str