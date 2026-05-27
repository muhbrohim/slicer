# service-code: #CA1015
# endpoint:     /card/online-card-inquiry
# category:     CA
# section:      3.1
# program:      LHBSC15S
#
# #CA1015 - generated from CTBCLH01 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M A  is echo and ASC return value, is listed in FSD
lastCardNumber                  19    # O A  is echo and ASC return value, is listed in FSD

@repeat cardList 8
    accountNumber                   19    # M A  billing account this card belongs to
    accountOwnerCifNumber           16    # M A  CIF number of account owner
    accountStatus                    1    # M A
    productCode                      3    # M A
    accountBlockCode                 2    # O A  populated for primary cards only
    lastStatementDate                8    # O A  YYYYMMDD, populated for primary cards only
    paymentDueDate                   8    # O A  YYYYMMDD, populated for primary cards only
    permanentCreditLimit            13    # O N  populated for primary cards only
    temporaryCreditLimit            13    # O N  populated for primary cards only
    dateTemporaryCreditStart         8    # O A  YYYYMMDD, populated for primary cards only
    dateTemporaryCreditExpiry        8    # O A  YYYYMMDD, populated for primary cards only
    totalCreditLimit                13    # O N  effective limit (perm+temp), populated for primary cards only
    availableCreditLimit            13    # O N  populated for primary cards only
    cashCreditLimit                 13    # O N  populated for primary cards only
    cashAvailable                   13    # O N  populated for primary cards only
    cashCurrentBalance              13    # O N  populated for primary cards only
    totalOutstandingBalance         13    # O N  full payoff amount, populated for primary cards only
    minimumAmountDue                13    # O N  minimum payment required, for primary cards only
    lastPaymentAmount               13    # O N  populated for primary cards only
    lastPaymentDate                  8    # O A  YYYYMMDD, populated for primary cards only
    daysPastDue                      3    # O A  populated for primary cards only
    electronicStatementFlag          1    # O A  populated for primary cards only
    cardNumber                      16    # M A
    cardId                          19    # M A
    embossedName                    26    # M A
    cardSequenceNumber               3    # M A  reissue/replacement sequence
    cardLanguageCode                 1    # M A  ATM language code
    cardPinFlag                      1    # M A  source: external PIN system
    cardMainType                     1    # M A  P=Primary/S=Supplementary
    accountOwnerFlag                 1    # M A  Y/N, if supplementary card and cardCifNumber equals accountOwnerCifNumber the...
    cardIssuedDate                   8    # M A  YYYYMMDD
    cardExpiryDate                   4    # M A  MMYY
    cardBlockCode                    2    # O A
    cardBlockDate                    8    # O A  YYYYMMDD
    cardStatus                       1    # M A
    cardPendingActivationFlag        1    # M A  Y/N
    cardActivationDate               8    # O A  YYYYMMDD
    cardCifNumber                   16    # M A  cardholder CIF number
    separateLimitIndicator           1    # O A  0=shared/1=separate, supplementary cards only
    cardLimit                       13    # M N  primary: total credit limit, supplementary with separate limit: card perm cre...
    cardAvailableCreditLimit        13    # M N  primary: account available credit, supplementary: derived
    cardOutstandingBalance          13    # M N  primary: account outstanding balance, supplementary: sum of card transactions
    cardOutstandingBalanceSign       1    # M N  -
    fullPaymentAmount               13    # M N  Defaults to 0 if there is no statement or if the customer has fully paid
    oldCardId                       19    # O A  returned for replacement cards
    oldCardExpiryDate                4    # O A  MMYY, returned for renewed cards
@end

