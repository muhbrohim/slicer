# service-code: #CA1035
# endpoint:     /card/cs-unbilled-transaction-inquiry
# category:     CA
# section:      4.8
# program:      LHBSC35S
#
# #CA1035 - generated from CTBCLH31 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M N  Pagination Control. 0=initial, 1=continue, 2=last; enum: ["0","1","2"]
referenceNumber                 11    # M N  Intended for pagination; nullable: true
cycleCutDate                     8    # M N  YYYYMMDD
spendingAmount                  13    # M N  number (double)
cashLimit                       13    # M N  number (double)
cashAvailable                   13    # M N  number (double)
creditLimit                     13    # O N  number (double)
availableLimit                  13    # M A  number (double)
lastUsedDate                     8    # M A  YYYYMMDD
cardNumberMask                  19    # M A
cardMainType                     1    # M A  P=Primary, S=Supplementary
@repeat txnList 8
    transactionDate                  8    # M N  YYYYMMDD
    transactionTime                  6    # M N  HHMMSS
    transactionCode                  4    # M A
    transactionAmount               13    # M A  number (double)
    transactionCurrency              3    # M N
    transactionChannel              10    # O A
    transactionDescription          41    # O A  YYYYMMDD
    postDate                         8    # O A  nullable: true
    acquirerCountry                  3    # O A  mcc; nullable: true
    merchantCategoryCode             4    # M A
    merchantId                      15    # O A
    retrievalReferenceNumber        23    # O A  D=Debit, C=Credit
    transactionType                  2    # M A
    authorizationCode                6    # O N  nullable: true
    referenceNumber_2               11    # O N
@end
