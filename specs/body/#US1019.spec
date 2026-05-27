# service-code: #US1019
# endpoint:     /customer/close-account-amt-cal
# category:     US
# section:      4.31
# program:      LHBSU19S
#
# #US1019 - generated from CTBCLH60 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                     8    # M A  Echo from request msg
status                           1    # M A  S=success, F=failed
accountNumber                   19    # M A
amount                          13    # M N  total payoff amount
LOC_end                          4    # M A  Value #LOC

