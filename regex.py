# -*- coding: utf-8 -*-
puncRe=u'(\r|-|\n|,|"|\'|\(|\)|;|\.|!|\?|؟|،|؛|{|}|\[|\]|\\\|0|1)'
# Standard punctuation
underscoreRe=u'\_'
hashRe=u'\#'
# Underscore (for hashtags)
httpRe=u'http'
httpCleanRe=u'(\r|\n|"|”)'
atRe=u'\A\@'

alifRe=u'(آ|أ|إ|آ)'
alifMaksourRe=u'ى'
# Variations of letter alif
wawRe=u'ؤ'
# Letter waw
hahRe=u'ه\Z'
#hahaRe=u'هههه\Z'
hahmarbotaRe=u'ة\Z'

# Letter hah
alRe=u'(\Aلل\Aفال|\Aكال|\Aبال|\Aوال|\Aال|\Aبت|\Aنت|\Aبي|\Aات|\Aيا)'
# Variations of al
tuhaRe=u'تها\Z'
haRe=u'(ها\Z)'

# Strip feminine pronoun
verbSuffixesRe=u'(ون\Z|ين\Z|وا\Z|كم\Z|نا\Z|تك\Z|هم\Z|"\Z)'
# Verb sufixes
harakatRe=u'(ٍ|َ|ُ|ِ|ّ|ْ|ً)'
# Diacritics
# All unicode regular expressions must be uncompiled

