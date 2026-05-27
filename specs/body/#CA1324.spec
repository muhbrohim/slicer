# service-code: #CA1324
# endpoint:     /card/ipp-eligible-program-get-details
# category:     CA
# section:      3.24
# program:      LHBSR23S
#
# #CA1324 - generated from CTBCLH62 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
Echo_request                    43    # M A  Echo from request msg
monthSequence                    2    # M N
monthlyAmount                   13    # M N
monthlyPrincipalAmount          13    # M N
monthlyInterestAmount           13    # M N
LOC_End                          4    # M A  Value #LOC

