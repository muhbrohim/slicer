# ANI6000 — verify-PIN / encrypt-PIN response.
# Layout follows DSPY-RESP-MSG-DETAIL (response prefix), then the
# API-specific fields, then the "#LOC" terminator.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE  (e.g. 'R')
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- ANI6000 body  (mandatory/optional + type taken from contract)
encryptedPin         16     # M A  clear PIN encrypted with ZPK, PIN block format 01
channel              10     # M A  request channel
memo                 60     # O A
status                1     # M A  'S' = success, 'F' = fail
loc_end               4     # M A  literal "#LOC"
