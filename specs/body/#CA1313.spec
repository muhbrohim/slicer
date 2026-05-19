# #CA1313 - generated from CTBCLH13 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_request                    15    # M A  Echo message from request msg
programCode                     10    # M A
programName                     50    # M A
productCode                     10    # M A
programScheme                   10    # M A
rateType                        10    # M A  rate type(Flat Rate /Float Rate)
schemeCode                      10    # M A  schemeCode(term code)
ratePerMounth                    6    # M A
ratePerYear                      6    # M A
vatRate                          6    # M A
handlingFee                     13    # M A
monthlyInstallmentAmount        13    # M N
totalLoanAmount                 13    # M N  Total Loan Amount (Principle + Interest)
totalPrincipleAmount            13    # M N
totalInterestAmount             13    # M N
LOC_end                          4    # M A  Value #LOC

