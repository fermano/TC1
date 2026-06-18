def invoice_export_is_deliverable(metadata):
    return bool(metadata.get("release_watermark"))
