# ssctl

Traffic control, TLS inspection, and host-based protection.

Right now this is just an early prototype built to experiment with:
- HTTPS/TLS interception
- domain blocking
- local traffic control
- policy-based filtering

The long-term goal is .... IDK, we'll see.

### Current State

- Things will break.
- TLS interception is messy.
- Browser behavior varies.
- The architecture will likely change a lot.

### Current Features

- Local HTTPS/TLS interception
- Domain blocking
- TOML-based configuration
- Embedded mitmproxy runtime

## Setup

**Requirements**

- Linux
- Python 3.12+
- uv

Install dependencies:

```bash
uv sync
```

Start ssctl

```bash
uv run python -m ssctl.main start
```

This won't work yet because ssctl uses local TLS interception for HTTPS filtering. You must trust the generated CA certificate or browsers will reject HTTPS traffic.

#### Arch Linux

Install the CA certificate:

```bash
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /etc/ca-certificates/trust-source/anchors/ssctl.crt
```

Refresh trust store:

```bash
sudo trust extract-compat
```

#### Ubuntu / Debian

Install the CA certificate:

```bash
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/ssctl.crt
```

Refresh trust store:

```bash
sudo update-ca-certificates
```

## Browser Proxy Setup

For now, browsers must use the local proxy manually.

Temporary shell setup:

```bash
export http_proxy=http://127.0.0.1:8080
export https_proxy=http://127.0.0.1:8080
```

Launch browser from the same terminal session:

```bash
chrome
```

Transparent system-wide interception without proxy exports will come later. Firefox-based browsers may ignore system certificates by default.

To fix Firefox, Go to:

```
about:config
```

Set:

```
security.enterprise_roots.enabled = true
```

Then restart the browser.
