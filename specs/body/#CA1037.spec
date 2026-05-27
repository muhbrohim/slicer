# service-code: #CA1037
# endpoint:     /card/cs-payment-history-inquiry
# category:     CA
# section:      4.11
# program:      LHBSC37S
#
# #CA1037 - generated from CTBCLH34 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
statementDate                    8    # M N  YYYYMMDD
lastPaymentDate                  8    # O N  YYYYMMDD
monthsOnBook                     4    # M N
paymentFlag                      1    # M A  0=Not reach minimum payment, 1=Minimum payment, 2=More than minimum but not f...
daysPastDue                      3    # M N
lifeToDateAmount                13    # M N
cycleToDateAmount               13    # M N
yearToDateAmount                13    # M N
highBalancePurchase             13    # O N
paymentToday                    11    # O N
statementYear                    2    # M N  YY
statementMonth                   2    # M N  MM

