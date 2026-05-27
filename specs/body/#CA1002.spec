# service-code: #CA1002
# endpoint:     /card/card-secure-info-inquiry
# category:     CA
# section:      3.3
# program:      LHBSC02S
#
# #CA1002 - generated from CTBCLH03 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardNumber                      19    # M A  Encrypted，Masking Card No.1111-11xx-xxxx-1111
cardholderName                  26    # M A
cardCVV2                         4    # M A  CVV2 - Encrypted，Masking all,xxxxxxxxxxxxxxx
productCode                      3    # M A
cardType                         3    # M A
cardStatementDay                 4    # M A  Cycle day ex. 1015
endTag                           4    # M A

