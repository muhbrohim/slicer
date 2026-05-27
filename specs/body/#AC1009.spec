# service-code: #AC1009
# endpoint:     /account/account-block-code-set
# category:     AC
# section:      4.18
# program:      LHBSA09S
#
# #AC1009 - generated from CTBCLH40 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
echo                            72    # M A  Echo request message
status                           1    # M A  S=success, F=failed

