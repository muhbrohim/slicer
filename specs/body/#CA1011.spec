# service-code: #CA1011
# endpoint:     /card/card-issue
# category:     CA
# section:      4.23
# program:      LHBSC11S
#
# #CA1011 - generated from CTBCLH51 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo                            71
status                           1    # M A

