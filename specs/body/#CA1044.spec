# #CA1044 - generated from CTBCLH28 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M A
lastCardNumber                  19    # O A

# --- array 10 records
@repeat records 10
  recBreak                         4    # M A  record break ，Value:=01=/=02=/...
  citizenId                       13    # O A
  mobileNumber                    20    # O A
  cardId                          19    # M A
  cardMainType                     1    # M A  P=Primary, S=Supplementary
  cardNumberMask                  19    # M A
  cardAccountNumber               19    # M A
  cardProductNumber                3    # M A
  cardStatus                       2    # M A
  cardBlockCode                    2    # O A
  cardBlockDate                    8    # O A  YYYYMMDD
  cardIssuedDate                   8    # M A  YYYYMMDD
  cardLastUsedDate                 8    # M A  YYYYMMDD
  englishName                     40    # M A
  localName                       40    # O A
  embossedName                    26    # M A
  cardLanguageCode                 2    # M A
  cardPinFlag                      1    # M A  Y/N
  cardExpiryDate                   4    # M A  YYMM
  cardActivationFlag               1    # M A  Y/N
  cardActivationDate               8    # O A  YYYYMMDD
  cardCifNumber                   16    # M A
  cardLimit                       13    # M N
  cardAvailableCreditLimit        13    # M N
  cardAvailableCashLimit          13    # M N
  cardCreditLimit                 13    # M N
  cardCashLimit                   13    # M N
  cardOutstandingBalance          13    # M N
@end
LOC_end                          4    # M A  Value #LOC

