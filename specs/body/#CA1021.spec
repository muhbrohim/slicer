# service-code: #CA1021
# endpoint:     /card/usage-setting-set
# category:     CA
# section:      3.16
# program:      LHBSC21S
#
# #CA1021 - generated from CTBCLH16 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_request                   172    # M A  Echo content of request msg
Status                           1    # M A  S(success)/F(Failed)
LOC_end                          4    # M A  Value #LOC

