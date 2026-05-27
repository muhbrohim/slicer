# service-code: #US1002
# endpoint:     /customer/cs-customer-set
# category:     US
# section:      4.16
# program:      LHBSU02S
#
# #US1002 - generated from CTBCLH38 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
status                           1    # M A  S=success, F=failed

