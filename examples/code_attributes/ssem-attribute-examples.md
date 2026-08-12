# SSEM Attribute Examples — "With" vs "Without"

> Closes/relates to [OWASP/FIASSE#14](https://github.com/OWASP/FIASSE/issues/14) — *"Contrast each attribute 'with' vs 'without' each attribute."*

This document provides one contrasting Python example per SSEM attribute (per the FIASSE RFC §2.1 model: **Maintainability**, **Trustworthiness**, **Reliability**). Each example is:

- Self-contained (standard library only, runnable as-is).
- Focused on the attribute in isolation — not a full application.
- Grounded in an existing OWASP reference where one applies (Cheat Sheet Series, ASVS, or a FIASSE core principle).

Language convention: `❌ Without <Attribute>` shows a version that lacks the attribute (and the concrete risk that follows), `✅ With <Attribute>` shows the same scenario engineered to have it.

---

## Maintainability

### 1. Analyzability

*The ability to quickly assess the impact of changes, diagnose issues, and identify what needs to be modified.*

```python
# ❌ Without Analyzability
# One function mixes input parsing, business rules, persistence, and
# notification. A reviewer cannot tell what a change to "discount rules"
# will touch without reading (and mentally executing) the whole function.
def process_order(data):
    if data.get("qty") and data["qty"] > 0:
        total = data["qty"] * data["price"]
        if data.get("coupon") == "VIP10":
            total = total * 0.9
        if data["customer"]["country"] == "US":
            total = total * 1.0825
        db_conn.execute(
            "INSERT INTO orders (customer, total) VALUES (?, ?)",
            (data["customer"]["id"], total),
        )
        if total > 500:
            send_email(data["customer"]["email"], "High value order placed")
    return total
```

```python
# ✅ With Analyzability
# Each concern is a named, single-purpose function. Impact of a change
# (e.g. "how is discount applied?") is localized to one small function,
# so a maintainer can reason about it without tracing the whole flow.
from dataclasses import dataclass


@dataclass(frozen=True)
class OrderRequest:
    quantity: int
    unit_price: float
    coupon_code: str | None
    customer_country: str


def apply_coupon(subtotal: float, coupon_code: str | None) -> float:
    return subtotal * 0.9 if coupon_code == "VIP10" else subtotal


def apply_tax(amount: float, country: str) -> float:
    return amount * 1.0825 if country == "US" else amount


def calculate_total(order: OrderRequest) -> float:
    subtotal = order.quantity * order.unit_price
    discounted = apply_coupon(subtotal, order.coupon_code)
    return apply_tax(discounted, order.customer_country)
```

---

### 2. Modifiability

*The ability to safely and quickly modify a system without causing defects or reducing quality or securability.*

```python
# ❌ Without Modifiability
# The password policy is duplicated in three places. Changing the
# minimum length requires finding and editing every copy — miss one
# and the system silently enforces inconsistent security rules.
def register_user(password: str) -> bool:
    return len(password) >= 8 and any(c.isdigit() for c in password)


def reset_password(password: str) -> bool:
    return len(password) >= 8 and any(c.isdigit() for c in password)


def admin_change_password(password: str) -> bool:
    return len(password) >= 6 and any(c.isdigit() for c in password)  # drifted!
```

```python
# ✅ With Modifiability
# The policy lives in exactly one place. Every caller depends on the
# same rule, so a single edit (e.g. raising the minimum length) is
# guaranteed to apply everywhere, consistently.
from dataclasses import dataclass


@dataclass(frozen=True)
class PasswordPolicy:
    min_length: int = 12
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

---

### 3. Testability

*The ability to verify that a system meets its requirements and is free of defects.*

```python
# ❌ Without Testability
# Business logic is entangled with I/O (system clock, database).
# A unit test cannot exercise "is this account locked out?" without
# a live database connection and without controlling wall-clock time.
import datetime


def is_account_locked(user_id: str) -> bool:
    row = db_conn.execute(
        "SELECT failed_attempts, last_failed_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    if row["failed_attempts"] >= 5:
        elapsed = datetime.datetime.utcnow() - row["last_failed_at"]
        return elapsed < datetime.timedelta(minutes=15)
    return False
```

```python
# ✅ With Testability
# Pure decision logic is separated from I/O. The lockout *rule* is a
# plain function of its inputs, so it can be unit tested with no
# database and no dependency on the real clock.
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class LoginState:
    failed_attempts: int
    last_failed_at: datetime | None


def is_locked_out(state: LoginState, now: datetime, threshold: int = 5,
                   cooldown: timedelta = timedelta(minutes=15)) -> bool:
    if state.failed_attempts < threshold or state.last_failed_at is None:
        return False
    return (now - state.last_failed_at) < cooldown


# Test example — no DB, no real clock required:
# def test_recent_lockout_blocks_login():
#     state = LoginState(failed_attempts=5, last_failed_at=datetime(2026, 1, 1, 12, 0))
#     now = datetime(2026, 1, 1, 12, 5)
#     assert is_locked_out(state, now) is True
```

---

### 4. Observability

*The degree to which the internal state of a system can be inferred from its external outputs.*

```python
# ❌ Without Observability
# Failures are swallowed silently. When a payment fails in production,
# there is no external signal — no log, no metric, no trace — that
# lets anyone infer what happened or why.
def charge_card(customer_id: str, amount: float) -> bool:
    try:
        payment_gateway.charge(customer_id, amount)
        return True
    except Exception:
        return False
```

```python
# ✅ With Observability
# Structured, contextual logging (per the OWASP Logging Cheat Sheet:
# no sensitive data such as full card numbers, but enough context to
# reconstruct "what happened") makes internal state inferable from
# the outside without attaching a debugger.
import logging
import uuid

logger = logging.getLogger("payments")


def charge_card(customer_id: str, amount: float) -> bool:
    correlation_id = str(uuid.uuid4())
    logger.info(
        "payment.attempt",
        extra={"correlation_id": correlation_id, "customer_id": customer_id, "amount": amount},
    )
    try:
        payment_gateway.charge(customer_id, amount)
    except PaymentGatewayError as exc:
        logger.error(
            "payment.failed",
            extra={"correlation_id": correlation_id, "customer_id": customer_id, "reason": str(exc)},
        )
        return False
    logger.info("payment.succeeded", extra={"correlation_id": correlation_id, "customer_id": customer_id})
    return True
```

---

## Trustworthiness

### 5. Confidentiality

*The ability to keep sensitive information secure and private.*

```python
# ❌ Without Confidentiality
# Passwords are stored in plaintext. A single database read (via a
# leak, backup exposure, or SQL injection) fully compromises every
# user's credentials.
def save_user(username: str, password: str) -> None:
    db_conn.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
```

```python
# ✅ With Confidentiality
# Per the OWASP Password Storage Cheat Sheet, the password is never
# stored or compared in plaintext. A per-user salt plus a slow,
# memory-hard KDF (scrypt) makes offline brute-forcing impractical
# even if the database is exposed.
import hashlib
import hmac
import os


def hash_password(password: str) -> tuple[bytes, bytes]:
    salt = os.urandom(16)
    derived = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return salt, derived


def verify_password(password: str, salt: bytes, expected: bytes) -> bool:
    candidate = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    return hmac.compare_digest(candidate, expected)  # constant-time comparison


def save_user(username: str, password: str) -> None:
    salt, hashed = hash_password(password)
    db_conn.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (username, hashed, salt),
    )
```

---

### 6. Accountability

*The ability to uniquely trace actions to the responsible entity.*

```python
# ❌ Without Accountability
# The action happens, but nothing records *who* performed it. If a
# customer's balance is wrongly adjusted, there is no way to trace
# it back to an actor for investigation or dispute resolution.
def adjust_balance(account_id: str, amount: float) -> None:
    db_conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (amount, account_id),
    )
```

```python
# ✅ With Accountability
# Every sensitive action is tied to a specific, authenticated actor
# and recorded in an append-only audit trail (who, what, when, on
# what target) — aligned with the OWASP Logging Cheat Sheet's
# guidance on security-relevant event logging.
import logging
from datetime import datetime, timezone

audit_logger = logging.getLogger("audit")


def adjust_balance(account_id: str, amount: float, actor_id: str, reason: str) -> None:
    db_conn.execute(
        "UPDATE accounts SET balance = balance + ? WHERE id = ?",
        (amount, account_id),
    )
    audit_logger.info(
        "balance.adjusted",
        extra={
            "actor_id": actor_id,
            "target_account_id": account_id,
            "amount": amount,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
```

---

### 7. Authenticity

*The ability to confirm the identity of a user or system.*

```python
# ❌ Without Authenticity
# The caller's claimed role is taken from client-supplied data and
# trusted directly — a textbook violation of FIASSE's Derived
# Integrity Principle. Any client can send "role": "admin".
def delete_document(request: dict) -> bool:
    if request["role"] == "admin":
        db_conn.execute("DELETE FROM documents WHERE id = ?", (request["doc_id"],))
        return True
    return False
```

```python
# ✅ With Authenticity
# Identity and role are *derived* from a server-verified session
# (e.g. a signed token validated against the authoritative session
# store), never from unmanaged client input — consistent with the
# Derived Integrity Principle and OWASP Session Management guidance.
@dataclass(frozen=True)
class AuthenticatedSession:
    user_id: str
    role: str


def get_authenticated_session(session_token: str) -> AuthenticatedSession:
    # Validated server-side against the session store / token signature —
    # the caller cannot influence this value.
    return session_store.verify(session_token)


def delete_document(session_token: str, doc_id: str) -> bool:
    session = get_authenticated_session(session_token)
    if session.role != "admin":
        return False
    db_conn.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    return True
```

---

## Reliability

### 8. Availability

*The ability of a system to remain accessible and operational when needed.*

```python
# ❌ Without Availability
# No timeout and no bound on concurrent work. A single slow or stuck
# upstream dependency can exhaust worker threads/connections and take
# the whole service down — a self-inflicted denial of service.
def fetch_exchange_rate(currency: str) -> float:
    response = http_client.get(f"https://rates.example.com/{currency}")
    return response.json()["rate"]
```

```python
# ✅ With Availability
# A bounded timeout and a simple rate limiter guarantee the system
# fails fast instead of hanging indefinitely, keeping it responsive
# even when a dependency misbehaves.
import time
from collections import deque

_recent_calls: deque[float] = deque(maxlen=100)


def rate_limited(max_calls: int, window_seconds: float) -> bool:
    now = time.monotonic()
    while _recent_calls and now - _recent_calls[0] > window_seconds:
        _recent_calls.popleft()
    if len(_recent_calls) >= max_calls:
        return False
    _recent_calls.append(now)
    return True


def fetch_exchange_rate(currency: str) -> float:
    if not rate_limited(max_calls=20, window_seconds=1.0):
        raise RuntimeError("rate limit exceeded, try again shortly")
    response = http_client.get(f"https://rates.example.com/{currency}", timeout=2.0)
    return response.json()["rate"]
```

---

### 9. Integrity

*The ability to ensure that a system's data is accurate and uncorrupted.*

```python
# ❌ Without Integrity
# The price is taken from the client's own request at checkout. Any
# tampering with the request body directly changes what the
# customer pays — the system trusts unmanaged external context for
# a critical decision.
def checkout(cart_item_id: str, client_price: float, quantity: int) -> float:
    return client_price * quantity
```

```python
# ✅ With Integrity
# The price is derived from the authoritative catalog on the server,
# never from client-supplied data — a direct application of FIASSE's
# Derived Integrity Principle. Client input is used only to *select*
# the item, not to determine its value.
def checkout(cart_item_id: str, quantity: int) -> float:
    catalog_price = catalog.get_authoritative_price(cart_item_id)  # server source of truth
    if catalog_price is None:
        raise ValueError("unknown item")
    return catalog_price * quantity
```

---

### 10. Resilience

*The ability to recover from failures and continue operating.*

```python
# ❌ Without Resilience
# A single failed call to a downstream service propagates as an
# unhandled exception with no retry and no fallback — one dependency
# hiccup takes down the whole request path.
def get_recommendations(user_id: str) -> list[str]:
    return recommendation_service.fetch(user_id)
```

```python
# ✅ With Resilience
# A bounded retry with backoff absorbs transient failures, and a
# graceful fallback keeps the system usable — degraded, but
# operating — when the dependency is unavailable.
import time


def get_recommendations(user_id: str, max_retries: int = 3) -> list[str]:
    delay = 0.2
    for attempt in range(max_retries):
        try:
            return recommendation_service.fetch(user_id)
        except RecommendationServiceError:
            if attempt == max_retries - 1:
                break
            time.sleep(delay)
            delay *= 2  # exponential backoff
    return []  # graceful degradation instead of a hard failure
```

---

## References

- OWASP FIASSE RFC — [Securable Software Engineering Model §2.1](https://github.com/OWASP/FIASSE/blob/main/docs/securable_framework.md)
- OWASP Password Storage Cheat Sheet
- OWASP Logging Cheat Sheet
- OWASP Session Management Cheat Sheet
- FIASSE Core Principle — *Derived Integrity Principle* (examples 7 and 9 above)
