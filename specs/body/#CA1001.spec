# service-code: #CA1001
# endpoint:     /card/card-validate
# category:     CA
# section:      3.10
# program:      LHBSC01S
#
# #CA1001 - generated from CTBCLH10 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardNumberMark                  19    # M A  Masking Card No.1111-11xx-xxxx-1111
cardId                          19    # M A
LOC_End                          4    # M A  Value #LOC

