"""Request Signer

Employed for generating the "Signature" header in authentication requests.
"""

import base64
from datetime import UTC, datetime
import hashlib
import struct

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

from pythonxbox.authentication.models import SignaturePolicy
from pythonxbox.common import filetimes

DEFAULT_SIGNING_POLICY = SignaturePolicy(
    version=1, supported_algorithms=["ES256"], max_body_bytes=8192
)


class RequestSigner:
    def __init__(
        self,
        signing_key: ec.EllipticCurvePrivateKey | None = None,
        signing_policy: SignaturePolicy | None = None,
    ) -> None:
        self.signing_key = signing_key or ec.generate_private_key(ec.SECP256R1())
        self.signing_policy = signing_policy or DEFAULT_SIGNING_POLICY

        pub_nums = self.signing_key.public_key().public_numbers()
        self.proof_field = {
            "use": "sig",
            "alg": self.signing_policy.supported_algorithms[0],
            "kty": "EC",
            "crv": "P-256",
            "x": self.__encode_ec_coord(pub_nums.x),
            "y": self.__encode_ec_coord(pub_nums.y),
        }

    def export_signing_key(self) -> str:
        return self.signing_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.TraditionalOpenSSL,
            serialization.NoEncryption(),
        ).decode()

    @staticmethod
    def import_signing_key(signing_key: str) -> ec.EllipticCurvePrivateKey:
        key = serialization.load_pem_private_key(signing_key.encode(), password=None)
        if not isinstance(key, ec.EllipticCurvePrivateKey):
            msg = "Expected an EC private key"
            raise TypeError(msg)
        return key

    @classmethod
    def from_pem(cls, pem_string: str) -> "RequestSigner":
        request_signer = RequestSigner.import_signing_key(pem_string)
        return cls(request_signer)

    @staticmethod
    def get_timestamp_buffer(dt: datetime) -> bytes:
        """
        Get usable buffer from datetime

        dt: Input datetime

        Returns:
            bytes: FILETIME buffer (network order/big endian)
        """
        filetime = filetimes.dt_to_filetime(dt)
        return struct.pack("!Q", filetime)

    @staticmethod
    def get_signature_version_buffer(version: int) -> bytes:
        """
        Get big endian uint32 bytes-representation from
        signature version

        version: Signature version

        Returns: Version as uint32 big endian bytes
        """
        return struct.pack("!I", version)

    def verify_digest(
        self,
        signature: bytes,
        digest: bytes,
        verifying_key: ec.EllipticCurvePublicKey | None = None,
    ) -> bool:
        """
        Verify signature against digest

        signature: Signature to validate
        message: Digest to verify
        verifying_key: Public key to use for verification.
                       If that key is not provided, the private key used for signing is used.

        Returns: True on successful verification, False otherwise
        """
        verifier = verifying_key or self.signing_key.public_key()
        r = int.from_bytes(signature[:32], "big")
        s = int.from_bytes(signature[32:], "big")
        der_sig = utils.encode_dss_signature(r, s)
        verifier.verify(der_sig, digest, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        return True

    def sign(
        self,
        method: str,
        path_and_query: str,
        body: bytes = b"",
        authorization: str = "",
        timestamp: datetime | None = None,
    ) -> str:
        if timestamp is None:
            timestamp = datetime.now(UTC)

        signature = self._sign_raw(
            method, path_and_query, body, authorization, timestamp
        )
        return base64.b64encode(signature).decode("ascii")

    def _sign_raw(
        self,
        method: str,
        path_and_query: str,
        body: bytes,
        authorization: str,
        timestamp: datetime,
    ) -> bytes:
        # Get big-endian representation of signature version and timestamp (FILETIME)
        signature_version_bytes = self.get_signature_version_buffer(
            self.signing_policy.version
        )
        ts_bytes = self.get_timestamp_buffer(timestamp)

        # Concatenate bytes to sign + hash
        data = self._concat_data_to_sign(
            signature_version_bytes,
            method,
            path_and_query,
            body,
            authorization,
            ts_bytes,
            self.signing_policy.max_body_bytes,
        )

        # Calculate digest
        digest = self._hash(data)

        # Sign the hash
        der_sig = self.signing_key.sign(
            digest,
            ec.ECDSA(utils.Prehashed(hashes.SHA256()), deterministic_signing=True),
        )
        r, s = utils.decode_dss_signature(der_sig)
        signature = r.to_bytes(32, "big") + s.to_bytes(32, "big")

        # Return signature version + timestamp encoded + signature
        return signature_version_bytes + ts_bytes + signature

    @staticmethod
    def _hash(data: bytes) -> bytes:
        """Compute SHA-256 hash of the input data."""
        return hashlib.sha256(data).digest()

    @staticmethod
    def _concat_data_to_sign(  # noqa: PLR0913
        signature_version: bytes,
        method: str,
        path_and_query: str,
        body: bytes,
        authorization: str,
        ts_bytes: bytes,
        max_body_bytes: int,
    ) -> bytes:
        body_size_to_hash = min(len(body), max_body_bytes)

        return (
            signature_version
            + b"\x00"
            + ts_bytes
            + b"\x00"
            + method.upper().encode("ascii")
            + b"\x00"
            + path_and_query.encode("ascii")
            + b"\x00"
            + authorization.encode("ascii")
            + b"\x00"
            + body[:body_size_to_hash]
            + b"\x00"
        )

    @staticmethod
    def __base64_escaped(binary: bytes) -> str:
        return (
            base64.b64encode(binary)
            .decode("ascii")
            .rstrip("=")
            .replace("+", "-")
            .replace("/", "_")
        )

    @staticmethod
    def __encode_ec_coord(coord: int) -> str:
        return RequestSigner.__base64_escaped(coord.to_bytes(32, "big"))
