# service-code: #CA1045
# endpoint:     /card/cs-activate-card
# category:     CA
# section:      4.12
# program:      LHBSC45S
#
# #CA1045 - generated from CTBCLH35 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
memo                            60    # O A  echo
channel                         10    # O A  echo
status                           1    # M A  S=success, F=failed
promotionCode                   20    # O A  activation campaign code from LOS
errorCode                       10    # O A  populated when activation fails
endTag                           4    # M A

