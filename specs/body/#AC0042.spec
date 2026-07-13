# service-code: #AC0042
# endpoint:     /card/temp-limit-set
# category:     AC
# section:      3.23
# program:      SCDSA42S
#
# #AC0042 - generated from CTBCLH23 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
tempCustAmount	13
tempCustStartDate	8
tempCustEndDate	8
tempAcctAmount	13
tempAcctStartDate	8
tempAcctEndDate	8
reasonCode	4
channel	10
memo	60
updateStatusSuccess              1    # M A  approved amount
approvedAmount                  13    # M N
currentLimit                    13    # M N  current limit ( before temp )
newLimit                        13    # M N  current limit + temp
LOC_end                          4    # M A  Value #LOC

