# service-code: #CA1041
# endpoint:     /card/waive-transaction
# category:     CA
# section:      4.22
# program:      LHBSC41S
#
# #CA1041 - generated from CTBCLH45 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
transactionAmount               13
transactionCode                 4
referenceNumber                 11
channel                         10
memo                            60
status                           1    # M A  S(Success)/F(Failed)
LOC_end                          4    # M A  Value #LOC

