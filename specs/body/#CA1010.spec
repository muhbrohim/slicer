# service-code: #CA1010
# endpoint:     /card/cash-available-inquiry
# category:     CA
# section:      3.7
# program:      LHBSC10S
#
# #CA1010 - generated from CTBCLH07 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardNumberMask                  19    # M A  Masking Card No.1111-11xx-xxxx-1111
product_Code                     3    # M A
cardType                         1    # M A  Primary, Supplement
accountOwner                     1    # M A  [Y/N] , if cardNo is primary
cardStatus                       2    # M A  "Account status: '0' – Newly Created, '1' – Inactive, '2' – Active, '5' – Cha...
accountBlockCode                 2    # O A
cashAvailableFlag                1    # M A  [Y/N], if can't do CA show N
cashOutstandingBalance          13    # M N
totalAvailableCreditLimit       13    # M N
availableCashCreditLimit        13    # M N
numberOfCashLimitPerDay          3    # M N
numberOfCashUsagePerDay          3    # M N
amountCashLimitPerDay           13    # M N  Include Memo
amountCashUsagePerDay           13    # M N  Include Memo
minimumCashRequestAmount        13    # M N  LHB You back-office per Product Code
maximumCashRequestAmount        13    # M N  LHB You back-office per Product Code
LOC_end                          4    # M A  Value #LOC

