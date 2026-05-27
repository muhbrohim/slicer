# service-code: #CA1028
# endpoint:     /card/trasaction-inquiry
# category:     CA
# section:      4.24
# program:      LHBSC28S
#
# #CA1028 - generated from CTBCLH50 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_retrievalReferenceNumber   11    # M A  unique transaction identifier
transactionDate                  8    # M N  YYYYMMDD
transactionTime                  6    # M N  HHMMSS
transactionAmount               13    # M N  number (double)
transactionCurrency              3    # M A
transactionDescription         100    # M A
postDate                         8    # M N  YYYYMMDD
merchantId                      15    # O A
merchantName                    40    # O A
retrievalReferenceNumber        11    # M A
transactionType                  1    # M A  D=Debit to account, C=Credit to account
authorizationCode                6    # O A

