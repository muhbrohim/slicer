# service-code: #US1003
# endpoint:     /customer/customer-search
# category:     US
# section:      4.2
# program:      LHBSU03S
#
# #US1003 — customer / array response.
# Layout follows DSPY-RESP-MSG-DETAIL, then echo block, then a fixed
# 20-element array of records terminated by "#LOC".

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE  (e.g. 'G')
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- echo block (188 bytes)
echo_cifNumber       16
echo_citizenId       13
echo_cardNumber      19
echo_mobileNumber    20
echo_fullName       100
echo_uid             20

# --- 20 customer records
@repeat records 20
    break             4     # "=01=" .. "=20="
    cifNumber        16
    mobileNumber     20
    customerStatus    2     # value + trailing space, or 2 spaces if empty
@end

# --- list terminator
loc_end               4     # literal "#LOC"
