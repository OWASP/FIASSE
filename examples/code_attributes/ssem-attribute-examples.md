# SSEM Attribute Examples — "With" vs "Without"

> Closes/relates to [OWASP/FIASSE#14](https://github.com/OWASP/FIASSE/issues/14) — *"Contrast each attribute 'with' vs 'without' each attribute."*

This document provides one contrasting Python example per attribute of the Securable Software Engineering Model (FIASSE RFC [§3.1–3.2](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md#31-model-overview-and-design-language)): **Maintainability** (Analyzability, Modifiability, Testability, Observability), **Trustworthiness** (Confidentiality, Accountability, Authenticity), and **Reliability** (Availability, Integrity, Resilience).

Ground rules, applied to every example:

- **Runnable as-is, standard library only** (Python 3.10+). Where an example needs an external collaborator (database, payment gateway, remote service), it appears as a clearly marked in-memory stub so each block executes without infrastructure.
- **Both versions do the same job.** The ❌ and ✅ versions of a pair implement the same behavior; the delta is the attribute. Where the ✅ version deliberately changes a second thing (e.g., narrowing an exception handler), the comment says so and explains why it belongs to the attribute.
- **Definitions are the RFC's.** Each attribute opens with the RFC §3.2 definition (ISO-sourced), not a paraphrase.
- **Money is integer cents.** SSEM Integrity is the "property of accuracy and completeness" [ISO-27000 §3.36], and binary floats cannot represent 0.1 — so monetary values use exact integer arithmetic throughout.
- **Grounded and measurable.** Each pair ends with its OWASP/CWE grounding and a one-line verification check drawn from RFC [Appendix A](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md#appendix-a-measuring-ssem-attributes), the framework's own measurement guidance — so the examples double as review-checklist entries.

Language convention: `❌ Without <Attribute>` shows a version that lacks the attribute (and the concrete risk that follows), `✅ With <Attribute>` shows the same scenario engineered to have it.

---

## Maintainability

*"The degree of effectiveness and efficiency with which a product or system can be modified by the intended maintainers"* [RFC §3.2.1, ISO-25010]. It has been evolved, corrected, and adapted to new threats *"without undue effort or the introduction of new vulnerabilities."*

### 1. Analyzability

*"The degree of effectiveness and efficiency with which it is possible to assess the impact on a product or system of an intended change to one or more of its parts, or to diagnose a product for deficiencies or causes of failures, or to identify parts to be modified"* [RFC §3.2.1.1, ISO-25010 §4.2.7.3]. In practical terms: the ability to locate the cause of a behavior within the code — which directly determines the speed and accuracy of vulnerability remediation.

```python
# ❌ Without Analyzability
# --- in-memory stand-ins so the example runs as-is --------------------------
_ORDERS: list[tuple[str, int]] = []
_OUTBOX: list[tuple[str, str]] = []

def _db_insert_order(customer_id: str, total_cents: int) -> None:
    _ORDERS.append((customer_id, total_cents))

def _send_email(address: str, message: str) -> None:
    _OUTBOX.append((address, message))
# ----------------------------------------------------------------------------

# One function mixes input checking, pricing rules, persistence, and
# notification. The security-relevant question "what code can change an
# order's total?" has no localized answer: a reviewer must read and
# mentally execute the whole function to assess any change.
def process_order(data):
    if data.get("qty") and data["qty"] > 0:
        total_cents = data["qty"] * data["unit_price_cents"]
        if data.get("coupon") == "VIP10":
            total_cents = total_cents * 90 // 100         # 10% off
        if data["customer"]["country"] == "US":
            total_cents = total_cents * 10825 // 10000    # 8.25% tax
        _db_insert_order(data["customer"]["id"], total_cents)
        if total_cents > 500_00:
            _send_email(data["customer"]["email"], "High value order placed")
    return total_cents  # The tangle also hides a crash path: if "qty" is
                        # missing or 0, this line raises UnboundLocalError.
                        # Low analyzability is where bugs like this go unseen.
```

```python
# ✅ With Analyzability
# Same job -- validate, price, persist, notify -- but every concern is a
# named, single-purpose unit. "How is the discount applied?" is answered by
# reading apply_coupon alone, and the invalid-order path is explicit
# instead of a hidden crash.
from dataclasses import dataclass

# --- in-memory stand-ins so the example runs as-is --------------------------
_ORDERS: list[tuple[str, int]] = []
_OUTBOX: list[tuple[str, str]] = []

def _db_insert_order(customer_id: str, total_cents: int) -> None:
    _ORDERS.append((customer_id, total_cents))

def _send_email(address: str, message: str) -> None:
    _OUTBOX.append((address, message))
# ----------------------------------------------------------------------------

VIP_COUPON = "VIP10"
US_TAX_BASIS_POINTS = 10_825   # 8.25% tax, as basis points of 10_000
HIGH_VALUE_CENTS = 500_00


@dataclass(frozen=True)
class OrderRequest:
    customer_id: str
    customer_email: str
    customer_country: str
    quantity: int
    unit_price_cents: int
    coupon_code: str | None = None


def parse_order(data: dict) -> OrderRequest:
    quantity = int(data.get("qty", 0))
    if quantity <= 0:
        raise ValueError("order quantity must be a positive integer")
    return OrderRequest(
        customer_id=data["customer"]["id"],
        customer_email=data["customer"]["email"],
        customer_country=data["customer"]["country"],
        quantity=quantity,
        unit_price_cents=data["unit_price_cents"],
        coupon_code=data.get("coupon"),
    )


def apply_coupon(subtotal_cents: int, coupon_code: str | None) -> int:
    return subtotal_cents * 90 // 100 if coupon_code == VIP_COUPON else subtotal_cents


def apply_tax(amount_cents: int, country: str) -> int:
    return amount_cents * US_TAX_BASIS_POINTS // 10_000 if country == "US" else amount_cents


def calculate_total(order: OrderRequest) -> int:
    subtotal = order.quantity * order.unit_price_cents
    return apply_tax(apply_coupon(subtotal, order.coupon_code), order.customer_country)


def process_order(data: dict) -> int:
    order = parse_order(data)            # invalid input fails loudly, up front
    total_cents = calculate_total(order)
    _db_insert_order(order.customer_id, total_cents)
    if total_cents > HIGH_VALUE_CENTS:
        _send_email(order.customer_email, "High value order placed")
    return total_cents
```

**Verify it** [RFC A.1.1]: unit size and cyclomatic complexity per function are now small enough to review in isolation — "time to understand" the discount rule is the time to read `apply_coupon`.

**Grounding:** contributing factors *Unit Size* and *Unit Complexity* [RFC §3.2.1.1]; CWE-1120 (Excessive Code Complexity).

---

### 2. Modifiability

*"The degree to which a product or system can be effectively and efficiently modified without introducing defects or degrading existing product quality"* [RFC §3.2.1.2, ISO-25010 §4.2.7.4] — the ability to change code without breaking existing functionality or introducing new vulnerabilities.

```python
# ❌ Without Modifiability
# The password policy is duplicated in three places. Changing the minimum
# length requires finding and editing every copy -- miss one and the system
# silently enforces inconsistent rules. Note where the drift landed: the
# WEAKEST copy of the rule guards the MOST privileged path.
def register_user(password: str) -> bool:
    return len(password) >= 8 and any(c.isdigit() for c in password)


def reset_password(password: str) -> bool:
    return len(password) >= 8 and any(c.isdigit() for c in password)


def admin_change_password(password: str) -> bool:
    return len(password) >= 6 and any(c.isdigit() for c in password)  # drifted!
```

```python
# ✅ With Modifiability
# The policy lives in exactly one place, so it cannot drift. Behavior is
# identical to the intended policy above (minimum 8, one digit) -- and
# strengthening it, e.g. PasswordPolicy(min_length=12), is now a one-line
# change that is guaranteed to apply to every path, including admin.
from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 8
    require_digit: bool = True

    def is_valid(self, password: str) -> bool:
        if len(password) < self.min_length:
            return False
        if self.require_digit and not any(c.isdigit() for c in password):
            return False
        return True


PASSWORD_POLICY = PasswordPolicy()


def register_user(password: str) -> bool:
    return PASSWORD_POLICY.is_valid(password)


def reset_password(password: str) -> bool:
    return PASSWORD_POLICY.is_valid(password)


def admin_change_password(password: str) -> bool:
    return PASSWORD_POLICY.is_valid(password)
```

**Verify it** [RFC A.1.2]: change-impact size for "raise the minimum length" is one line in one file; `grep` for `len(password)` finds exactly one definition.

**Grounding:** contributing factor *Duplication* [RFC §3.2.1.2]; CWE-1041 (Use of Redundant Code); OWASP Authentication Cheat Sheet (password length requirements).

---

### 3. Testability

*"The degree of effectiveness and efficiency with which test criteria can be established for a system, product or component and tests can be performed to determine whether those criteria have been met"* [RFC §3.2.1.3, ISO-25010 §4.2.7.5]. Operationally: *"the ability to write a test for a piece of code without modifying the code under test."* Testability is what lets a team verify that security controls actually work — a control you cannot test is a requirement you cannot verify.

```python
# ❌ Without Testability
# The lockout rule (a security control -- CWE-307 protection) is entangled
# with I/O: a module-global database and an inline clock read. To unit test
# "is this account locked out?" you must patch module globals and freeze
# time -- i.e., modify the conditions of the code under test.
from datetime import datetime, timedelta, timezone

# --- in-memory stand-in so the example runs as-is ---------------------------
_ROWS = {"u1": {"failed_attempts": 5, "last_failed_at": datetime.now(timezone.utc)}}

class _Db:
    def fetch_user(self, user_id: str) -> dict:
        return _ROWS[user_id]

db_conn = _Db()
# ----------------------------------------------------------------------------


def is_account_locked(user_id: str) -> bool:
    row = db_conn.fetch_user(user_id)                    # hidden I/O dependency
    if row["failed_attempts"] >= 5:
        elapsed = datetime.now(timezone.utc) - row["last_failed_at"]  # hidden clock
        return elapsed < timedelta(minutes=15)
    return False
```

```python
# ✅ With Testability
# The lockout *rule* is a pure function of its inputs: state in, decision
# out, clock injected. The tests below are real, runnable code -- no
# database, no patching, no waiting 15 minutes.
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class LoginState:
    failed_attempts: int
    last_failed_at: datetime | None


def is_locked_out(
    state: LoginState,
    now: datetime,
    threshold: int = 5,
    cooldown: timedelta = timedelta(minutes=15),
) -> bool:
    if state.failed_attempts < threshold or state.last_failed_at is None:
        return False
    return (now - state.last_failed_at) < cooldown


def test_recent_failures_block_login() -> None:
    state = LoginState(5, datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc))
    assert is_locked_out(state, now=datetime(2026, 1, 1, 12, 5, tzinfo=timezone.utc))


def test_lockout_expires_after_cooldown() -> None:
    state = LoginState(5, datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc))
    assert not is_locked_out(state, now=datetime(2026, 1, 1, 12, 20, tzinfo=timezone.utc))


if __name__ == "__main__":
    test_recent_failures_block_login()
    test_lockout_expires_after_cooldown()
    print("ok")
```

**Verify it** [RFC A.1.3]: mocking/stubbing complexity for the lockout rule is zero; the two tests run in milliseconds on every commit.

**Grounding:** the scenario is CWE-307 (Improper Restriction of Excessive Authentication Attempts) — the point is that only the testable version can *prove* the protection works; RFC §3.2.1.3 ("verify that security controls function as intended").

---

### 4. Observability

*"The degree to which the internal state of a system can be inferred from its external outputs"* [RFC §3.2.1.4]. The RFC's measurement guidance names the exact failure mode shown here: *failure-path observability* — "silent failures and exception swallowing are common gaps" [RFC A.1.4].

```python
# ❌ Without Observability
# Failures are swallowed silently. When a payment fails in production,
# there is no external signal -- no log, no metric, no trace -- from which
# anyone can infer what happened, or that anything happened at all.

# --- in-memory stand-in so the example runs as-is ---------------------------
class PaymentGatewayError(Exception):
    pass

class _DecliningGateway:
    def charge(self, customer_id: str, amount_cents: int) -> None:
        raise PaymentGatewayError("card declined: insufficient funds")

payment_gateway = _DecliningGateway()
# ----------------------------------------------------------------------------


def charge_card(customer_id: str, amount_cents: int) -> bool:
    try:
        payment_gateway.charge(customer_id, amount_cents)
        return True
    except Exception:
        return False
```

```python
# ✅ With Observability
# Every path -- attempt, failure, success -- emits a structured, contextual
# event (per the OWASP Logging Cheat Sheet: no card numbers or other
# sensitive data, but enough context to reconstruct what happened).
#
# Two deliberate details:
#  * The events are emitted as explicit JSON. Stock `logging` formatters
#    silently DROP `extra={...}` fields, so "structured logging" that relies
#    on them emits no structure unless a custom formatter is installed.
#  * `correlation_id` is accepted from the caller, propagated from the
#    incoming request -- a fresh UUID minted here would correlate nothing.
import json
import logging

logging.basicConfig(level=logging.INFO)   # so the events are actually visible
logger = logging.getLogger("payments")

# --- in-memory stand-in so the example runs as-is ---------------------------
class PaymentGatewayError(Exception):
    pass

class _DecliningGateway:
    def charge(self, customer_id: str, amount_cents: int) -> None:
        raise PaymentGatewayError("card declined: insufficient funds")

payment_gateway = _DecliningGateway()
# ----------------------------------------------------------------------------


def _log_event(event: str, **context) -> None:
    logger.info(json.dumps({"event": event, **context}))


def charge_card(customer_id: str, amount_cents: int, correlation_id: str) -> bool:
    _log_event("payment.attempt", correlation_id=correlation_id,
               customer_id=customer_id, amount_cents=amount_cents)
    try:
        payment_gateway.charge(customer_id, amount_cents)
    except PaymentGatewayError as exc:
        # Narrowing `except Exception` to the gateway's error type is part of
        # the observability fix, not a side change: absorbing unknown
        # exceptions was precisely how the system went dark. Unexpected
        # exceptions now propagate loudly instead of vanishing.
        _log_event("payment.failed", correlation_id=correlation_id,
                   customer_id=customer_id, reason=str(exc))
        return False
    _log_event("payment.succeeded", correlation_id=correlation_id,
               customer_id=customer_id)
    return True
```

**Verify it** [RFC A.1.4]: failure-path observability — grep for `except` blocks that return without logging; the ✅ version has none.

**Grounding:** OWASP Logging Cheat Sheet; CWE-778 (Insufficient Logging).

---

## Trustworthiness

*"Ability to meet stakeholder expectations in a verifiable way"* [RFC §3.2.2, ISO-5723] — security properties that can be demonstrated rather than assumed.

### 5. Confidentiality

*"Property that information is not made available or disclosed to unauthorized individuals, entities, or processes"* [RFC §3.2.2.1, ISO-27000 §3.10].

```python
# ❌ Without Confidentiality
# Passwords are stored -- and compared -- in plaintext. A single read of
# the user store (leak, backup exposure, SQL injection, insider) fully
# compromises every user's credential, here and on every site where it
# was reused.

# --- in-memory stand-in so the example runs as-is ---------------------------
_USERS: dict[str, str] = {}   # username -> plaintext password (!)
# ----------------------------------------------------------------------------


def save_user(username: str, password: str) -> None:
    _USERS[username] = password


def verify_password(username: str, password: str) -> bool:
    return _USERS.get(username) == password
```

```python
# ✅ With Confidentiality
# Per the OWASP Password Storage Cheat Sheet, the password is never stored
# or compared in plaintext. A per-user salt plus a slow, memory-hard KDF
# makes offline brute-forcing impractical even if the store is exposed.
#
# Parameters matter: the cheat sheet's minimum work factor for scrypt is
# N=2^17 (128 MiB), r=8, p=1 -- weaker settings (e.g. N=2^14) are CWE-916
# territory. The stdlib enforces a memory cap, so maxmem must be raised
# above 128*N*r bytes or the call fails. (Argon2id is the cheat sheet's
# first choice; scrypt is used here because it ships in the standard
# library. Expect ~1 second and ~128 MiB per hash -- that cost is the
# point.)
import hashlib
import hmac
import os

_SCRYPT_N, _SCRYPT_R, _SCRYPT_P = 2**17, 8, 1
_SCRYPT_MAXMEM = 2**27 + 2**21          # > 128 * N * r bytes, plus overhead

# --- in-memory stand-in so the example runs as-is ---------------------------
_USERS: dict[str, tuple[bytes, bytes]] = {}   # username -> (salt, derived key)
# ----------------------------------------------------------------------------


def _derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"), salt=salt,
        n=_SCRYPT_N, r=_SCRYPT_R, p=_SCRYPT_P, maxmem=_SCRYPT_MAXMEM,
    )


def save_user(username: str, password: str) -> None:
    salt = os.urandom(16)
    _USERS[username] = (salt, _derive_key(password, salt))


def verify_password(username: str, password: str) -> bool:
    record = _USERS.get(username)
    if record is None:
        return False
    salt, expected = record
    return hmac.compare_digest(_derive_key(password, salt), expected)  # constant-time
```

**Verify it** [RFC A.2.1]: ask "if the user store leaks, what does the attacker hold?" — plaintext credentials in the ❌ version; per-user salts and memory-hard hashes in the ✅ version.

**Grounding:** OWASP Password Storage Cheat Sheet; CWE-256 (Plaintext Storage of a Password), CWE-916 (Password Hash With Insufficient Computational Effort).

---

### 6. Accountability

*"The property that every action taken within a system can be attributed to a specific, identified entity"* [RFC §3.2.2.2] — its core focus is *unique and verifiable* attribution.

```python
# ❌ Without Accountability
# The action happens, but nothing records *who* performed it. If a
# customer's balance is wrongly adjusted, there is no way to trace it back
# to an actor for investigation or dispute resolution.
import sqlite3

# --- in-memory stand-in so the example runs as-is ---------------------------
conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE accounts (id TEXT PRIMARY KEY, balance_cents INTEGER NOT NULL);
    INSERT INTO accounts VALUES ('acct-1', 10000);
""")
# ----------------------------------------------------------------------------


def adjust_balance(account_id: str, amount_cents: int) -> None:
    with conn:
        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents + ? WHERE id = ?",
            (amount_cents, account_id),
        )
```

```python
# ✅ With Accountability
# Two things make the attribution *verifiable*, not just present:
#  1. The actor is taken from a server-verified AuthenticatedSession
#     (established as in example 7), never from a caller-supplied string --
#     an audit trail of unverified claims is a trail of potential lies.
#  2. The action and its audit record commit in ONE transaction: there is
#     no code path where the balance changes without an attributable
#     record. (In production, enforce append-only at the database layer --
#     the audit role gets INSERT, not UPDATE/DELETE.)
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

# --- in-memory stand-in so the example runs as-is ---------------------------
conn = sqlite3.connect(":memory:")
conn.executescript("""
    CREATE TABLE accounts (id TEXT PRIMARY KEY, balance_cents INTEGER NOT NULL);
    CREATE TABLE audit_log (
        at TEXT NOT NULL,
        actor_id TEXT NOT NULL,
        action TEXT NOT NULL,
        target TEXT NOT NULL,
        amount_cents INTEGER NOT NULL,
        reason TEXT NOT NULL
    );
    INSERT INTO accounts VALUES ('acct-1', 10000);
""")
# ----------------------------------------------------------------------------


@dataclass(frozen=True)
class AuthenticatedSession:      # identity verified server-side, as in example 7
    user_id: str
    role: str


def adjust_balance(
    account_id: str, amount_cents: int, session: AuthenticatedSession, reason: str
) -> None:
    with conn:  # one transaction: the change and its attribution are atomic
        conn.execute(
            "UPDATE accounts SET balance_cents = balance_cents + ? WHERE id = ?",
            (amount_cents, account_id),
        )
        conn.execute(
            "INSERT INTO audit_log VALUES (?, ?, ?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(),
                session.user_id,          # who -- a verified principal
                "balance.adjusted",       # what
                account_id,               # on what target
                amount_cents,             # by how much
                reason,                   # why
            ),
        )
```

**Verify it** [RFC A.2.2]: traceability success rate — pick any balance change at random; can you name the verified actor, target, amount, time, and reason? In the ✅ version the schema makes "yes" structural.

**Grounding:** RFC §2.6.3 (immutable audit trails: who, what, where, when, why); OWASP Logging Cheat Sheet (security event logging); CWE-778 (Insufficient Logging).

---

### 7. Authenticity

*"The property that an entity is what it claims to be"* [RFC §3.2.2.3, ISO-27000]. The attribute is about *verifying identity claims*. Note: SSEM deliberately has **no Authorization attribute** — the RFC's "On Authorization" callout classifies authorization as a security feature built *on top of* authenticated identity. This example therefore centers on identity verification, not role checks.

```python
# ❌ Without Authenticity
# Identity is whatever the client claims it is: a header any caller can
# type. Nothing verifies the entity is what it claims to be, so any user
# can impersonate any other user by editing one string (CWE-290). This is
# the Isolated Integrity Principle (RFC §4.4.1.2) violated for the most
# integrity-critical value there is: who is acting.

# --- in-memory stand-in so the example runs as-is ---------------------------
_MESSAGES = {"alice": ["meet at 10"], "bob": ["invoice attached"]}
# ----------------------------------------------------------------------------


def get_current_user(request: dict) -> str:
    return request["headers"]["X-User-Id"]    # trusted as-is. Why not lie?


def read_messages(request: dict) -> list[str]:
    user_id = get_current_user(request)
    return _MESSAGES.get(user_id, [])
```

```python
# ✅ With Authenticity
# Identity is *proven*, not claimed: the caller presents a token only the
# server could have produced (HMAC-signed), and verification fails closed.
# The mechanics are shown inline so the example runs; production systems
# should use a vetted session framework or token library with a pinned
# algorithm, plus expiry, rotation, and revocation (RFC §3.2.2.3's
# credential-lifecycle guidance).
import base64
import binascii
import hashlib
import hmac
from dataclasses import dataclass

_SIGNING_KEY = b"demo-key: load from a secret store, never hardcode"

# --- in-memory stand-in so the example runs as-is ---------------------------
_MESSAGES = {"alice": ["meet at 10"], "bob": ["invoice attached"]}
# ----------------------------------------------------------------------------


class InvalidToken(Exception):
    pass


@dataclass(frozen=True)
class AuthenticatedSession:
    user_id: str


def issue_token(user_id: str) -> str:
    payload = user_id.encode("utf-8")
    signature = hmac.new(_SIGNING_KEY, payload, hashlib.sha256).digest()
    return (base64.urlsafe_b64encode(payload).decode()
            + "." + base64.urlsafe_b64encode(signature).decode())


def verify_token(token: str) -> AuthenticatedSession:
    try:
        payload_b64, signature_b64 = token.split(".")
        payload = base64.urlsafe_b64decode(payload_b64)
        signature = base64.urlsafe_b64decode(signature_b64)
    except (ValueError, binascii.Error) as exc:
        raise InvalidToken("malformed token") from exc          # fail closed
    expected = hmac.new(_SIGNING_KEY, payload, hashlib.sha256).digest()
    if not hmac.compare_digest(signature, expected):
        raise InvalidToken("signature mismatch")                # fail closed
    return AuthenticatedSession(user_id=payload.decode("utf-8"))


def read_messages(token: str) -> list[str]:
    session = verify_token(token)     # identity proven, or no data at all
    # Any role/permission check would go here -- authorization, a separate
    # feature that DEPENDS on this verified identity (RFC §3.2.2.3 callout).
    return _MESSAGES.get(session.user_id, [])
```

**Verify it** [RFC A.2.3]: authentication mechanism coverage — can any request path reach user data without passing `verify_token`? In the ✅ version, no; and the failure path (the `InvalidToken` branches) is where the attribute is actually enforced.

**Grounding:** OWASP Session Management Cheat Sheet; CWE-290 (Authentication Bypass by Spoofing); Isolated Integrity Principle [RFC §4.4.1.2] — "a user's role or permission level must be loaded from a server-side session or database, not passed in a client request."

---

## Reliability

*"The degree to which a system, product or component performs specified functions under specified conditions for a specified period of time"* [RFC §3.2.3, ISO-25010] — consistent, predictable operation under adverse conditions, unexpected inputs, or attack.

### 8. Availability

*"Property of being accessible and usable on demand by an authorized entity"* [RFC §3.2.3.1, ISO-27000 §3.7] — including under adverse circumstances such as DoS conditions.

```python
# ❌ Without Availability
# No deadline and no bound on concurrent work. Every request that hits a
# stuck upstream parks a worker forever; under normal traffic the pool
# drains in seconds and the WHOLE service is down -- a self-inflicted
# denial of service triggered by one slow dependency.

# --- stand-in for a stuck upstream so the example runs as-is ----------------
import time

def _http_get(url: str) -> dict:
    time.sleep(3600)          # the dependency has stalled; this never returns
    return {"rate": 1.0}      # (define, don't call, unless you have an hour)
# ----------------------------------------------------------------------------


def fetch_exchange_rate(currency: str) -> float:
    response = _http_get(f"https://rates.example.com/{currency}")
    return response["rate"]
```

```python
# ✅ With Availability
# The two failure modes above get matching fixes:
#  * A hard DEADLINE: a stuck upstream costs at most 2 seconds, not a
#    worker forever.
#  * A BULKHEAD (bounded concurrency): at most N calls are in flight to
#    this dependency; request N+1 is shed fast with a typed error instead
#    of queueing without bound. The semaphore makes the bound thread-safe
#    by construction.
# (Inbound rate limiting / throttling is a complementary availability
# measure the RFC files under architecture, §5.1. The bulkhead is what
# prevents worker exhaustion.)
import threading

_MAX_CONCURRENT_UPSTREAM_CALLS = 8
_upstream_slots = threading.BoundedSemaphore(_MAX_CONCURRENT_UPSTREAM_CALLS)


class ServiceBusy(Exception):
    """Shed load: reject promptly instead of queueing without bound."""


# --- stand-in for a responsive HTTP client so the example runs as-is --------
def _http_get(url: str, timeout_seconds: float) -> dict:
    return {"rate": 1.0}      # a real client enforces timeout_seconds
# ----------------------------------------------------------------------------


def fetch_exchange_rate(currency: str) -> float:
    if not _upstream_slots.acquire(blocking=False):
        raise ServiceBusy("exchange-rate dependency saturated; retry shortly")
    try:
        response = _http_get(
            f"https://rates.example.com/{currency}", timeout_seconds=2.0
        )
        return response["rate"]
    finally:
        _upstream_slots.release()
```

**Verify it** [RFC A.3.1]: performance under stress — load-test with the dependency artificially stalled; the service should keep answering (fast failures for this endpoint, normal service elsewhere) instead of exhausting its workers.

**Grounding:** OWASP Denial of Service Cheat Sheet; CWE-400 (Uncontrolled Resource Consumption).

---

### 9. Integrity

*"Property of accuracy and completeness"* [RFC §3.2.3.2, ISO-27000 §3.36]. SSEM applies it at two levels — system integrity and data integrity; this example shows the data/business-logic side, where the RFC's own worked example lives.

```python
# ❌ Without Integrity
# The price is taken from the client's own request at checkout, so any
# tampering with the request body directly changes what the customer pays
# (CWE-602). Quantity is not validated either: quantity=-3 produces a
# NEGATIVE total -- a refund exploit. The system has adopted the unknown
# integrity of client-supplied data for its most integrity-critical facts.


def checkout(request: dict) -> int:
    return request["price_cents"] * request["quantity"]
```

```python
# ✅ With Integrity
# The Isolated Integrity Principle (RFC §4.4.1.2): the client expresses
# INTENT -- which item, how many -- and every integrity-critical fact is
# derived from authoritative server-side sources. Client input selects;
# it never dictates value. Canonical input handling (RFC §4.4.1) bounds
# what "how many" can even mean, closing the negative-total exploit.

# --- in-memory stand-in so the example runs as-is ---------------------------
_CATALOG_PRICE_CENTS = {"12345": 597}    # the server's source of truth
# ----------------------------------------------------------------------------

MAX_QUANTITY_PER_ITEM = 100


def checkout(request: dict) -> int:
    if "price_cents" in request or "price" in request:
        # A client trying to set a server-derived fact is probing, not
        # shopping. The RFC recommends log-or-reject at this boundary
        # (§4.4.1.1); in a payment flow, reject.
        raise ValueError("price is not a client-settable field")

    quantity = int(request["quantity"])
    if not 1 <= quantity <= MAX_QUANTITY_PER_ITEM:
        raise ValueError("quantity out of range")     # blocks quantity=-3

    price_cents = _CATALOG_PRICE_CENTS.get(request["item_id"])
    if price_cents is None:
        raise LookupError("unknown item")

    return price_cents * quantity     # exact integer arithmetic: no float drift
```

**Verify it** [RFC A.3.2]: input validation effectiveness at the trust boundary — attempt `quantity=-3`, `quantity=10**9`, and a request carrying `price_cents`; all three must be rejected, and the rejections logged.

**Grounding:** Isolated Integrity Principle [RFC §4.4.1.2] (this is the RFC's own checkout example, made concrete); CWE-602 (Client-Side Enforcement of Server-Side Security), CWE-20 (Improper Input Validation); OWASP Input Validation Cheat Sheet.

---

### 10. Resilience

*"The ability of a system to continue operating during and after the failure of one or more of its parts, and to recover from that failure and restore full operations"* [RFC §3.2.3.3].

Division of labor with example 8: **Availability** keeps the system responsive *while* a dependency misbehaves (deadlines, bulkheads, load shedding); **Resilience** absorbs the failure and recovers (retries, fallbacks, restoration).

```python
# ❌ Without Resilience
# A single failed call to a downstream service propagates as an unhandled
# exception -- no retry, no fallback. One transient hiccup in a
# nice-to-have dependency takes down the whole request path.
import random

# --- stand-in for a flaky dependency so the example runs as-is --------------
class RecommendationServiceError(Exception):
    pass

class _FlakyRecommendationService:
    def fetch(self, user_id: str) -> list[str]:
        if random.random() < 0.7:                      # transient failures
            raise RecommendationServiceError("temporarily unavailable")
        return ["rec-1", "rec-2"]

recommendation_service = _FlakyRecommendationService()
# ----------------------------------------------------------------------------


def get_recommendations(user_id: str) -> list[str]:
    return recommendation_service.fetch(user_id)
```

```python
# ✅ With Resilience
# Bounded retries with jittered exponential backoff absorb transient
# failures; a fallback keeps the system usable -- degraded, but operating.
# Degradation is graceful but never SILENT: the fallback emits a signal
# (failure-path observability, RFC A.1.4 -- example 4's lesson applies to
# recovery paths too).
import logging
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("recommendations")

# --- stand-in for a flaky dependency so the example runs as-is --------------
class RecommendationServiceError(Exception):
    pass

class _FlakyRecommendationService:
    def fetch(self, user_id: str) -> list[str]:
        if random.random() < 0.7:                      # transient failures
            raise RecommendationServiceError("temporarily unavailable")
        return ["rec-1", "rec-2"]

recommendation_service = _FlakyRecommendationService()
# ----------------------------------------------------------------------------


def get_recommendations(user_id: str, max_retries: int = 3) -> list[str]:
    delay = 0.2
    for attempt in range(1, max_retries + 1):
        try:
            return recommendation_service.fetch(user_id)
        except RecommendationServiceError as exc:
            if attempt == max_retries:
                logger.warning(
                    "recommendations degraded to empty list: "
                    "user_id=%s attempts=%d reason=%s", user_id, attempt, exc,
                )
                return []      # graceful degradation -- and it left a trace
            # Jitter prevents synchronized retry stampedes against a
            # dependency that is already struggling. Keep the total retry
            # budget under the caller's own deadline (see example 8).
            time.sleep(delay + random.uniform(0, delay))
            delay *= 2
    return []
    # Next step at system scale: a circuit breaker, so repeated failures
    # stop the calls entirely for a cooldown period instead of retrying
    # into a known-down dependency.
```

**Verify it** [RFC A.3.3]: simulate dependency failure — the request path must return a degraded-but-valid result within its deadline, and the degradation must appear in telemetry (error/recovery signals present).

**Grounding:** OWASP Error Handling Cheat Sheet; CWE-755 (Improper Handling of Exceptional Conditions); RFC §3.2.1.4 ("Resilience through error and recovery telemetry").

---

## References

- OWASP FIASSE RFC — [Securable Software Engineering Model, §3.1–3.2](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md#31-model-overview-and-design-language); [Appendix A: Measuring SSEM Attributes](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md#appendix-a-measuring-ssem-attributes)
- FIASSE Core Principle — [The Isolated Integrity Principle, §4.4.1.2](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md#4412-the-isolated-integrity-principle) (examples 7 and 9)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Denial of Service Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
- CWE references: [CWE-20](https://cwe.mitre.org/data/definitions/20.html), [CWE-256](https://cwe.mitre.org/data/definitions/256.html), [CWE-290](https://cwe.mitre.org/data/definitions/290.html), [CWE-307](https://cwe.mitre.org/data/definitions/307.html), [CWE-400](https://cwe.mitre.org/data/definitions/400.html), [CWE-602](https://cwe.mitre.org/data/definitions/602.html), [CWE-755](https://cwe.mitre.org/data/definitions/755.html), [CWE-778](https://cwe.mitre.org/data/definitions/778.html), [CWE-916](https://cwe.mitre.org/data/definitions/916.html), [CWE-1041](https://cwe.mitre.org/data/definitions/1041.html), [CWE-1120](https://cwe.mitre.org/data/definitions/1120.html)
