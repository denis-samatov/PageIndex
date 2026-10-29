# Scope of this fork

Upstream: [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex). Original authorship and license
remain with upstream; upstream performance/clinical claims are not personal
portfolio results.

Reference fork of the upstream vectorless retrieval project. No personal commits were identified in the audited default-branch history under the `denis-samatov` identity. This does not assess other identities or branches.

## Audited snapshot and limits

Portfolio audit base: `72469fb9e2249bd5b3bf0a63bcd4494a308d9484` (2026-10-28, rechecked 2026-10-29).

The frozen requirements include PyPDF2/litellm versions with advisory matches. Do not treat this historical checkout as a qualified parser/proxy deployment or process untrusted PDFs with it. A maintained execution environment needs an upstream-compatible migration and regression tests; no dependency security or benchmark qualification is claimed here.

This note changes attribution and usage guidance only. It does not certify the
upstream code, refresh its full dependency tree, or claim newly executed tests.

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
