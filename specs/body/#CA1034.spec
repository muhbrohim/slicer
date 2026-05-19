# #CA1034 - generated from CTBCLH30 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
statementMonth                   8    # O A
pageContinue                     1    # M A  Pagination Control. 0=initial call, 1=continue, 2= last record
referenceNumber                 11    # O N  Intended for pagination, provided by ascend on initial call; for subsequenct ...
cycleCut                         8    # M N  YYYYMMDD
statementDate                    8    # O N  YYYYMMDD
dueDate                          8    # M N  YYYYMMDD
gracePeriod                      8    # M N  YYYYMMDD
interest                        13    # M N
currentPaymentDue               13    # M N
totalInstallmentAmount          13    # M N
minimumPaymentAmount            13    # M N
fullPaymentAmount               13    # M N
lastPaymentAmount               13    # M N
overPaymentAmount               13    # M N
lastUsedDate                     8    # O N  YYYYMMDD
statementChannel                10    # M A
cardNumberMask                  19    # M A
cardMainType                     1    # M A  P=Primary, S=Supplementary
recBreak                         4    # M  Array of objects
postDate                         8    # M A  value:#REC
transactionFlag                  2    # M N  YYYYMMDD
transactionCode                  4    # M A
transactionDate                  8    # M A
transactionTime                  6    # M N  YYYYMMDD
transactionAmount               13    # M N  HHMMSS
transactionCurrency              3    # M N
transactionChannel              10    # M A
transactionDecription          100    # M A
billingAmount                   13    # M A
billingCurrency                  3    # M N

@repeat f_3 10
    acquirerCountry                  3    # M A
    merchantId                      15    # O A
    retrievalReferenceNumber        12    # O A
    transactionType                  1    # O A
    authorizationCode                6    # M A  D = Debit to account , C = Credit to account
    merchantCategoryCode             4    # O A
    referenceNumber_2               11    # O A  date + batch number + sequence numb
    LOC_end                          4    # M A  Value #LOC
@end

