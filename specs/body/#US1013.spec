# #US1013 - generated from CTBCLH47 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M A  Pagination Control. 0=initial call, 1=continue, 2= last record
lastAccount                     19    # O A  Intended for pagination, provided by ascend on initial call; for subsequenct ...
lastCard                        19    # O A  Intended for pagination, provided by ascend on initial call; for subsequenct ...
cifNumber                       16    # M A
MonthOnBook                      5    # O N
earlyWarningFlag                 1    # O A
classCode                        1    # O A
vipFlag                          2    # O A
familyBankingFlag               20    # O A
staffFlag                       20    # O A
customerStatus                  10    # M A
crrB                            10    # O A
creditReviewFlag                 4    # O A
tempLimitPurposeFlag             3    # O A
customerDPD                      3    # O N
customerLocalName               40    # O A
customerEnglishName             40    # M A
customerCreditLimit             13    # M N
customerTemporaryCreditLimit    13    # O N
custAvialiableCreditLimit       13    # M N
custCurrentBalance              13    # M N
custCashCreditLimit             13    # M N
custCashCurrBal                 13    # M N
custOutStandingBalance          13    # O N
custDateTempCreditExpiry         8    # O N  YYYYMMDD
cusRiskLevelSegment             40    # O A
custDateTempCreditStart          8    # O N  YYYYMMDD
accountRecBreak                  4    # M A
accountNo                       19    # M A
accountOpenDate                  8    # O N
cardMailingFlag                  1    # O A
deliveryBranchCode               5    # O A
accountStatus                   10    # O A
accountBlockCode                 2    # O A
dayPastDue                       3    # O N
creditLimit                     13    # O N
tempCreditLimit                 13    # O N
outStandingBalance              13    # O N
supplNumberActiveCount           3    # O A
cardRecBreak                     4    # M A
cardCifNo                       16    # M A
cardId                          19    # M A
cardNBRMask                     19    # M A
productCode                     10    # O A
cardAccountNumber               19    # M A
cardStatus                      10    # M A
cardMainType                     1    # M A
cardIssuedDate                   8    # M N
cardBlockCode                    2    # O A
endTag                           4    # M A

