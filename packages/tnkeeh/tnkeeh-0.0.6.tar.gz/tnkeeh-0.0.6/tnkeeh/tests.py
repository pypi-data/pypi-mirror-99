import tnkeeh
import pandas as pd 

text = tnkeeh._remove_special_chars('كيف حالكم ، يا أشقاء')
expected = 'كيف حالكم   يا أشقاء'

if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_special_chars('3 + 3 and 3 - 3', excluded_chars = ['+' , '-', '*'])
expected = '3 + 3 and 3 - 3'

if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_special_chars('9/8/1770', excluded_chars = ['/'])
expected = '9/8/1770'

if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_twitter_meta("@arthurlacoste check this link : https://lit.ly/hugeLink ! so #nsfw")
expected = "  check this link :   ! so  "
if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_diacritics("وَأفْجَـعُ مَن فَقَدْنَا مَن وَّجَدْنَا قُـبَيْلَ الفَقْدِ مَفْقُـودَ الْمِثالِ يُدفِّـنُ بَعْضُنَا")
expected = "وأفجـع من فقدنا من وجدنا قـبيل الفقد مفقـود المثال يدفـن بعضنا"

if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_html_elements('<doc id="7" url="https://ar.wikipedia.org/wiki?curid=7" title="ماء">')
expected = ""
if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_repeated_chars('هههههههه')
expected = "هه"
if text == expected:
    print('success')
else:
    print('failed')

text = tnkeeh._remove_extra_spaces('اهلا     كيف حالك')
expected = "اهلا كيف حالك"
if text == expected:
    print('success')
else:
    print('failed')

df = pd.DataFrame({'col1':['السلام عليكم', 'كيًف حالكم']})

print(tnkeeh.clean_data_frame(df, 'col1', remove_diacritics = True))



