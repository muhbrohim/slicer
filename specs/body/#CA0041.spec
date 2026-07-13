# service-code: #CA0041
# endpoint:     /card/supplement-card-credit-control-set
# category:     CA
# section:      4.20
# program:      SCDSC41S
#
# #CA0041 - generated from CTBCLH43 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
suppCardLimit			              13
channel	                        10
memo	                          60
status                           1    # O N

