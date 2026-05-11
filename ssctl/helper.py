import re
from urllib.parse import urlsplit

from ssctl.exceptions import InvalidDomainError
from ssctl.types import Config

# Wildcards are intentionally NOT handled here and must be processed first.
# Supports: google.com or punycode like xn--mnchen-3ya.de
DOMAIN_RE = re.compile(r"^(\*\*?\.)?([a-z0-9-]+\.)+[a-z]{2,}$")

# Strict safe path regex
PATH_RE = re.compile(r"^/[A-Za-z0-9._/-]*$")


# Validation order is IMPORTANT and should not be changed casually.
def sanitize_domain(domain: str) -> str:
    """Sanitize and validate domain patterns used by ssctl rules.

    Validation order is IMPORTANT and should not be changed casually:

    1. Normalize casing/spacing
    2. Reject obvious invalid formats (schemes, paths)
    3. Extract and validate wildcard syntax
    4. Normalize Unicode domains to ASCII punycode (IDNA)
    5. Validate final normalized domain structure

    Wildcard syntax is handled separately from domain validation:
        *.example.com   -> single-level subdomains
        **.example.com  -> multi-level subdomains

    Regex validation only applies to the final normalized domain portion.

    Raises:
        InvalidDomainError:
            If the domain format, wildcard placement,
            or normalized structure is invalid.

    """

    # normalize casing, spacing and trailing dot
    domain = domain.strip().lower().rstrip(".")

    # reject schemes
    if "://" in domain:
        raise InvalidDomainError("scheme not allowed")

    # reject paths
    if "/" in domain:
        raise InvalidDomainError("path not allowed")

    # validate wildcard placement
    if "*" in domain:
        if not (domain.startswith("*.") or domain.startswith("**.")):
            raise InvalidDomainError("invalid wildcard placement")

        # reject extra wildcards
        base = domain[2:] if domain.startswith("*.") else domain[3:]

        if "*" in base:
            raise InvalidDomainError("multiple wildcards not allowed")

    # convert Unicode → ASCII punycode
    wildcard = ""

    if domain.startswith("*."):
        domain = domain[2:]
        wildcard = "*."
    elif domain.startswith("**."):
        domain = domain[3:]
        wildcard = "**."

    domain = domain.encode("idna").decode("ascii")

    # validate structure
    if not DOMAIN_RE.match(domain):
        raise InvalidDomainError("invalid domain format")

    return wildcard + domain


def validate_path(path: str) -> str:
    """
    Validate strict safe policy paths.

    Allowed:
    - /about
    - /about/test
    - /rss.xml

    Rejected:
    - encoded chars
    - query params
    - fragments
    - unicode
    - spaces
    - traversal
    - duplicate slashes
    """

    path = path.strip()

    # Must start with /
    if not path.startswith("/"):
        raise ValueError("Path must start with '/'")

    # Reject encoded chars
    if "%" in path:
        raise ValueError("Encoded characters are not allowed")

    # Reject queries
    if "?" in path:
        raise ValueError("Query parameters are not allowed")

    # Reject fragments
    if "#" in path:
        raise ValueError("Fragments are not allowed")

    # Reject spaces
    if " " in path:
        raise ValueError("Spaces are not allowed")

    # Reject traversal
    if ".." in path:
        raise ValueError("Path traversal is not allowed")

    # Reject duplicate slashes
    if "//" in path:
        raise ValueError("Duplicate slashes are not allowed")

    # Strict ASCII-safe validation
    if not PATH_RE.fullmatch(path):
        raise ValueError("Invalid path characters")

    # Remove trailing slash
    if path != "/" and path.endswith("/"):
        path = path[:-1]

    return path


def normalize_path(path: str) -> str:
    """
    Normalize paths into canonical ssctl matching format.

    Examples:
    /about/        -> /about
    /about?id=1   -> /about
    /about#bio    -> /about
    """

    # Parse URL components
    parsed = urlsplit(path)

    # Extract path only
    normalized = parsed.path.strip()

    # Remove trailing slash
    if normalized != "/" and normalized.endswith("/"):
        normalized = normalized[:-1]

    # Ensure leading slash
    if not normalized.startswith("/"):
        normalized = "/" + normalized

    return normalized


def typed_config_to_dict(config: Config) -> dict:
    """
    Convert typed ssctl configuration objects into
    plain serializable dictionary format.

    Used when:
    - writing config back to TOML
    """

    return {
        "global": {
            "default": config.global_config.default,
        },
        "rules": [
            {
                # Convert enum -> string
                "action": rule.action.value,
                "domain": rule.domain,
                # Include path only if defined
                **({"path": rule.path} if rule.path else {}),
            }
            for rule in config.rules
        ],
    }
