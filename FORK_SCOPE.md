# Scope of this fork

Upstream: [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex). Original authorship and license
remain with upstream; upstream performance/clinical claims are not personal
portfolio results.

Reference fork of the upstream vectorless retrieval project. No personal commits were identified at the original audit base under the `denis-samatov` identity. Subsequent personal adapter and dependency contributions are described below; they do not transfer upstream authorship.

## Audited snapshot and limits

Portfolio audit base: `72469fb9e2249bd5b3bf0a63bcd4494a308d9484` (2026-10-28, rechecked 2026-10-29).

The original requirements included PyPDF2/litellm versions with advisory matches. The maintained profile below replaces them. Historical snapshots remain unsuitable for untrusted PDFs; neither snapshot is a parser sandbox or a qualified proxy deployment.

The original note changed attribution and usage guidance only. Subsequent changes
and their bounded verification are recorded separately below.

## Adapter follow-up — 2026-10-29

The subsequent personal contribution is limited to the own-model Anthropic
chat adapter and its regression tests. It normalizes a terminal assistant
reply already recorded by newer SDKs, preventing duplicate text and unanswered
terminal tool calls in the appendable conversation. Tests also distinguish
legacy full-history requests from SDK message-thread continuation and preserve
caller headers without rejecting SDK protocol betas.

Local mock-only validation on Python 3.13.15, with Anthropic 2.3.0 and separately
0.108.0, passed the full suite in each environment: **432 passed, 7 skipped**.
The chat module passed **115 tests** with each SDK. Optional Claude Agent SDK
tests were not qualified locally; no real provider calls, deployment, benchmark
or dependency-security qualification is claimed. Existing upstream authorship,
untrusted-PDF and dependency limitations above remain applicable.


## Maintained dependency profile — 2026-10-30

This fork now requires **Python 3.11+**. The patched `filelock>=4.2.1`
requires Python 3.11, so retaining a Python 3.10 installation claim would leave
known vulnerabilities unresolved. Python 3.10 users must retain a historical
snapshot with its documented risks or upgrade; this is an explicit support change.

- Replaced unmaintained PyPDF2 3.0.1 with pypdf 6.21.4. A bounded subprocess
  regression reproduces the old parser's unterminated-comment hang and checks
  successful extraction with pypdf. The legacy `pdf_parser="PyPDF2"` selector
  remains accepted, alongside `"pypdf"`.
- Pinned the maintained application profile to LiteLLM 1.100.4 and imposed a
  filelock security floor. Newer LiteLLM releases imposing `filelock<4` are
  incompatible with that floor; the resolver must reject them rather than force
  an unsupported override.
- Generated complete Linux Python 3.11 and 3.13 CI locks, including optional
  frameworks. CI installs with hashes, exercises framework presence/absence,
  and audits every locked package against OSV without Dependency Graph settings.
  The pdfium 4 compatibility leg is separate from the maintained pdfium 5 profile.

Reproduce from a checkout on the matching Linux interpreter:

```bash
python -m pip install --require-hashes -r requirements-ci-py3.13-linux.lock
LITELLM_LOCAL_MODEL_COST_MAP=True python -m pytest -q
python -m pip install pip-audit==2.10.1
python -m pip_audit --strict --disable-pip --require-hashes -s osv -r requirements-ci-py3.13-linux.lock
# Regenerate, rather than editing a generated lock:
uv pip compile requirements-ci.in --python-version 3.13 --python-platform x86_64-unknown-linux-gnu --generate-hashes --output-file requirements-ci-py3.13-linux.lock
```

On macOS/Python 3.13.13, the patched profile passed **433 tests, 7 skipped**;
optional Claude SDK and live-key cases were not exercised in that local run.
The actual installed environment had no known OSV matches at the audit time.
This is a point-in-time dependency result, not proof of exploit absence, real
provider compatibility, document retrieval quality or deployment readiness.
Published upstream `pageindex` wheels are not artifacts of this fork; install
this checkout to obtain these changes. No release/package was published.
