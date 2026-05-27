# service-code: ANI4000
# endpoint:     /card/payment-online-add
# category:     ANI
# section:      3.11
# program:      <none>
#
# ANI4000 - generated from CTBCLH11 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_Header                    105    # M A  Echo from request message
status                           1    # M A  S=success, F=failed
loc_end                          4    # M A  value #LOC

