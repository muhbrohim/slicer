# #US1008 - generated from CTBCLH24 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
numberOfRecord                   2    # O N
pageContinue                     1    # M A  Pagination control. 0 = initial call, 1 = continue, 2 = last record.
last_memoId_memo_sequence        3    # O A
last_memoDate                    8    # O N
last_memoTime                    8    # O N
memoExt                         27    # O A  additional key for retrieve
memoId_memo_sequence             3    # M A
memoDate                         8    # M N
memoTime                         8    # M N
memoType                         1    # M A
memoText                        60    # M A
channel_user                    10    # M A
LOC_end                          4    # M A  Value #LOC

