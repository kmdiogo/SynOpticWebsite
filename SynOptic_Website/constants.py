# Scale Field constants
CMAJOR = "CMAJOR"
CMAJOR_PENT = "CMAJOR_PENT"
GMAJOR = "GMAJOR"
FLYDIAN = "FLYDIAN"
CCHROMATIC = "CCHROMATIC"

SCALE_CHOICES = (
    (CMAJOR, "C Major"),
    (CMAJOR_PENT, "C Major Pentatonic"),
    (GMAJOR, "G Major"),
    (FLYDIAN, "F Lydian"),
    (CCHROMATIC, "C Chromatic")

)

# Song Length Field constants
SONGLENGTH_CHOICES = (
    (8,"Short"),
    (16,"Medium"),
    (32,"Long")
)