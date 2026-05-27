# service-code: #US1020
# endpoint:     /customer/block-roll
# category:     US
# section:      5.4
# program:      LHBSU20S
#
# #US1020 - generated from CTBCLH55 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                    72    # M A  Echo request message
status                           1    # M A  S=success, F=failed
LOC_end                          4    # M A  Value #LOC

