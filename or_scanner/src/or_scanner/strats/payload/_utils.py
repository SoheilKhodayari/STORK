import uuid
import socket
from urllib.parse import urlparse, urlunparse
from functools import reduce
from ...utils.misc import to_base
from ...logging import get_logger

logger = get_logger(__name__)

def prepend_uuid_subdomain(url):
    parsed_url = urlparse(url)
    old_netloc = parsed_url.netloc
    new_url = urlunparse(parsed_url._replace(netloc=f"{uuid.uuid4()}.{old_netloc}"))
    return new_url


def change_scheme(url, new_scheme):
    # Change scheme
    parsed_url = urlparse(url)
    old_scheme = parsed_url.scheme
    new_url = url.replace(f"{old_scheme}://", new_scheme, 1)
    return new_url


def _nip(url):
    # Convert to nip address
    parsed_url = urlparse(url)
    ip = socket.gethostbyname(parsed_url.netloc.split(":")[0])
    nip_dot = f"{parsed_url.netloc}.{ip}.nip.ip"
    nip_dash = f'{parsed_url.netloc.replace(".", "-")}-{ip.replace(".", "-")}.nip.ip'
    dot_url = url.replace(parsed_url.netloc, nip_dot, 1)
    dash_url = url.replace(parsed_url.netloc, nip_dash, 1)
    return [dot_url, dash_url]

def nip_dot(url):
    # Convert to nip address using dots as delimiter
    return _nip(url)[0]

def nip_dash(url):
    # Convert to nip address using slashes as delimiter
    return _nip(url)[1]


def _ip4(url):
    # Extract ip4 address and port

    parsed_url = urlparse(url)
    if not parsed_url.netloc:
        error_message = f"Invalid URL. Could not detect netloc ({url})"
        logger.error(error_message)
        raise ValueError(error_message)

    ip = socket.gethostbyname(parsed_url.netloc.split(":")[0]).split(".")
    port = f":{parsed_url.port}" if parsed_url.port else ""
    
    return ip, port


def ip4_oct(url):
    # Octal representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    ip_oct = [oct(int(b))[2:].ljust(3, "0") for b in ip]
    new = parsed_url._replace(netloc=f'0{".0".join(ip_oct)}{port}')
    new_url = urlunparse(new)
    return new_url

def ip4_dec(url):
    # Dec representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    new = parsed_url._replace(netloc=f'{".".join(ip)}{port}')
    new_url = urlunparse(new)
    return new_url

def ip4_hex(url):
    # Hex representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    ip_hex = [hex(int(b))[2:].ljust(2, "0") for b in ip]
    new = parsed_url._replace(netloc=f'0x{".0x".join(ip_hex)}{port}')
    new_url = urlunparse(new)
    return new_url


def ip4_dotless_oct(url):
    # Dotless octal representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    dword_ip = reduce(lambda x, y: int(x) * 256 + int(y), ip, 0)
    new = parsed_url._replace(netloc=f"0{to_base(dword_ip, 8)}{port}")
    new_url = urlunparse(new)
    return new_url

def ip4_dotless_dec(url):
    # Dotless decimal representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    dword_ip = reduce(lambda x, y: int(x) * 256 + int(y), ip, 0)
    new = parsed_url._replace(netloc=f"{dword_ip}{port}")
    new_url = urlunparse(new)
    return new_url

def ip4_dotless_hex(url):
    # Dotless hexadecimal representation
    parsed_url = urlparse(url)
    ip, port = _ip4(url)

    dword_ip = reduce(lambda x, y: int(x) * 256 + int(y), ip, 0)
    new = parsed_url._replace(netloc=f"0x{to_base(dword_ip, 16)}{port}")
    new_url = urlunparse(new)
    return new_url

def ip6(url):
    # Convert to ip6 address
    parsed_url = urlparse(url)
    ip = socket.gethostbyname(parsed_url.netloc.split(":")[0])
    new_url = url.replace(parsed_url.netloc, f"[::{ip}]", 1)
    return new_url

def ip6_mapped(url):
    # Convert to ip6 address
    parsed_url = urlparse(url)
    ip = socket.gethostbyname(parsed_url.netloc.split(":")[0])
    new_url = url.replace(parsed_url.netloc, f"[::ffff:{ip}]", 1)
    return new_url
