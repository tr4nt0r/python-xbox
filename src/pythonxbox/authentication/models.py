"""Authentication Models."""

from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from pythonxbox.common.models import PascalCaseModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class XTokenResponse(PascalCaseModel):
    issue_instant: datetime
    not_after: datetime
    token: str

    def is_valid(self) -> bool:
        return self.not_after > utc_now()


class XADDisplayClaims(BaseModel):
    """{"xdi": {"did": "F.....", "dcs": "0"}}"""

    xdi: dict[str, str]


class XADResponse(XTokenResponse):
    display_claims: XADDisplayClaims


class XATDisplayClaims(BaseModel):
    xti: dict[str, str]


class XATResponse(XTokenResponse):
    display_claims: XATDisplayClaims


class XAUDisplayClaims(BaseModel):
    xui: list[dict[str, str]]


class XAUResponse(XTokenResponse):
    display_claims: XAUDisplayClaims


class XSTSDisplayClaims(BaseModel):
    xui: list[dict[str, str]]


class XSTSResponse(XTokenResponse):
    display_claims: XSTSDisplayClaims

    @property
    def xuid(self) -> str:
        return self.display_claims.xui[0]["xid"]

    @property
    def userhash(self) -> str:
        return self.display_claims.xui[0]["uhs"]

    @property
    def gamertag(self) -> str:
        return self.display_claims.xui[0]["gtg"]

    @property
    def age_group(self) -> str:
        return self.display_claims.xui[0]["agg"]

    @property
    def privileges(self) -> str:
        return self.display_claims.xui[0]["prv"]

    @property
    def user_privileges(self) -> str:
        return self.display_claims.xui[0]["usr"]

    @property
    def authorization_header_value(self) -> str:
        return f"XBL3.0 x={self.userhash};{self.token}"


class OAuth2TokenResponse(BaseModel):
    token_type: str
    expires_in: int
    scope: str
    access_token: str
    refresh_token: str | None = None
    user_id: str
    issued: datetime = Field(default_factory=utc_now)

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()


"""XAL related models"""


@dataclass
class XalAppParameters:
    app_id: str
    title_id: str
    redirect_uri: str


@dataclass
class XalClientParameters:
    user_agent: str
    device_type: str
    client_version: str
    query_display: str


class SisuAuthenticationResponse(PascalCaseModel):
    msa_oauth_redirect: str
    msa_request_parameters: dict[str, str]


class SisuAuthorizationResponse(PascalCaseModel):
    device_token: str
    title_token: XATResponse
    user_token: XAUResponse
    authorization_token: XSTSResponse
    web_page: str
    sandbox: str
    use_modern_gamertag: bool | None = None


"""Signature related models"""


class TitleEndpoint(PascalCaseModel):
    protocol: str
    host: str
    host_type: str
    path: str | None = None
    relying_party: str | None = None
    sub_relying_party: str | None = None
    token_type: str | None = None
    signature_policy_index: int | None = None
    server_cert_index: list[int] | None = None


class SignaturePolicy(PascalCaseModel):
    version: int
    supported_algorithms: list[str]
    max_body_bytes: int


class TitleEndpointCertificate(PascalCaseModel):
    thumbprint: str
    is_issuer: bool | None = None
    root_cert_index: int


class TitleEndpointsResponse(PascalCaseModel):
    end_points: list[TitleEndpoint]
    signature_policies: list[SignaturePolicy]
    certs: list[TitleEndpointCertificate]
    root_certs: list[str]
