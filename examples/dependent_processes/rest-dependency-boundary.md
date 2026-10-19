# A called process at a trust boundary

A dependency the team calls sits across a trust boundary (Section 4.3). Its
behavior changes when its operator decides, not when the team takes a new
version. Here the integration is written twice: a checkout service calling a
remote tax and pricing service over REST, first with the response threaded
through the caller's internals, then with it stopped at a boundary the caller
owns.

Both are code a competent software engineer writes. What mostly separates them
is coupling, and one defect rides along with it. I wrote the before version
first, and every later change to it made it more defensible rather than less,
because an example whose before version would not survive review proves
nothing. This example is written to Section 4.5, for the kind of dependency a
team calls rather than the kind it takes into its build.

The Isolated Integrity Principle (Section 4.4.1.2) uses a checkout where a
server refuses to let a client dictate the price. This is the same counter seen
from the other end of the wire: a caller refusing to let a callee dictate what
it accepts. The parse that makes the refusal possible is the Canonical Parsing
Principle (Section 4.4.1.1) pointed outward, because a response is input
arriving at a boundary.

Section 4.4.1.2 already splits authority fact by fact: the client is trusted
for which item and how many, and not for the price. What the framework does not
name is the direction taken here, where the party on the far side of the
boundary is the system of record for one of the facts in the exchange.

Ground rules, matching the existing code examples: Python 3.10 or later,
standard library only, money in integer cents, and the response's number fields
arrive as JSON integers. The transport is reduced to a function taking a
request and returning a response, since what is at issue is what the caller
does with the answer. The three blocks below are one file and run in order, so
each block imports what it needs where it needs it.

## Before

```python
from collections.abc import Callable

CATALOG_CENTS = {"SKU-1": 2475}


class SaleRefused(Exception):
    """The order does not complete."""


class CoupledCheckout:
    def __init__(self, post: Callable[[dict], dict]) -> None:
        self._post = post

    def place_order(self, sku: str, quantity: int, destination: str) -> dict:
        quote = self._quote(sku, quantity, destination)
        if not quote.get("sale_permitted", True):
            raise SaleRefused(f"not sold into {destination}")
        order = dict(quote)
        order["sku"] = sku
        order["quantity"] = quantity
        order["total_cents"] = quote["line_subtotal_cents"] + quote["tax_cents"]
        return order

    def _quote(self, sku: str, quantity: int, destination: str) -> dict:
        request = {"sku": sku, "quantity": quantity,
                   "unit_price_cents": CATALOG_CENTS[sku], "to": destination}
        try:
            return self._post(request)
        except Exception:
            # Keep checkout moving while the tax service is unavailable.
            return {"line_subtotal_cents": CATALOG_CENTS[sku] * quantity,
                    "tax_jurisdiction": "UNKNOWN", "tax_cents": 0}

    def receipt_line(self, order: dict) -> str:
        return f"tax {order['tax_cents']} in {order['tax_jurisdiction']}"
```

The response becomes the order, with the caller's own `sku` and `quantity`
written in over the copy, so the far side's vocabulary is now the caller's and
everything else it sends is carried on to whatever reads the order next. The
subtotal arrives in the response even though the caller could derive it from
its own catalog, and even though the request it answers carried the unit price
out. A real system has the far side's field names everywhere an order is
touched; here they are written and read across three of this class's four
methods, so replacing the dependency is not a local change.

Nothing records which parts of the response the caller depends on. That
knowledge is the set of keys the code happens to touch, recoverable only by
reading every method that touches the order. The response is never checked for
shape either. If the far side starts sending its refusal as the text "false"
instead of as a boolean, a change that ships on its own schedule, nothing here
could notice.

The fallback is the part most likely to be defended in review. Charging no tax
while the tax service is unavailable is a real decision and may be the right
one. Two things ride along with it that nobody chose. The sale completes,
because the fallback carries no permission field and a default answered that
question. And a jurisdiction no authority issued reaches the order record and
the customer's receipt.

## After

```python
import logging
import re
from dataclasses import dataclass

_log = logging.getLogger(__name__)

# The recorded reliance: what the far side sends, and in what form.
RELIED_ON = {"tax_cents": int, "tax_jurisdiction": str, "sale_permitted": bool}
# The shape of a destination this caller sends. Whether a sale is permitted
# into one is the far side's answer and not this.
DESTINATION = re.compile(r"[A-Z]{2}-[A-Z]{2}")


class QuoteUnavailable(Exception):
    """The far side answered with something this caller cannot use."""


@dataclass(frozen=True)
class TaxQuote:
    tax_cents: int
    tax_jurisdiction: str
    sale_permitted: bool


@dataclass(frozen=True)
class Order:
    sku: str
    quantity: int
    subtotal_cents: int
    tax_cents: int
    tax_jurisdiction: str
    total_cents: int


def parse_quote(payload: object) -> TaxQuote:
    # Any mapping will do for the envelope. The fields are stricter, because
    # there the exact type carries meaning.
    if not isinstance(payload, dict):
        raise QuoteUnavailable(f"quote arrived as {type(payload).__name__}")
    taken: dict = {}
    for name, expected in RELIED_ON.items():
        if name not in payload:
            raise QuoteUnavailable(f"quote omitted {name}")
        value = payload[name]
        # Type identity and not isinstance: in Python a bool is an int, and a
        # subclass is not the shape that was agreed.
        if type(value) is not expected:
            raise QuoteUnavailable(f"quote sent {name} as {type(value).__name__}")
        taken[name] = value
    # A type is not the whole shape, and what this caller accepts is its own.
    if taken["tax_cents"] < 0:
        raise QuoteUnavailable("quote sent a negative tax_cents")
    if not taken["tax_jurisdiction"]:
        raise QuoteUnavailable("quote sent an empty tax_jurisdiction")
    ignored = sorted(k for k in payload if k not in RELIED_ON)
    if ignored:
        _log.info("tax quote carried fields not relied on: %s", ignored)
    return TaxQuote(
        tax_cents=taken["tax_cents"],
        tax_jurisdiction=taken["tax_jurisdiction"],
        sale_permitted=taken["sale_permitted"],
    )


class BoundedCheckout:
    def __init__(self, post: Callable[[dict], object]) -> None:
        self._post = post

    def place_order(self, sku: str, quantity: int, destination: str) -> Order:
        # The caller's own door is a boundary too.
        if type(quantity) is not int or quantity < 1:
            raise SaleRefused(f"quantity {quantity!r} is not a whole positive number")
        if sku not in CATALOG_CENTS:
            raise SaleRefused(f"no catalog entry for {sku!r}")
        if type(destination) is not str or not DESTINATION.fullmatch(destination):
            raise SaleRefused(f"{destination!r} is not one this caller sends")
        # Ours.
        subtotal_cents = CATALOG_CENTS[sku] * quantity
        quote = self._quote(sku, quantity, destination)
        if not quote.sale_permitted:
            raise SaleRefused(f"not sold into {destination}")
        # A bound stated from a figure this caller owns. Refusing an
        # implausible answer is not recomputing it.
        if quote.tax_cents > subtotal_cents:
            _log.warning("tax quote refused for %s into %s: tax over subtotal",
                         sku, destination)
            raise QuoteUnavailable(f"quoted tax {quote.tax_cents} exceeds subtotal")
        return Order(
            sku=sku,
            quantity=quantity,
            subtotal_cents=subtotal_cents,
            # Theirs.
            tax_cents=quote.tax_cents,
            tax_jurisdiction=quote.tax_jurisdiction,
            total_cents=subtotal_cents + quote.tax_cents,
        )

    def _quote(self, sku: str, quantity: int, destination: str) -> TaxQuote:
        request = {"sku": sku, "quantity": quantity,
                   "unit_price_cents": CATALOG_CENTS[sku], "to": destination}
        try:
            payload = self._post(request)
        except Exception as exc:
            # This response also answers whether the sale is permitted.
            _log.warning("no tax quote for %s into %s", sku, destination)
            raise SaleRefused("no quote, so the sale is not permitted") from exc
        try:
            return parse_quote(payload)
        except QuoteUnavailable as exc:
            _log.warning("tax quote refused for %s into %s: %s",
                         sku, destination, exc)
            raise

    def receipt_line(self, order: Order) -> str:
        return f"tax {order.tax_cents} in {order.tax_jurisdiction}"
```

`RELIED_ON` and `parse_quote` are the only place the shape of the far side's
response is known. The request vocabulary sits in `_quote`, so both directions
of the exchange are described in one declaration and two functions and nowhere
else. `place_order` never reads a field out of a response.

`RELIED_ON`, `TaxQuote`, and the keyword arguments between them are not one
declaration written three times. `RELIED_ON` says what the far side sends;
`TaxQuote` says what this caller holds; the keywords are the mapping. That
mapping is what lets the far side rename a field without the rename reaching
`Order` or the receipt. Both types are frozen because a record that can be
edited after it is built gives the far side's answer a second chance to change,
from inside this time.

`RELIED_ON` is a dict of names to shapes because the ground rules here are
standard library only. Where a codebase already carries a schema library, the
reliance belongs in the model instead, and at more than a handful of fields it
has to. What survives the change of tool is that the list exists at all, and
that one function owns it.

The parse refuses rather than converts. A refusal arriving as the text "false"
is a change in the far side's behavior, and converting it into something usable
would let the far side decide what this caller accepts. The boundary takes the
shape it agreed to, down to whether a mapping arrived in place of the response
at all, and refuses anything else. It refuses on value too: a negative tax
figure, and a tax larger than the subtotal the caller derived. A bound stated
from a figure the caller owns is not a recomputation of the far side's figure.
The messages these exceptions carry name the far side's fields, which is
diagnostic detail for this caller's own logs, not a message returned to an
untrusted party.

A field the far side adds is ignored rather than rejected, and logged rather
than passed over in silence. Section 4.4.1.1 leaves that choice to the
engineer. For a response from a known operator, ignoring is reasonable; for a
request from an unknown client the same section argues the other way. The
choice is stated here because the section asks that it not be left as an
implicit default.

The rule has two halves: derive what you are the authority for, and take what
you are not. `subtotal_cents` is derived from the caller's own catalog, and the
response's version is not read at all. `tax_cents` is taken as it came and not
recomputed from a local rate table, because the far side is the system of
record and a local recomputation would make this caller a second authority for
someone else's fact. Taking only the first half argues for a caller enforcing
decisions it has no standing to make.

`quantity`, `sku`, and `destination` arrive from somewhere too, and the after
version parses all three before computing with them or sending them on, for the
same reason it parses the response. An unknown `sku` would otherwise reach the
catalog as a dictionary lookup and leave as a `KeyError` raised from inside this
caller's own pricing. `destination` would otherwise go out exactly as it
arrived, into a request the far side then has to parse. Which destinations may
be sold into is still the far side's answer; the shape this caller is willing to
send is its own. The before version computes with `quantity` only in its
fallback, and reads the answer otherwise.

One cost is left standing. An outage and a policy refusal leave this boundary
as the same exception type, so an upstream caller has to read the message or
the cause to learn whether retrying would help, instead of switching on the
outcome.

## The tests

```python
import unittest

BASE_QUOTE = {
    "line_subtotal_cents": 4950,
    "tax_cents": 408,
    "tax_jurisdiction": "WA-KING",
    "sale_permitted": True,
}
PURCHASE = ("SKU-1", 2, "US-WA")


def answering(payload: dict) -> Callable[[dict], dict]:
    """A far side that answers. The seam both callers are exercised through."""
    def post(request: dict) -> dict:
        return dict(payload)
    return post


def silent(request: dict) -> dict:
    raise TimeoutError("the tax service did not answer")


def not_an_object(request: dict) -> object:
    """A far side that answers with something that is not an object at all."""
    return None


class CouplingContrast(unittest.TestCase):

    # Property: what the caller relies on is written down in one place, so
    # what the far side adds does not become part of the caller's own record.
    def test_what_the_far_side_adds(self):
        widened = dict(BASE_QUOTE, promotion_campaign="SUMMER",
                       sku="SKU-CHEAP", quantity=99)
        coupled = CoupledCheckout(answering(widened))
        carried = coupled.place_order(*PURCHASE)
        self.assertIn("promotion_campaign", carried)
        self.assertEqual((carried["sku"], carried["quantity"]), ("SKU-1", 2))
        bounded = BoundedCheckout(answering(widened))
        wide_order = bounded.place_order(*PURCHASE)
        self.assertEqual(wide_order,
                         BoundedCheckout(answering(BASE_QUOTE)).place_order(*PURCHASE))
        # The same line, read from the far side's names in one and from the
        # caller's own type in the other.
        self.assertEqual(coupled.receipt_line(carried), "tax 408 in WA-KING")
        self.assertEqual(bounded.receipt_line(wide_order), "tax 408 in WA-KING")

    # Property: a relied-on field that stops arriving, or that arrives in a
    # shape the caller never agreed to, is a decided outcome at the boundary.
    def test_what_the_far_side_changes(self):
        narrowed = {k: v for k, v in BASE_QUOTE.items() if k != "tax_cents"}
        with self.assertRaises(KeyError):
            CoupledCheckout(answering(narrowed)).place_order(*PURCHASE)
        with self.assertRaises(QuoteUnavailable) as omitted:
            BoundedCheckout(answering(narrowed)).place_order(*PURCHASE)
        self.assertIn("tax_cents", str(omitted.exception))
        restyled = dict(BASE_QUOTE, sale_permitted="false")
        carried = CoupledCheckout(answering(restyled)).place_order(*PURCHASE)
        self.assertEqual(carried["total_cents"], 5358)
        # Each of these is a change the caller never agreed to, in shape, in
        # type, or in value. The coupled version has nowhere to notice any.
        for changed in (restyled,
                        dict(BASE_QUOTE, tax_jurisdiction=53033),
                        dict(BASE_QUOTE, tax_cents=-500),
                        dict(BASE_QUOTE, tax_cents=999_999_999),
                        dict(BASE_QUOTE, tax_jurisdiction="")):
            with self.assertRaises(QuoteUnavailable):
                BoundedCheckout(answering(changed)).place_order(*PURCHASE)
        with (self.assertLogs(_log.name, level="WARNING") as logged,
              self.assertRaises(QuoteUnavailable)):
            BoundedCheckout(not_an_object).place_order(*PURCHASE)
        # The refusal is recorded against the call it answered.
        self.assertIn("SKU-1", logged.output[0])

    # Property: the caller derives the figure it is the authority for and takes
    # the figure the far side is the authority for, becoming a second authority
    # for neither of them.
    def test_who_each_figure_belongs_to(self):
        disagreeing = dict(BASE_QUOTE, line_subtotal_cents=1)
        coupled = CoupledCheckout(answering(disagreeing)).place_order(*PURCHASE)
        self.assertEqual(coupled["total_cents"], 409)
        bounded = BoundedCheckout(answering(disagreeing)).place_order(*PURCHASE)
        self.assertEqual(bounded.subtotal_cents, 4950)
        self.assertEqual(bounded.tax_cents, 408)
        self.assertEqual(bounded.total_cents, 5358)
        # A second quantity and a second jurisdiction, so that neither figure
        # can be a constant standing in for a derivation.
        elsewhere = dict(BASE_QUOTE, line_subtotal_cents=1, tax_cents=17,
                         tax_jurisdiction="OR-LANE")
        larger = BoundedCheckout(answering(elsewhere))
        order = larger.place_order("SKU-1", 3, "US-OR")
        self.assertEqual(order.subtotal_cents, 7425)
        self.assertEqual(order.tax_cents, 17)
        self.assertEqual(order.total_cents, 7442)
        self.assertEqual(larger.receipt_line(order), "tax 17 in OR-LANE")
        # What it derives from is parsed at the caller's own door. A checker
        # catches this one statically; the parse catches the ones it cannot see.
        with self.assertRaises(SaleRefused):
            BoundedCheckout(answering(BASE_QUOTE)).place_order(
                "SKU-1", 2.5, "US-WA")  # type: ignore[arg-type]

    # Property: where the dependency was answering what is permitted, an answer
    # that arrives is honored by both, and an answer that never arrives closes
    # the door only where losing it was decided.
    def test_the_far_side_says_nothing(self):
        refusing = dict(BASE_QUOTE, sale_permitted=False)
        for checkout in (CoupledCheckout(answering(refusing)),
                         BoundedCheckout(answering(refusing))):
            with self.assertRaises(SaleRefused):
                checkout.place_order(*PURCHASE)
        coupled = CoupledCheckout(silent)
        stranded = coupled.place_order(*PURCHASE)
        self.assertEqual(stranded["tax_cents"], 0)
        self.assertEqual(coupled.receipt_line(stranded), "tax 0 in UNKNOWN")
        with (self.assertLogs(_log.name, level="WARNING") as logged,
              self.assertRaises(SaleRefused)):
            BoundedCheckout(silent).place_order(*PURCHASE)
        self.assertIn("SKU-1", logged.output[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

Each test names a property and asserts it against both variants, so the
contrast is the assertion and not a claim made here. The fourth shows the two
agreeing while the far side speaks and diverging when it stops. That divergence
is a difference in property, not a defect: the before version does what its
author intended, and the intent covered availability without reaching
permission.

## Named against the model

`RELIED_ON` and `parse_quote` are Analyzability: what this system assumes about
the far side has an answer a reviewer can read, instead of one reassembled from
keys scattered through the caller. Both directions of the exchange living in
one declaration and two functions is Modifiability: replacing the dependency
does not reach `place_order`, `Order`, or the receipt. Every unusable answer is
logged with the call it answered, which is Observability. A sale the far side
declines is an answer rather than a deviation, and is not logged. The split
between the derived figure and the taken figure is Integrity read from the
calling side. Deciding what happens when the call is lost, and deciding it as a
question about what is permitted, is Resilience and Integrity again; Section
4.4's graceful and secure failure is the shape of it. Availability is what was
traded for them, deliberately.

Testability is the one attribute both versions already have. The transport is
passed in on both sides, which is why the contrast can be asserted in tests at
all.

Confidentiality is constructed in the same place the request is. `_quote` is
the only code that decides what leaves, and what leaves here includes the unit
price, which the after version still sends even though it no longer reads the
subtotal that comes back. This example does not vary that; that is where it
would be varied.
