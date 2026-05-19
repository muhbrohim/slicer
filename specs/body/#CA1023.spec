# #CA1023 - generated from CTBCLH17 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
cardPresentNotificationEnabled    1    # M A  Y/N
cnpNotificationEnabled           1    # M A  Y/N
caNotificationEnabled            1    # M A  Y/N
minimumAmountNotification       13    # M N  threshold amount to trigger notification
lhbYouNotificationEnabled        1    # M A  Y/N
emailNotificationEnabled         1    # M A  Y/N
smsNotificationEnabled           1    # M A  Y/N
promotionEmailEnabled            1    # M A  Y/N
LOC_End                          4    # M A  Value #LOC

