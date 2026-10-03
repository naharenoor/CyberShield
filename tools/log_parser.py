from __future__ import annotations

import io
import json

import pandas as pd

SUPPORTED_EXTENSIONS = {".csv", ".json", ".txt"}


def parse_upload(raw: bytes, filename: str) -> pd.DataFrame:
    """Parse supported log formats into a DataFrame."""
    suffix = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError("Supported formats are CSV, JSON, and TXT.")

    if suffix == ".csv":
        frame = pd.read_csv(io.BytesIO(raw))
    elif suffix == ".json":
        payload = json.loads(raw.decode("utf-8"))
        if isinstance(payload, dict):
            payload = payload.get("events", [payload])
        if not isinstance(payload, list):
            raise ValueError("JSON must contain an object or a list of event objects.")
        frame = pd.json_normalize(payload)
    else:
        lines = [line.strip() for line in raw.decode("utf-8", errors="replace").splitlines() if line.strip()]
        frame = pd.DataFrame({"raw_event": lines})

    if frame.empty:
        raise ValueError("The uploaded file contains no records.")
    return frame.fillna("")


def summarize_events(frame: pd.DataFrame, max_rows: int = 150) -> str:
    """Create a bounded text summary to limit model input size."""
    sample = frame.head(max_rows)
    return (
        f"Total rows in file: {len(frame)}\n"
        f"Columns: {', '.join(map(str, frame.columns))}\n\n"
        f"Sample events (up to {max_rows} rows):\n{sample.to_csv(index=False)}"
    )
