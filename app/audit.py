from __future__ import annotations

from hashlib import sha256
import json
from typing import Any


def canonical_event(event: dict[str, Any]) -> str:
    return json.dumps(event, sort_keys=True, separators=(",", ":"), default=str)


def chained_hash(previous_hash: str, event: dict[str, Any]) -> str:
    payload = f"{previous_hash}|{canonical_event(event)}".encode("utf-8")
    return sha256(payload).hexdigest()


def append_audit(chain: list[dict[str, Any]], event: dict[str, Any]) -> dict[str, Any]:
    previous_hash = chain[-1]["audit_hash"] if chain else "GENESIS"
    record = dict(event)
    record["previous_hash"] = previous_hash
    record["audit_hash"] = chained_hash(previous_hash, event)
    chain.append(record)
    return record


def verify_chain(chain: list[dict[str, Any]]) -> bool:
    previous = "GENESIS"
    for record in chain:
        event = {k: v for k, v in record.items() if k not in {"previous_hash", "audit_hash"}}
        if record.get("previous_hash") != previous:
            return False
        expected = chained_hash(previous, event)
        if record.get("audit_hash") != expected:
            return False
        previous = expected
    return True
