# service-code: <header>
# endpoint:     <none>
# category:     -
# section:      -
# program:      <none>
#
# DSVI-HDR-INFO — 220-byte TCP header, shared by every API.
# Field names match the protocol doc, except HDR-SERVICE is exposed
# as `service_code` so the slicer dispatcher can find it.

# HDR-TAG (8) — channel marker, e.g. ADSVADSV
HDR_TAG               8

# HDR-CMD (8) = service-type (1) + service (7)
HDR_SERVICE_TYPE      1
service_code          7    # HDR-SERVICE — selects specs/body/{value}.spec

# HDR-CLIENT (20) — client identifier
HDR_CLIENT_ID        20

# H. Date / Time
HDR_DATE              8
HDR_TIME              8

# HDR-CLIENT (25) = job (10) + nbr (6) + trace (6) + filler (3)
HDR_JOB              10
HDR_NBR               6
HDR_TRACE             6
HDR_CLIENT_FILLER     3

# HDR-RSP-CODE (8) = major (4) + minor (4)
HDR_RSP_MAJOR         4
HDR_RSP_MINOR         4

# HDR-DATA-LEN (5) — body length in bytes
HDR_DATA_LEN          5

# HDR-FILLER (60) — reserved
HDR_FILLER           60

# HDR-HDR-ASC (70) = date-a (8) + time-a (8) + user (10) + queue (10) + filler (34)
HDR_DATE_A            8
HDR_TIME_A            8
HDR_USER             10
HDR_RTN_QUEUE        10
HDR_ASC_FILLER       34
