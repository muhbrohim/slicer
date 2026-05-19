# #CA1020 - generated from CTBCLH15 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardPresentDomInd                1    # M A  Y/N, domestic card present
cardPresentInterInd              1    # M A  Y/N, international card present
cardNotPresentInd                1    # M A  Y/N, card not present
cashAdvanceInd                   1    # M A  Y/N, cash advance
contactlessInd                   1    # M A  Y/N
cardPresentDailyAmt             13    # M N  limit per day of this category 1400
cardNotPresentDailyAmt          13    # M N  limit per day of this category
cashAdvanceDailyAmt             13    # M N  limit per day of this category
cardPresentAmtPerTxn            13    # M N  per txn limit for card present
cardNotPresentAmtPerTxn         13    # M N  per txn limit for card not present
cashAdvanceAmtPerTxn            13    # M N  per txn limit for cash advance
cardPresentDailyCnt              2    # M N  daily count limit for card present
cardNotPresentDailyCnt           2    # M N  daily count limit for card not present
cashAdvanceDailyCnt              2    # M N  daily count limit for cash advance
totalSpendingAmt                13    # M N  total daily spending limit
endTag                           4    # M A

