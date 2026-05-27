# service-code: #CA1038
# endpoint:     /card/cs-loan-inquiry
# category:     CA
# section:      4.9
# program:      LHBSC38S
#
# #CA1038 - generated from CTBCLH32 (specs/reff/all-spec.md).
# Layout: response prefix, then service body.
# Review and adjust array boundaries / field types as needed.

# --- response prefix (DSPY-RESP-CODE + DSPY-KEY-TYPE + DSPY-KEY-VALUE)
resp_code             2     # DSPY-RESP-CODE
key_type              1     # DSPY-KEY-TYPE
key_bank              4     # DT0000-KEY-BANK
key_val              19     # DT0000-KEY-VAL

# --- service body
pageContinue                     1    # M A  Pagination Control. 0=initial call, 1=continue, 2= last record
referenceNumber                 11    # O A  Intended for pagination, provided by ascend on initial call; for subsequenct ...
cardNumberMask                  19    # M A  format 1111-11xx-xxxx-1111
cardMainType                     3    # M N
referenceNumber_2               11    # M A
orderStatus                      1    # M A
cardNumber                      19    # M A
programCode                      6    # M A
productCode                      6    # M A
paymentSchemeCode                6    # M A
numberOfUnits                    9    # M A
orderAmount                     13    # M N
description                     30    # M A
deliveryCode                     1    # O A
deliveryAddress                120    # O A
deliveryDate                     8    # O A
remarks                         60    # O A
sourceOfOrder                    1    # O A
authorizationCycle               2    # O A
billingCycle                     2    # O A
lastAuthDate                     8    # O A
lastAuthAmount                  13    # O N
lastAuthCode                     6    # O A
responseCode                     2    # O A
lastPaymentDate                  8    # O A
numberOfInstallmentsBilled       3    # M A
numberOfDeferred                 2    # O A
unitsCancelled                   9    # O A
amountCancelled                 13    # O N
dateCancelled                    8    # O A
cancelledByUser                 10    # O A
unitsReturned                    9    # O A
amountReturned                  13    # O N
dateReturned                     8    # O A
returnedByUser                  10    # O A
dateStopped                      8    # O A
stoppedByUser                   10    # O A
dateAccelerated                  8    # O A
acceleratedByUser               10    # O A
dateDeferred                     8    # O A
deferredByUser                  10    # O A
deferNumber                      2    # O A
rebateAmount                    13    # O N
accelerationAmount              13    # O N
merchantPostingDate              8    # O A
installmentPlan                  4    # O A  YYYYMMDD
installmentIndicator             1    # O A  YYYYMMDD
handlingFee                     13    # O N
interestRate                     6    # O N
totalInterest                   13    # O N
monthlyInterestAmount           13    # O N
interestFreeMonths               2    # O A
waiveInstallmentFromMonth        2    # O A
waiveInstallmentToMonth          2    # O A  YYYYMMDD
accelerationFee                 13    # O N
disputeIndicator                 1    # O A
remainingPrincipal              13    # M N
remainingInterest               13    # O N
principalRemained               13    # O N
lastPayMode                      1    # O A
lastRate                         6    # O N
lastInstallment                 13    # O N  YYYYMMDD
creationDate                     8    # M A
lastUpdateDate                   8    # O A
lastUpdateTime                   8    # O A
lastUpdateUserId                10    # O A

