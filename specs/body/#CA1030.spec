# #CA1030 — credit card statement / billed transactions response.
# Layout: DSPY-RESP-MSG-DETAIL (response prefix), echo+paging block, a
# 10-element billedTransactions array, then "#LOC".

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE (e.g. 'R')
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- echo / paging block (47 bytes)
echo_statementDate    8     # M A   echo back of request's statementDate
pageContinue          1     # M A   0=initial, 1=continue, 2=last record
referenceNumber      11     # O A   pagination cursor (echo on subsequent calls)
statementDate         8     # M N   YYYYMMDD
cardNumberMask       19     # M A   e.g. 1111-11xx-xxxx-1111 (or blank)

# --- 10 billed transactions, 148 bytes each
@repeat billedTransactions 10
    transactionType        1    # M A
    transactionDate        8    # M N   YYYYMMDD
    transactionTime        6    # M N   HHMMSS
    transactionAmount     12    # M N
    transactionCurrency    3    # M A
    transactionChannel    10    # M A
    transactionDescription 41   # M A
    postingDate            8    # M N   YYYYMMDD
    billingAmount         12    # M N
    billingCurrency        3    # O A
    merchantId            11    # O A
    retrievalRefNumber    12    # O A
    authorizationCode      6    # O A
    mcc                    4    # O A
    referenceNumber       11    # O A   date + batch + sequence
@end

# --- list terminator
loc_end               4     # literal "#LOC"
