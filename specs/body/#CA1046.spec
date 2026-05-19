# #CA1046 - generated from CTBCLH61 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
statementDate                    8    # M A
pageContinue                     1    # M A
referenceNumber                 11    # O A
cardNumber                      19    # M A
transactionDate                  8    # M A
transactionCode                  4    # M A
transactionAmount               11    # M N
postingDate                      8    # M A
billingCurrencyCode              3    # M A
transactionDescription          41    # M A
transactionType                  2    # O A
walletId                         1    # O A
originalCurrencyCode             3    # O A
originalAmount                  12    # O N
preConversionCurrencyCode        3    # O A
preConversionAmount             12    # O N
settlementCurrencyCode           3    # O A
settlementAmount                13    # O N
settlementFlag                   1    # O A
authorizationCode                6    # O A
sourceCode                       4    # O A
mccCode                          4    # O A
acquirerRefNumber               23    # O A
merchantBankNumber               4    # O A
merchantNumber                  11    # O A
zipCode                          5    # O A
state                            3    # O A
reimbursementAttribute           1    # O A
ifiIndicator                     1    # O A
psiIndicator                     1    # O A
mailTelIndicator                 1    # O A
otherProcessingIndicator         1    # O A
posEntryMode                     3    # O A
dmsCaseNumber                   10    # O A
addendaRef                      16    # O A

