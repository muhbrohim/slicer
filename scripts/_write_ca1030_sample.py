"""Write the real #CA1030 sample message verbatim, preserving every space."""

from pathlib import Path

HEADER = (
    "ADSVADSV"            # HDR_TAG (8)
    "1"                   # HDR_SERVICE_TYPE (1)
    "#CA1030"             # service_code (7)
    + "MOBILE" + " " * 14  # HDR_CLIENT_ID (20)
    + "20260422"          # HDR_DATE (8)
    + "16272858"          # HDR_TIME (8)
    + "2026042216"        # HDR_JOB (10)
    + "272857"            # HDR_NBR (6)
    + "773481"            # HDR_TRACE (6)
    + "   "               # HDR_CLIENT_FILLER (3)
    + "000-"              # HDR_RSP_MAJOR (4)
    + "00  "              # HDR_RSP_MINOR (4)
    + "03726"             # HDR_DATA_LEN (5)
    + " " * 60            # HDR_FILLER (60)
    + "20260518"          # HDR_DATE_A (8)
    + "17482474"          # HDR_TIME_A (8)
    + "SCDS064S  "        # HDR_USER (10)
    + "SCUS060Q  "        # HDR_RTN_QUEUE (10)
    + " " * 34            # HDR_ASC_FILLER (34)
)
assert len(HEADER) == 220, len(HEADER)

RESPONSE_PREFIX = (
    "00"                  # resp_code (2)
    + "R"                 # key_type (1)
    + "1327"              # key_bank (4)
    + "1000000000000188"  # 16 chars of key_val
    + "   "               # padding to 19
)
assert len(RESPONSE_PREFIX) == 26, len(RESPONSE_PREFIX)

ECHO_BLOCK = (
    "20250923"            # echo_statementDate (8)
    + "2"                 # pageContinue (1)
    + "24024006010"       # referenceNumber (11)
    + "20250923"          # statementDate (8)
    + " " * 19            # cardNumberMask (19)
)
assert len(ECHO_BLOCK) == 47, len(ECHO_BLOCK)


def record(parts: list[tuple[str, int]]) -> str:
    out = "".join(v.ljust(n)[:n] for v, n in parts)
    assert len(out) == 148, (len(out), out)
    return out


R1 = record([
    ("C", 1),
    ("20250805", 8),
    ("000000", 6),
    ("000000000000", 12),
    ("THB", 3),
    ("0003", 10),
    ("Billed Retail Interest Credit Adjustment", 41),
    ("20250828", 8),
    ("000000003890", 12),
    ("THB", 3),
    ("00000000000", 11),
    ("", 12),         # retrievalRefNumber blank
    ("", 6),          # authCode blank
    ("0000", 4),      # mcc
    ("24050060039", 11),
])

R2 = record([
    ("C", 1),
    ("20250805", 8),
    ("000000", 6),
    ("000000000000", 12),
    ("THB", 3),
    ("0001", 10),
    ("Cash Payment (LHB YOU)", 41),
    ("20250828", 8),
    ("000000530000", 12),
    ("THB", 3),
    ("00000000000", 11),
    ("EW2026051201", 12),
    ("", 6),
    ("0000", 4),
    ("24024006010", 11),
])

EMPTY = record([
    ("", 1),
    ("", 8),
    ("000000", 6),
    ("000000000000", 12),
    ("", 3),
    ("", 10),
    ("", 41),
    ("", 8),
    ("000000000000", 12),
    ("", 3),
    ("", 11),
    ("", 12),
    ("", 6),
    ("", 4),
    ("", 11),
])

BODY = RESPONSE_PREFIX + ECHO_BLOCK + R1 + R2 + EMPTY * 8 + "#LOC"
assert len(BODY) == 1557, len(BODY)

MESSAGE = HEADER + BODY
assert len(MESSAGE) == 1777, len(MESSAGE)

out = Path(__file__).resolve().parent.parent / "sample_messages" / "ca1030_real.txt"
out.write_bytes(MESSAGE.encode("utf-8") + b"\n")
print(f"wrote {out}  ({len(MESSAGE)} chars)")
