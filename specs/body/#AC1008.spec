# service-code: #AC1008
# endpoint:     /account/account-get
# category:     AC
# section:      4.4
# program:      LHBSA08S
#
# #AC1008 - generated from CTBCLH27 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
@repeat accountList 2
  accountBreak                     4    # M A  value:=01=\=02=\...
  accountOwnerCifNumber           16    # M A
  accountOwnerFlag                 1    # M A
  accountNumber                   19    # M A
  productCode                      3    # M A
  accountBlockCode                 2    # O A
  accountBlockDate                 8    # O N
  billingCycleDay                  2    # M N
  accountStatus                    2    # M A
  applyDate                        8    # M N
  openDate                         8    # M N
  writeOffDate                     8    # O N
  closedDate                       8    # O N
  physicalStatement                1    # O A
  chargeOffStatus                  2    # O A
  chargeOffReason                  4    # O A
  incomeAmount                    13    # O N
  skipPaymentFlag                  1    # M A
  skipPaymentLastDate              8    # O N
  drFlag                           1    # M A
  drNumber                         3    # O N
  drLastDate                       8    # O N
  tdrFlag                          1    # M A
  tdrNumber                        3    # O N
  tdrLastDate                      8    # O N
  debtClinicFlag                   1    # M A
  debtClinicDate                   8    # O N
  numberOfSupp                     2    # O N
  printStatementFlag               1    # M A
  stopStatementFlag                1    # M A
  statementDeliverySuccess         1    # M A
  archiveStatus                    1    # O A
  permanentCreditLimit            13    # M N
  tempCreditLimit                 13    # O N
  tempCreditStartDate              8    # O N
  tempCreditExpiryDate             8    # O N
  cashCreditLimit                 13    # M N
  installmentCreditLimit          13    # M N
  shadowLimit                     13    # O N
  lastPermanentLimitDate           8    # O N
  lastPermanentLimitAmount        13    # O N
  accountPermanentIncreaseDate     8    # O N
  currentBalance                  13    # M N
  memoDebit                       13    # M N
  memoCredit                      13    # M N
  cashBalance                     13    # M N
  cashMemoDebit                   13    # M N
  cashMemoCredit                  13    # M N
  totalOutstandingAmount          13    # M N
  authOutstandingAmount           13    # M N
  authCashOutstandingAmount       13    # M N
  availableCreditLimit            13    # M N
  availableCashCreditLimit        13    # M N
  availableInstallmentCreditLimit   13    # M N
  lastPurchaseDate                 8    # O N
  lastPurchaseAmount              13    # O N
  lastPaymentDate                  8    # O N
  lastPaymentAmount               13    # O N
  paymentDate                      8    # O N
  atmEligible                      1    # M A
  ippEligible                      1    # M A
  paymentRate                      5    # M N
  highSpendingAmount              13    # O N
  highSpendingDate                 8    # O N
  paymentHoldAmount               13    # O N
  membershipFeeLastAmount         13    # O N
  membershipFeeLastDate            8    # O N
  supplementaryMembershipFeeLastAmount   13    # O N
  supplementaryMembershipFeeLastDate    8    # O N
  lastActivityDate                 8    # O N
  disputeItemAmount               13    # O N
  disputeNumber                    3    # O N
  lastCashAdvanceAmount           13    # O N
  lastCashAdvanceDate              8    # O N
  accruedInterest                 13    # O N
  chargeOffAccruedInterest        13    # O N
  lastStatementDate                8    # O N
  nextStatementDate                8    # M N
  paymentDueDate                   8    # M N
  gracePeriodDate                  8    # M N
  fullPaymentAmount               13    # M N
  minimumPaymentAmount            13    # M N
  lastDelinquencyDate              8    # O N
  daysPastDue                      3    # M N
  delinquencyProfile24Month       24    # O A
  dayProfile24Month               24    # O A
  intoCollectionDate               8    # O N
@end
LOC_end                          4    # M A  Value #LOC

