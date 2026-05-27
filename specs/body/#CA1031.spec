# service-code: #CA1031
# endpoint:     /card/online-statement-list-inquiry
# category:     CA
# section:      3.6
# program:      LHBSC31S
#
# #CA1031 - generated from CTBCLH06 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo                 19     # DT0000-KEY-VAL
@repeat statmentList 24
  statementDate                    8    # M N
  paymentDueDate                   8    # M N
  fullPaymentAmount               13    # M N
  minimumPaymentAmount            13    # M N
@end
LOC_END                          4    # M A  Value #LOC

