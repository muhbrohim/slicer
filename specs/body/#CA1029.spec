# service-code: #CA1029
# endpoint:     /card/cs-pending-transaction-inquiry
# category:     CA
# section:      4.25
# program:      LHBSC29S
#
# #CA1029 - generated from CTBCLH52 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M A  Pagination Control. 0=initial call, 1=continue, 2= last record
referenceNumber                 11    # O N  Intended for pagination, provided by ascend on initial call: echoed by channe...
cardNumberMask                  19    # M A
accountNumber                   19    # M A
cashLimit                       13    # M N
cashAvailable                   13    # M N
creditLimit                     13    # M N
availableLimit                  13    # M N
lastUsedDate                     8    # O N  YYYYMMDD
cardType                         1    # M A  P=Primary, S=Supplementary

@repeat pendingTransactions 8
  recordBreak                      4    # M N
  transactionDate                  8    # M N  YYYYMMDD
  transactionExpired               8    # M A  HHMMSS
  transactionTime                  6    # M A
  transactionAmount               13    # O A
  transactionCurrency              3    # O A
  transactionDescription         100    # O A
  merchantId                      15    # M A  D=Debit to account, C=Credit to account
  merchantName                    40    # O A
  retrievalReferenceNumber        12    # M A
  transactionType                  1    # M A
  authorizationCode                6    # O A
@end

endTag                           4    # M A

