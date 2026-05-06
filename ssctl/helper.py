import re

from ssctl.exceptions import InvalidDomainError
from ssctl.types import Config

# Wildcards are intentionally NOT handled here and must be processed first.
# Supports: google.com or punycode like xn--mnchen-3ya.de
DOMAIN_RE = re.compile(r"^(\*\*?\.)?([a-z0-9-]+\.)+[a-z]{2,}$")


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


def typed_config_to_dict(config: Config) -> dict:
    return {
        "global": {
            "default": config.global_config.default,
        },
        "rules": [
            {
                "action": rule.action.value,
                "domain": rule.domain,
                **({"path": rule.path} if rule.path else {}),
            }
            for rule in config.rules
        ],
    }
