# Vouch Protocol

[![Discord](https://img.shields.io/badge/Discord-Join_Community-7289da?logo=discord&logoColor=white)](https://discord.gg/VxgYkjdph)
[![Spec: Community](https://img.shields.io/badge/Spec-Community_License-green.svg)](https://github.com/vouch-protocol/vouch/blob/main/licenses/LICENSE-SPEC)
[![Client: Apache 2.0](https://img.shields.io/badge/Client-Apache_2.0-blue.svg)](https://github.com/vouch-protocol/vouch/blob/main/LICENSE)
[![Server: AGPL-3.0](https://img.shields.io/badge/Server-AGPL_3.0-orange.svg)](https://github.com/vouch-protocol/vouch/blob/main/licenses/LICENSE-SERVER)
[![Status](https://img.shields.io/badge/Status-Public_Beta-yellow)](https://github.com/vouch-protocol/vouch)

> **The Open Standard for AI Agent Identity & Accountability**
> 
> When Anthropic launched MCP, they solved "how agents call tools."  
> They didn't solve "how we TRUST those agents."
> 
> **Vouch Protocol is the SSL certificate for AI agents.**

[Read the spec →](https://github.com/vouch-protocol/vouch/blob/main/docs/vouch_guide.md) | [Join Discord →](https://discord.gg/VxgYkjdph)

---

## The Problem

AI agents are making real-world API calls with **ZERO cryptographic proof** of:
- **WHO** they are
- **WHAT** they intended to do  
- **WHEN** they did it

**Examples of the risk:**
- Healthcare AI accesses patient data → HIPAA violation risk
- Financial AI makes unauthorized trades → Liability nightmare
- Customer service AI leaks data → Compliance failure

**Current solutions:**
- **DIY JWT signing** → No agent-specific features, security mistakes easy
- **Nothing** → Most people just YOLO it and hope for the best

---

## The Solution

**Vouch Protocol** provides cryptographic identity for AI agents, modeled after SSL/TLS:

✅ **Ed25519 signatures** (industry-standard cryptography)  
✅ **JWK key format** (works with existing infrastructure)  
✅ **Audit trail** (cryptographic proof of every action)  
✅ **Framework-agnostic** (works with MCP, LangChain, CrewAI, etc.)  
✅ **Open source** (Apache 2.0 license)

**Think of it as:**
- SSL certificate = Proves website identity
- **Vouch Protocol = Proves AI agent identity**

---

## Why Vouch Protocol?

### vs. DIY JWT

| Feature | Vouch Protocol | DIY JWT |
|---------|---------------|---------|
| **Agent-specific** | ✅ (designed for agents) | ❌ (generic) |
| **MCP integration** | ✅ (native) | ❌ (manual) |
| **Framework integrations** | ✅ (LangChain, CrewAI, etc.) | ❌ |
| **Audit trail format** | ✅ (standardized) | ❌ (custom) |
| **Security best practices** | ✅ (built-in) | ⚠️ (easy to mess up) |

---

## Quick Start

### 1. Install
```bash
pip install vouch-protocol
```

### 2. Generate Identity
```bash
vouch init --domain your-agent.com
```

### 3. Sign an Action (Agent Side)
```python
from vouch import Signer
import os

signer = Signer(
    private_key=os.environ['VOUCH_PRIVATE_KEY'],
    did=os.environ['VOUCH_DID']
)

token = signer.sign({'action': 'read_database', 'target': 'users'})
# Include token in Vouch-Token header
```

### 4. Verify (API Side)
```python
from fastapi import FastAPI, Header, HTTPException
from vouch import Verifier

app = FastAPI()

@app.post("/api/resource")
def protected_route(vouch_token: str = Header(alias="Vouch-Token")):
    public_key = '{"kty":"OKP"...}' # From agent's vouch.json
    
    is_valid, passport = Verifier.verify(vouch_token, public_key_jwk=public_key)
    
    if not is_valid:
        raise HTTPException(status_code=401, detail="Untrusted Agent")
        
    return {"status": "Verified", "agent": passport.sub}
```

**That's it.** 3 lines to sign, 3 lines to verify.

---

## Integrations

Works with all major AI frameworks out-of-the-box:

- ✅ **Model Context Protocol (MCP)** - Native integration for Claude Desktop & Cursor
- ✅ **LangChain** - Sign tool calls automatically
- ✅ **CrewAI** - Multi-agent identity management
- ✅ **AutoGPT** - Autonomous agent signing
- ✅ **AutoGen** - Microsoft multi-agent framework
- ✅ **Google Vertex AI** - Sign function calls
- ✅ **n8n** - Low-code agent workflows

[See all integrations →](https://github.com/vouch-protocol/vouch/tree/main/vouch/integrations)

---

## Enterprise Features

- 🔐 **Key Rotation** - Automatic rotating keys for production
- 🎙️ **Voice AI Signing** - Sign audio frames in real-time  
- ☁️ **Cloud KMS** - AWS KMS, GCP Cloud KMS, Azure Key Vault
- 📊 **Reputation Scoring** - Track agent behavior over time
- 🚫 **Revocation Registry** - Blacklist compromised keys
- ⚡ **Redis Caching** - Production-scale verification

---

## 📜 License & Legal

This project uses a **3-layer license structure** to balance open collaboration and sustainability:

1. **Specification:** [Community Specification License 1.0](https://github.com/vouch-protocol/vouch/blob/main/licenses/LICENSE-SPEC) 
   - The protocol standard (open for anyone to implement)
   
2. **Client SDK:** [Apache License 2.0](https://github.com/vouch-protocol/vouch/blob/main/LICENSE)
   - The reference implementation (permissive for all uses)
   
3. **Server SDK:** [AGPL-3.0](https://github.com/vouch-protocol/vouch/blob/main/licenses/LICENSE-SERVER) OR Commercial License
   - Network-facing components (pass-forward obligation OR paid license)

**TL;DR for developers:**
- ✅ Using the client library? **Apache 2.0** (use freely, even in closed-source)
- ✅ Implementing the protocol yourself? **Community Spec License** (open standard)
- ⚠️ Running the server component? **AGPL** (open-source your server) OR [contact us](mailto:commercial@vouch-protocol.com) for commercial license

**Default LICENSE:** This repository's main LICENSE file is Apache 2.0 for maximum compatibility. See individual components for specific licenses.

[View licenses/ directory](https://github.com/vouch-protocol/vouch/tree/main/licenses)

## Defensive Disclosure (Prior Art)
**Publication Date:** December 14, 2025  
**Subject:** Cryptographic Binding of AI Agent Intent via Model Context Protocol (MCP)

To ensure the freedom of the ecosystem to build secure agents, we explicitly disclose the following novel method as Prior Art:

1. **The "Identity Sidecar" Pattern:** An MCP Server acting as a local "Identity Proxy" for a stateless LLM, isolating keys from application code.
2. **Just-in-Time (JIT) Intent Signing:** A workflow where the LLM requests a signed "Vouch-Token" for a specific action *before* execution.
3. **Non-Repudiation:** Generating a cryptographically verifiable audit trail binding Identity, Intent, and Time.
