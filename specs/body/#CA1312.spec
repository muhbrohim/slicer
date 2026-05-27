# service-code: #CA1312
# endpoint:     /card/ipp-eligible-transaction-by-program-get
# category:     CA
# section:      3.12
# program:      LHBSC12S
#
# #CA1312 - generated from CTBCLH12 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
req_echo_min_amt                13    # M A  request echo from min amt
pageContinue                     1    # M A  0=initial call, 1= continue / more record, 2= last record
referenceNumber                 19    # O A  Intended for pagination, provided by ascend on initial call; for subsequenct ...
authorizationCode                6    # M A
approvalCode                     6    # M A
transactionPostId               20    # M A  Txn Post Id (Transaction reference number) TBC field name
postAmount                      12    # M N
postDate                         8    # M N
transactionDate                  8    # M N
transactionTime                  6    # M N
firstPaymentDate                 8    # M N
description                     41    # M A
merchantCategoryCode             4    # M A
merchantId                      15    # M A
refNumber                       11    # O A  date + batch number + sequence number
LOC_end                          4    # M A  value #LOC

