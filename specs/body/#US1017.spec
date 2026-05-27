# service-code: #US1017
# endpoint:     /customer/referral-search
# category:     US
# section:      5.2
# program:      LHBSU17S
#
# #US1017 - generated from CTBCLH54 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
mobileNumberLastFour             4    # M A  Last 4 digits of mobile number
pageContinue                     1    # M A  Pagination Control. 0=initial call, 1=continue, 2= last record
lastCifNumber                   16    # M O  Pagination Key
lastCardId                      19    # M O  Pagination Key
cifNumber                       16    # M A
customerFirstName               30    # M A
customerLastName                30    # M A
cardID                          19    # M A
LOC_end                          4    # M A  Value #LOC

