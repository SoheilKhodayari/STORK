from urllib.parse import urlparse
from ..logging import get_logger


def load_domains(filename):
    logger = get_logger(__name__)
    domains = []
    if not filename:
        logger.debug(f"No domain file prodided. Nothing loaded.")
        return domains
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            domains = prepare_domains(lines)
            logger.debug(f"Loaded {len(domains)} domains from {filename}")
    except Exception:
        logger.warn(f"Failed to load domains from {filename}")
    return domains


def load_qkeys(filename):
    logger = get_logger(__name__)
    qkeys = []
    if not filename:
        logger.debug(f"No qkey file prodided. Nothing loaded.")
        return qkeys
    try:
        with open(filename, "r") as f:
            lines = f.read().splitlines()
            qkeys = prepare_qkeys(lines)
            logger.debug(f"Loaded {len(qkeys)} qkeys from {filename}")
    except Exception:
        logger.warn(f"Failed to load qkeys from {filename}")
    return qkeys


def prepare_qkeys(qkey_list):
    qkeys = set()
    for qkey in qkey_list:
        qkey = qkey.strip()
        if qkey and not qkey.startswith("#"):
            qkeys.add(qkey)
    return list(qkeys)


def prepare_domains(domain_list):
    logger = get_logger(__name__)
    domains = set()
    for domain in domain_list:
        domain = domain.strip()
        if domain and not domain.startswith("#"):
            if not validate_domain(domain):
                logger.warn(f"Ignoring invalid domain: {domain}")
            else:
                domains.add(domain)
    return list(domains)

def validate_domain(domain):
    try:
        parsed_url = urlparse(domain) 
        if (not parsed_url.scheme
            and not parsed_url.netloc
            and parsed_url.path
            and not parsed_url.params
            and not parsed_url.query
            and not parsed_url.fragment):
            return True
    except:
        return False
    return False


