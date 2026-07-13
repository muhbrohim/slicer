# service-code: #CA1017
# endpoint:     /card/cash-transaction-add
# category:     CA
# section:      3.9
# program:      LHBSC09S
#
# #CA1017 - generated from CTBCLH09 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
programCode	10
productCode	10
programScheme	10
programType		1
requestAmount		13
channel		10
memo		60
transactionId		22
reversalFlag		1
Status                           1    # M A  Status transaction
approvalCode                     6    # M A  Aprroval code
LOC_end                          4    # M A  Value #LOC

