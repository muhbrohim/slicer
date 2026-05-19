# #CA1032 - generated from CTBCLH04 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardCifNumber                   16    # M A  echo the request from asccend
pageContinue                     1    # M N  0=initial call, 1=continue, 2= last record
referenceNumber                 20    # M A  Intended for pagination, provided by ascend on initial call; for subsequenct ...
cardOutstandingBalance          13    # M A  sum txn this card no. value can be minus
cardOutstandingBalanceSign       1    # M N
cardNumberMask                  19    # M N
cardProduct                      3    # M N  Masking Card No.1111-11xx-xxxx-1111
transactionDate                  8    # M A
transactionTime                  6    # M A
transactionOriginalAmount       12    # M A
transactionOriginalCurrency      3    # M N
transactionChannel              10    # M A
transactionDescription          41    # O N
postingAmount                   12    # O A
postingCurrency                  3    # O A
postingDate                      8    # M A
merchantId                      11    # M A
mcc                              4    # O A
pendingFlag                      1    # M A  Y=Authorize not yet post(approved Auth), N=Posted(unbill)
transactionType                  1    # O A  D = Debit to account , C = Credit to account
refNumber                       11    # M N  date + batch number + sequence number

