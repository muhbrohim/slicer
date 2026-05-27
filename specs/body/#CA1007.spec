# service-code: #CA1007
# endpoint:     /card/card-block-code-set
# category:     CA
# section:      3.19
# program:      LHBSC07S
#
# #CA1007 - generated from CTBCLH19 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_Request                    72    # M A  Echo message request
Status                           1    # M A  S (success)/ (F Failed)
LOC_End                          4    # M A  Value #LOC

