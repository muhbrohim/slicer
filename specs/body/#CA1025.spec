# service-code: #CA1025
# endpoint:     /card/early-settlement-inquiry
# category:     CA
# section:      4.14
# program:      LHBSS14S
#
# #CA1025 - generated from CTBCLH37 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                   118    # M A  Echo request message
status                           1    # M A  S=Eligible, F=Not Eligible
errorCode                       10    # M A  populated when not eligible
paymentAmount                   13    # M N  calculated early settlement amount
loanListCounter                  2    # M N  Number of array that has content
loanOrderNumber                 11    # M A
principalAmount                 13    # M N
interestAmount                  13    # M N
feeAmount                       13    # M N  nullable: true
LOC_END                          4    # M A  value #LOC

