# service-code: #CA1033
# endpoint:     /card/statement-history-inquiry
# category:     CA
# section:      4.6
# program:      LHBSC33S
#
# #CA1033 — /card/statement-history-inquiry response.
# Layout: DSPY-RESP-MSG-DETAIL (response prefix), then a 6-element
# statementList array, then "#LOC".

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE (e.g. 'R')
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- statementList: up to 6 statements, 563 bytes each
@repeat statementList 6
    statementDate                  8    # M N  YYYYMMDD
    paymentDueDate                 8    # M N  YYYYMMDD
    minimumPaymentAmount          13    # M N
    amountPastDue                 13    # M N
    creditLimit                   13    # M N
    cashLimit                     13    # M N
    availableCredit               13    # M N
    availableCash                 13    # M N
    currencyCode                   3    # M A
    numberOfTransactions          10    # M N
    blockCode                      2    # M A
    status                         1    # M A
    outOfBalanceFlag               1    # M A
    statementMessage               6    # M A

    # --- retail metrics
    retailStatementBalance        13    # M N
    retailCurrentBalance          13    # M N
    retailInterestRate             6    # M N
    retailDebitPurchaseAmount     13    # M N
    retailDebitPurchaseCount       5    # M N
    retailCreditPurchaseAmount    13    # M N
    retailCreditPurchaseCount      5    # M N
    retailDebitAmount             13    # M N
    retailDebitCount               5    # M N
    retailCreditAmount            13    # M N
    retailCreditCount              5    # M N
    retailPaymentAmount           13    # M N
    retailPaymentReversalAmount   13    # M N
    retailInterestAdjustment      11    # M N
    retailServiceCharge           11    # M N
    retailMiscFee                 11    # M N
    retailInsuranceFee            11    # M N
    retailMembershipFee           11    # M N
    retailStatementInterest       11    # M N
    retailDisputeBalance          13    # M N

    # --- cash metrics
    cashStatementBalance          13    # M N
    cashCurrentBalance            13    # M N
    cashInterestRate               6    # M N
    cashAdvanceAmount             13    # M N
    cashAdvanceCount               5    # M N
    cashAdvanceCreditAmount       13    # M N
    cashAdvanceCreditCount         5    # M N
    cashDebitAmount               13    # M N
    cashDebitCount                 5    # M N
    cashCreditAmount              13    # M N
    cashCreditCount                5    # M N
    cashPaymentAmount             13    # M N
    cashPaymentReversalAmount     13    # M N
    cashInterestAdjustment        11    # M N
    cashServiceCharge             11    # M N
    cashStatementInterest         11    # M N
    cashDisputeBalance            13    # M N

    # --- bonus points
    bonusPointBeginBalance        13    # M N
    bonusPointAdded               11    # M N
    bonusPointDeducted            11    # M N
    bonusPointEndBalance          13    # M N
    bonusPointPriorYear           13    # M N
@end

# --- list terminator
loc_end               4     # literal "#LOC"
