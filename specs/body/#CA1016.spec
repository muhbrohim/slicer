# #CA1016 - generated from CTBCLH08 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_request                    26    # M A  echo from request message
programCode                     10    # M A
programType                     20    # M A  programtype(Revolving plan / Installment Plan)
programName                     50    # M A
rateType                        10    # M N  rate type(Flat Rate /Float Rate)
productCode                     10    # M A
schemeCode                      10    # M A  schemeCode(term)
ratePerMounth                    6    # M N
ratePerYear                      6    # M N
FeeRate                          6    # M N
vatRate                          6    # M N
minimumAmount                   13    # M N  minimun amount(revolving)
feeAmount                       13    # M N  Fee Amount( THB ) (revolving)
vatAmount                       13    # M N  VAT
monthlyInstallmentAmount        13    # M N
totalLoanAmount                 13    # M N  Total Loan Amount (Principle + Interest)
totalPrincipleAmount            13    # M N
totalInterestAmount             13    # M N
firstPaymentDate                 8    # M N  First Payment Date, To be confrimed with product
LOC_END                          4    # M A  Value #LOC

