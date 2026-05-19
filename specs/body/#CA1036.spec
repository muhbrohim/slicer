# #CA1036 - generated from CTBCLH33 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardNumberMask                  19    # M A
retrievalReferenceNumber        23    # O A  nullable: true
acquirerId                      11    # O A  nullable: true
cardType                         1    # M A  P=Primary, S=Supplementary
transactionDate                  8    # M N  YYYYMMDD
transactionTime                  6    # M N  HHMMSS
postDate                         8    # M N  YYYYMMDD
postTime                         6    # M N  HHMMSS
paymentChannel                  10    # M A
paymentAmount                   13    # M N  number (double)

