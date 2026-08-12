"""Settlement-row selection used by the RC-69 package readout."""

READY_STATES = {"posted", "settled", "settled_final"}
PACKAGE_TYPES = {"settlement", "adjustment"}


def _normalize(value):
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _source_ref(manifest):
    return manifest.get("source_ref") or manifest.get("branch") or ""


def settlement_rows(events):
    """Return rows eligible for the RC-69 settlement package."""
    rows = []
    seen = set()

    for event in events:
        state = _normalize(event.get("state"))
        if state not in READY_STATES:
            continue

        package_type = _normalize(event.get("package_type"))
        if package_type not in PACKAGE_TYPES:
            continue

        key = (event.get("tenant_id"), event.get("settlement_id"), package_type)
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "tenant_id": event.get("tenant_id"),
                "settlement_id": event.get("settlement_id"),
                "package_type": package_type,
                "amount_cents": int(event.get("amount_cents") or 0),
            }
        )

    return rows


def manifest_identity(manifest):
    """Return a compact identity tuple for release-package provenance checks."""
    return {
        "artifact_id": manifest.get("artifact_id"),
        "source_ref": _source_ref(manifest),
        "source_sha": manifest.get("source_sha") or manifest.get("commit_sha"),
        "package_kind": _normalize(manifest.get("package_kind")),
    }


def is_release_candidate_manifest(manifest, expected_ref="release/rc-69"):
    identity = manifest_identity(manifest)
    return (
        identity["source_ref"] == expected_ref
        and identity["package_kind"] == "settlement"
        and bool(identity["source_sha"])
    )
