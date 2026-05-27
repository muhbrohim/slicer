# service-code: #CA1027
# endpoint:     /card/perm-limit-set
# category:     CA
# section:      5.1
# program:      LHBSC27S
#
# #CA1027 - generated from CTBCLH46 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                  1435    # M A  Echo request message
Status                           1    # M A  S F
errorCode                       10    # O A  populated when operation fails
LOC_end                          4    # M A  Value #LOC

