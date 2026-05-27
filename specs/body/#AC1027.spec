# service-code: #AC1027
# endpoint:     /account/billing-channel-set
# category:     AC
# section:      4.27
# program:      LHBSA27S
#
# #AC1027 - generated from CTBCLH56 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                    81    # M A  Echo request message
status                           1    # M A  S=success, F=failed
LOC_end                          4    # M A  Value #LOC

