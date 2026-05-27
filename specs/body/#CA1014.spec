# service-code: #CA1014
# endpoint:     /card/activate-card
# category:     CA
# section:      3.2
# program:      LHBSC14S
#
# #CA1014 - generated from CTBCLH02 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request_fields_1_4         77    # M A  Echo back from request message
status                           1    # M A  S=success, F=failed
promotionCode                   20    # O A  Return activation campaign code(refer to LOS)
LOC_END                          4    # M A  Value #LOC

