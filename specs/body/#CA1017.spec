# #CA1017 - generated from CTBCLH09 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo_request                   135    # M A  echo from request msg
Status                           1    # M A  Status transaction
approvalCode                     6    # M A  Aprroval code
LOC_end                          4    # M A  Value #LOC

