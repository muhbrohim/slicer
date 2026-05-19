# #US1018 - generated from CTBCLH57 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
phoneNumber                     20    # M A
cifNumber                       16    # M A
customerBlockCode                2    # M A
accountCounter                   2    # M N
cardCounter                      2    # M N
accountNumber                   19    # M A
accountBlockCode                 2    # O A
cardId                          19    # M A
cardBlockCode                    2    # O A
LOC_end                          4    # M A  Value #LOC

