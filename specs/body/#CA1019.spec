# service-code: #CA1019
# endpoint:     /epp/convert-instalment
# category:     CA
# section:      3.14
# program:      LHBSR14S
#
# #CA1019 - generated from CTBCLH14 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_request                   502    # M A  Echo content from request msg
programCode                     10    # M A
programType                     20    # M A  programtype(Revolving plan / Installment Plan)
programName                     50    # M A
rateType                        10    # M A  rate type(Flat Rate /Float Rate)
programMonth                     2    # M N  program month(installment)
totalPrincipleAmount            13    # M N  Principle Amount (THB)
totalFeeAmount                  13    # M N  Fee Amount( THB )
totalMonthlyInstallmentAmount   13    # M N  Total monthly installment Amount for all success txn
monthlyInterestRate              6    # M N
firstPaymentDate                 8    # M N
principalAmount                 13    # M N
feeAmount                       13    # M N
installmentPeriodMonth           2    # M N  Total Payment(Principle + Fixed Interest)
monthlyInstallmentAmount        13    # M N
transactionPostId               20    # M A
status                           1    # M A  S=success, F=failed
billed                           1    # M A  Y/N
LOC_END                          4    # M A  Value #LOC

