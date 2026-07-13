# service-code: #US1004
# endpoint:     /customer/customer-get
# category:     US
# section:      4.3
# program:      LHBSU04S
#
# #US1004 - generated from CTBCLH26 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body

cifNumber                       16    # M A
customerNumber                  16    # M A
customerStatus                   2    # M A
customerBlockCode                2    # O A
customerBlockDate                8    # O N
firstNameEN                     50    # M A
middleNameEN                    50    # O A
lastNameEN                      50    # M A
titleEN                         20    # M A
firstNameTH                     50    # O A
middleNameTH                    50    # O A
lastNameTH                      50    # O A
titleTH                         20    # O A
nationality                      3    # M A
language                         2    # M A
gender                           1    # M A
vipFlag                          1    # M A
citizenId                       13    # O A
passportId                      20    # O A
uid                             20    # O A
dateOfBirth                      8    # M N
annualIncomeAmount              13    # O N
annualIncomeAmountSign           1
staffFlag                        1    # M A
occupation                      50    # O A
mobileNumber                    20    # O A
homePhoneNumber                 20    # O A
officePhoneNumber               20    # O A
customerEmail                   50    # O A
addressLine1                    40    # O A
addressLine2                    40    # O A
addressLine3                    40    # O A
addressLine4                    40    # O A  homeAddress
city                            30    # O A
zipCode                         10    # O A
country                         40    # O A
addressLine1_2                  40    # O A
addressLine2_2                  40    # O A
addressLine3_2                  40    # O A
addressLine4_2                  40    # O A  workAddress
city_2                          30    # O A
zipCode_2                       10    # O A
country_2                       40    # O A
addressLine1_3                  40    # O A
addressLine2_3                  40    # O A
addressLine3_3                  40    # O A
addressLine4_3                  40    # O A  legalAddress
city_3                          30    # O A
zipCode_3                       10    # O A
country_3                       40    # O A
addressLine1_4                  40    # O A
addressLine2_4                  40    # O A
addressLine3_4                  40    # O A
addressLine4_4                  40    # O A  correspondenceAddress
city_4                          30    # O A
zipCode_4                       10    # O A
country_4                       40    # O A
billingChannel                  10    # O A
customerJoinDate                 8    # M N
customerMonthsOnBook             4    # M N
numberOfActiveAccounts           3    # M N
permanentCreditLimit            13    # M N
permanentCreditLimitSign         1    # M N
totalCreditLimit                13    # O N
totalCreditLimitSign             1    # O N
tempCreditLimitStartDate         8    # M N
tempCreditLimitEndDate           8    # O N
cashLimit                       13    # M N
cashLimitSign                    1    # M N
shadowLimit                     13    # M N
shadowLimitSign                  1    # M N
availableCreditLimit            13    # M N
availableCreditLimitSign         1    # M A
availableCashCreditLimit        13    # M A
availableCashCreditLimitSign     1    # M A
currentBalance                  13    # M N
currentBalanceSign               1    # M A
memoDebit                       13    # M N
memoCredit                      13    # M N
doNotEmailFlag                   1    # M A
doNotSMSFlag                     1    # M A
doNotCallFlag                    1    # M A
doNotNotiFlag                    1    # M A
endTag                           4    # M A
