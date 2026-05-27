# service-code: #US1010
# endpoint:     /customer/customer-block-code-set
# category:     US
# section:      4.17
# program:      LHBSU10S
#
# #US1010 - generated from CTBCLH39 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo                            70    # M A  Echo request message
status                           1    # M A  S=success, F=failed
errorCode                       10    # O A  populated when operation fails

