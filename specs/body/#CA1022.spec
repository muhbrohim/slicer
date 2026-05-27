# service-code: #CA1022
# endpoint:     /card/noti-setting-set
# category:     CA
# section:      3.18
# program:      LHBSC22S
#
# #CA1022 - generated from CTBCLH18 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                   130    # M A  Echo from request message
Status                           1    # M A  S/F
LOC_End                          4    # M A  Value #LOC

