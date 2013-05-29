#!/usr/bin/python
# -*- coding: utf-8 -*-

#a############################################################################
#a########  "قُلۡ بِفَضلِ ٱللَّهِ وَبِرَحمَتِهِۦ فَبِذَٰلِكَ فَليَفرَحُواْ هُوَ خَيرُُ مِّمَّا يَجمَعُونَ"  #########
#a############################################################################

import re, itertools
import  daw_araby
from daw_contacts import AwzanDB
z = 1

myawzan = AwzanDB()

#a العلل والزحافات------------------------------------------------------------
  
Zihafat_3ilal = { 
                 0:[u'لا شيء',u'صحيحة',u'صحيح'],
                 100:[u'لا شيء',u'صحيحة',u'صحيح'],
                 1:[u'إذالة',u'مذالة',u'مذال'],
                 2:[u'إضمار',u'مضمرة',u'مضمر'], 
                 3:[u'بتر',u'بتراء',u'أبتر'], 
                 4:[u'ترفيل',u'مرفّلة',u'مرفّل'], 
                 5:[u'تسبيغ',u'مسبّغة',u'مسبّغ'], 
                 6:[u'تشعيث',u'مشعّثة',u'مشعّث'], 
                 7:[u'ثلم',u'ثلماء',u'أثوم'], 
                 8:[u'جمم',u'جمّاء',u'أجمّ'], 
                 9:[u'حذذ',u'حذّاء',u'أحذّ'], 
                 10:[u'حذف',u'محذوفة',u'محذوف'], 
                 11:[u'خبل',u'مخبولة',u'مخبول'], 
                 12:[u'خبن',u'مخبونة',u'مخبون'], 
                 13:[u'خرب',u'خرباء',u'أخرب'], 
                 14:[u'خرم',u'خرماء',u'أخرم'], 
                 15:[u'خزل',u'مخزولة',u'مخزول'], 
                 16:[u'شتر',u'شتراء',u'أشتر'], 
                 17:[u'شكل',u'مشكولة',u'مشكول'], 
                 18:[u'صلم',u'صلماء',u'أصلم'], 
                 19:[u'طيّ',u'مطويّة',u'مطويّ'], 
                 20:[u'عصب',u'عصباء',u'أعصب'], 
                 21:[u'عضب',u'عضباء',u'أعضب'], 
                 22:[u'عقص',u'عقصاء',u'أعقص'], 
                 23:[u'عقل',u'معقولة',u'معقول'], 
                 24:[u'قبض',u'مقبوضة',u'مقبوض'], 
                 25:[u'قصر',u'مقصورة',u'مقصور'], 
                 26:[u'قصم',u'قصماء',u'أقصم'], 
                 27:[u'قطع',u'مقطوعة',u'مقطوع'], 
                 28:[u'قطف',u'مقطوفة',u'مقطوف'], 
                 29:[u'كفّ',u'مكفوفة',u'مكفوف'], 
                 30:[u'كبل',u'مكبولة',u'مكبول'], 
                 31:[u'نقص',u'منقوصة',u'منقوص'], 
                 32:[u'كسف',u'مكسوفة',u'مكسوف'], 
                 33:[u'وقص',u'موقوصة',u'موقوص'], 
                 34:[u'وقف',u'موقوفة',u'موقوف'],
                 35:[u'ثرم',u'ثرماء',u'أثرم'],
                 36:[u'إذالة وخبن',u'مذالة مخبونة',u'مذال مخبون'],
                 37:[u'إذالة وطيّ',u'مذالة مطويّة',u'مذال مطويّ'],
                 38:[u'إذالة وخبل',u'مذالة مخبولة',u'مذال مخبول'],
                 39:[u'خبن وقصر',u'مخبونة مقصورة',u'مخبون مقصور'], 
                 40:[u'خبن وحذف',u'مخبونة محذوفة',u'مخبون محذوف'],
                 41:[u'خبن وتسبيغ',u'مخبونة مسبّغة',u'مخبون مسبّغ'],
                 42:[u'إضمار وقطع',u'مضمرة مقطوعة',u'مضمر مقطوع'],
                 43:[u'إضمار وحذذ',u'مضمرة حذّاء',u'مضمر أحذّ'],
                 44:[u'إذالة وإضمار',u'مذالة مضمرة',u'مذال مضمر'],
                 45:[u'إذالة ووقص',u'مذالة موقوصة',u'مذال موقوص'],
                 46:[u'إذالة وخزل',u'مذالة خزلاء',u'مذال أخزل'], 
                 47:[u'إضمار وترفيل',u'مضمرة مرفّلة',u'مضمر مرفّل'],
                 48:[u'ترفيل ووقص',u'مرفّلة موقوصة',u'مرفّل موقوص'],
                 49:[u'ترفيل وخزل',u'مرفّلة خزلاء',u'مرفّل أخزل'],
                 50:[u'خبن ووقف',u'مخبونة موقوفة',u'مخبون موقوف'],
                 51:[u'طيّ ووقف',u'مطويّة موقوفة',u'مطويّ موقوف'],
                 52:[u'خبن وكسف',u'مخبونة مكسوفة',u'مخبون مكسوف'],
                 53:[u'طيّ وكسف',u'مكسوفة مطويّة',u'مكسوف مطويّ'],
                 54:[u'كسف وخبل',u'مكسوفة مخبولة',u'مكسوف مخبول'],
                 55:[u'خبل غير لازم',u'صحيحة دخلها خبل غير لازم',u'صحيح دخله خبل غير لازم'],
                 56:[u'خبن غير لازم',u'صحيحة دخلها خبن غير لازم',u'صحيح دخله خبن غير لازم'],
                 57:[u'كفّ غير لازم',u'صحيحة دخلها كفّ غير لازم',u'صحيح دخله كفّ غير لازم'],
                 58:[u'شكل غير لازم',u'صحيحة دخلها شكل غير لازم',u'صحيح دخله شكل غير لازم'],
                 59:[u'طيّ غير لازم',u'صحيحة دخلها طيّ غير لازم',u'صحيح دخله طيّ غير لازم'],
                 60:[u'إذالة وخبن غير لازم',u'مذالة دخلها خبن غير لازم',u'مذال دخله خبن غير لازم'],
                 61:[u'إذالة وطيّ غير لازم',u'مذالة دخلها طيّ غير لازم',u'مذال دخله طيّ غير لازم'],
                 62:[u'إذالة وخبل غير لازم',u'مذالة دخلها خبل غير لازم',u'مذال دخله خبل غير لازم'],
                 63:[u'قطع وخبن غير لازم',u'مقطوعة دخلها خبن غير لازم',u'مقطوع دخله خبن غير لازم'],
                 64:[u'قطف وقصر غير لازم',u'مقطوفة دخلها قصر غير لازم',u'مقطوف دخله قصر غير لازم'],
                 65:[u'قطف وقبض غير لازم',u'مقطوفة دخلها قبض غير لازم',u'مقطوف دخله قبض غير لازم'],
                 66:[u'عصب غير لازم',u'صحيحة دخلها عصب غير لازم',u'صحيح دخله عصب غير لازم'],
                 67:[u'إضمار غير لازم',u'صحيحة دخلها إضمار غير لازم',u'صحيح دخله إضمار غير لازم'],
                 68:[u'وقص غير لازم',u'صحيحة دخلها وقص غير لازم',u'صحيح دخله وقص غير لازم'],
                 69:[u'خزل غير لازم',u'صحيحة دخلها خزل غير لازم',u'صحيح دخله خزل غير لازم'],
                 70:[u'قطع وإضمار غير لازم',u'مقطوعة دخلها إضمار غير لازم',u'مقطوع دخله إضمار غير لازم'],
                 71:[u'إذالة وإضمار غير لازم',u'مذالة دخلها إضمار غير لازم',u'مذال دخله إضمار غير لازم'],
                 72:[u'إذالة ووقص غير لازم',u'مذالة دخلها وقص غير لازم',u'مذال دخله وقص غير لازم'],
                 73:[u'إذالة وخزل غير لازم',u'مذالة دخلها خزل غير لازم',u'مذال دخله خزل غير لازم'],
                 74:[u'ترفيل وإضمار غير لازم',u'مرفّلة دخلها إضمار غير لازم',u'مرفّل دخله إضمار غير لازم'],
                 75:[u'ترفيل ووقص غير لازم',u'مرفّلة دخلها وقص غير لازم',u'مرفّل دخله وقص غير لازم'],
                 76:[u'ترفيل وخزل غير لازم',u'مرفّلة دخلها خزل غير لازم',u'مرفّل دخله خزل غير لازم'],
                 77:[u'تسبيغ وخبن غير لازم',u'مسبّغة دخلها خبن غير لازم',u'مسبّغ دخله خبن غير لازم'],
                 78:[u'تسبيغ وكفّ غير لازم',u'مسبّغة دخلها كفّ غير لازم',u'مسبّغ دخله كفّ غير لازم'],
                 79:[u'تسبيغ وشكل غير لازم',u'مسبّغة دخلها شكل غير لازم',u'مسبّغ دخله شكل غير لازم'],
                 80:[u'حذف وخبن غير لازم',u'محذوفة دخلها خبن غير لازم',u'محذوف دخله خبن غير لازم'],
                 81:[u'قصر وخبن غير لازم',u'مقصورة دخلها خبن غير لازم',u'مقصور دخله خبن غير لازم'],
                 82:[u'وقف وخبن غير لازم',u'موقوفة دخلها خبن غير لازم',u'موقوف دخله خبن غير لازم'],
                 83:[u'قطع وطيّ غير لازم',u'مقطوعة دخلها طيّ غير لازم',u'مقطوع دخله طيّ غير لازم'],
                 84:[u'كسف وخبن غير لازم',u'مكسوفة دخلها خبن غير لازم',u'مكسوف دخله خبن غير لازم'],
                 85:[u'تشعيث غير لازم',u'صحيحة دخلها تشعيث غير لازم',u'صحيح دخله تشعيث غير لازم'],
                 86:[u'حذف غير لازم',u'صحيحة دخلها حذف غير لازم',u'صحيح دخله حذف غير لازم'],
                 87:[u'قبض غير لازم',u'صحيحة دخلها قبض غير لازم',u'صحيح دخله قبض غير لازم'],
                 88:[u'قطع غير لازم',u'صحيحة دخلها قطع غير لازم',u'صحيح دخله قطع غير لازم'],
                 89:[u'إذالة وقطع غير لازم',u'مذالة دخلها قطع غير لازم',u'مذال دخله قطع غير لازم'],
                 90:[u'ترفيل وخبن',u'مرفّلة مخبونة',u'مرفّل مخبون'],
                 91:[u'ترفيل وخبن وقطع غير لازم',u'مرفّلة مخبونة دخلها قطع غير لازم',u'مرفّل مخبون دخله قطع غير لازم'],
                 92:[u'عقل غير لازم',u'صحيحة دخلها عقل غير لازم',u'صحيح دخله عقل غير لازم'],
                 93:[u'عصب وكفّ غير لازم',u'عصباء دخلها كفّ غير لازم',u'أعصب دخله كفّ غير لازم'],
                 94:[u'عصب وقبض غير لازم',u'عصباء دخلها قبض غير لازم',u'أعصب دخله قبض غير لازم'],
                 95:[u'نقص غير لازم',u'صحيحة دخلها نقص غير لازم',u'صحيح دخله نقص غير لازم'],
                 }

Zihafat_ta3rif = { 
                 1:[u'إذالة',u'الإذالة\n زيادة حرف ساكن على الوتد المجموع في ضرب البيت، ومثاله: مستفعلنْ يدخلها الإذالة فتصير مستفعلان'],
                 2:[u'إضمار',u'الإضمار\nوهو تسكين ثاني التفعيلة إذا كان متحركاً وثاني سبب، ومثاله: مُتَفاعِلُنْ يدخلها الإضمار فتصير : مُتْفاعِلُنْ'], 
                 3:[u'بتر',u'البتر\nحذف سبب خفيف في عروض البيت أو ضربه ثم قطع الوتد الذي قبله، ومثاله: فعولن تدخلها علة البتر فتصير فعْ'], 
                 4:[u'ترفيل',u'الترفيل\nزيادة سبب خفيف على الوتد المجموع في ضرب البيت، ومثاله: فاعِلُنْ يدخلها الترفيل فتصير فاعلاتن'], 
                 5:[u'تسبيغ',u'التسبيغ\nزيادة حرف ساكن على السبب الخفيف فى آخر الضرب، ومثاله:فاعلاتن تدخلها  علة التسبيغ فتصير فاعلاتان'], 
                 6:[u'تشعيث',u'التشعيث\nوهو حذف الحرف الأول أو الثاني في الوتد المجموع، ومثاله: فاعلن تدخله علة التشعيث فيصير:فاعِنْ أو فالُنْ'], 
                 7:[u'ثلم',u'الثلم\nالثلم والخرم بمعنى واحد،وهو حذف الحرف الأول من الوتد المجموع في التفعيلة الأولى في الشطر، ويكون في فعولن و مفاعيلن ومفاعلتن'], 
                 8:[u'جمم',u'الجمم\nهو تغيير يلحق مفاعلتن في بحر الوافر وبيانه: يدخل  العقل  مفاعلتن فتصير مفاعتن بحذف اللام ثم يلحقها الخرم فتصير فاعتن'], 
                 9:[u'حذذ',u'الحذذ\nوهو حذف الوتد المجموع من آخر التفعيلة، ومثاله: متفاعلن يدخلها الحذذ فتصير :متفا'], 
                 10:[u'حذف',u'الحذف\nإسقاط السبب الخفيف من آخر التفعيلة في عروض البيت أو ضربه،ومثاله :مفاعيلن تدخلها  علة الحذف فتصير مفاعي'], 
                 11:[u'خبل',u'الخبل\nوهو زحاف مركب من الخبن والطي، ومثاله : مُسْتَفْعِلُنْ يدخلها الخبن أولاً فتصير: مُتَفْعِلُنْ ثم يعقبه الطي فتصير : مُتَعِلُنْ'], 
                 12:[u'خبن',u'الخبن\nوهو حذف  الحرف الثاني من التفعيلة متى كان ساكناً وثاني سبب، ومثاله : مُسْتَفْعِلُنْ يدخلها الخبن فتصير :مُتَفْعِلُنْ'], 
                 13:[u'خرب',u'الخرب\nهو حذف الحرف الأول و الحرف الأخير من التفعيلة الأولى في الشطر الأول، ومثاله: مفاعيلن يدخلها الخرب فتصير فاعيل كما في بحر الهزج'], 
                 14:[u'خرم',u'الخرم\nوهو حذف الحرف الأول من الوتد المجموع في التفعيلة الأولى في الشطر، ويكون في فعولن و مفاعيلن ومفاعلتن'], 
                 15:[u'خزل',u'الخزل\nوهو زحاف مركب من الإضمار والطي، ومثاله:مُتَفاعِلُنْ يدخلها الإطمار أولاً فتصير :مُتْفاعِلُن ثم يعقبه الطي :فتصير :مُتْفَعِلُنْ'], 
                 16:[u'شتر',u'الشتر\nإسقاط الحرف الأول والخامس من التفعيلة الأولى  في الشطر الأول أو الثاني من البيت ويختص به بحرا الهزج والمضارع'], 
                 17:[u'شكل',u'الشكل\nوهو زحاف مركب من الخبن والكف، ومثاله فاعِلاتُنْ يدخلها الخبن أولاً فتصير :فَعِلاتُنْ ثم يعقبه الكف فتصير :فَعِلاتُ'], 
                 18:[u'صلم',u'الصلم\nحذف  الوتد المفروق في عروض البيت أوضربه، ومثاله: مفعولات تدخلها علة الصلم فتصير مفعو'], 
                 19:[u'طيّ',u'الطي\nوهو حدف الحرف الرابع من التفعيلة متى كان ساكناً، ومثاله: مُتَفاعِلُنْ يدخلها  الطي فتصير :مُتَفَعِلُنْ'], 
                 20:[u'عصب',u'العصب\nوهو تسكين الحرف الخامس من التفعيلة متى كان متحركاً وثاني سبب، ومثاله: مُفاعَلَتُنْ يدخلها العصب فتصير : مُفاعَلْتُنْ'], 
                 21:[u'عضب',u'العضب\nويقع في بحر الوافر في التفعيلة الأولى من الشطر الأول فإذا خرمت مفاعلتن صارت فاعَلتن'], 
                 22:[u'عقص',u'العقص\nهو تغيير يلحق مفاعلتن في بحر الوافر وبيانه: يدخل العصب على مفاعلتن فتصير مفاعلْتن بتسكين اللام ثم يلحقها الكف فتصير مفاعلْت ثم يلحقها الخرم فتصير فاعلْتُ بتسكين اللام'], 
                 23:[u'عقل',u'العقل\nوهو حذف خامس التفعيلة متى كان متحركاً وثاني سبب ومثاله:مُفاعَلَتُنْ يدخلها زحاف العقل فتصير : مُفاعَتُنْ'], 
                 24:[u'قبض',u'القبض\nوهو حذف الحرف الخامس من التفعيلة متى كان ساكناً وثاني سبب، ومثاله:فَعولُنْ يدخلها زحاف القبض فتصير :فَعولُ'], 
                 25:[u'قصر',u'القصر\nحذف ساكن السبب الخفيف في عروض البيت أوضربه  وتسكين متحركه، ومثاله: فاعلاتُن تدخلها علة القصر فتصير فاعلاتْ'], 
                 26:[u'قصم',u'القصم\nهو تغيير يلحق مفاعلتن في بحر الوافر وبيانه: يدخل العصب على مفاعلتن فتصير مفاعلْتن بتسكين اللام ثم يلحقها الخرم فتصير فاعلْتن'], 
                 27:[u'قطع',u'القطع\nحذف ساكن الوتد المجموع  في عروض البيت أو ضربه وتسكين ما قبله، ومثاله: متفاعلن تدخله  علة القطع فيصير متفاعلْ'], 
                 28:[u'قطف',u'القطف\nإسقاط السبب الخفيف من آخر التفعيلة في عروض البيت أو ضربه وتسكين ماقبله، ومثاله: مفاعلَتن تدخلها  علة القطف فتصير :مفاعلْ'], 
                 29:[u'كفّ',u'الكف\nوهو حذف الحرف السابع من التفعيلة متى كان ساكناً وثاني سبب، ومثاله: مَفاعيلُنْ يدخلها زحاف الكف فتصير : مَفاعيلُ'], 
                 30:[u'كبل',u'مكبولة',u'مكبول'], 
                 31:[u'نقص',u'النقص\nوهوزحاف مركب من العصب والكف ،ومثاله مُفاعَلَتُنْ يدخلها العصب أولاً فتصير:مُفاعَلْتُنْ ثم يعقبه الكف فتصير:مُفاعَلْتُ'], 
                 32:[u'كسف',u'الكسف\nالكسف أو الكشف وهو حذف  آخر الوتد المفروق  في العروض أو الضرب، ومثاله: مفعولاتُ يدخلها الكسف فتصير: مغعولا'], 
                 33:[u'وقص',u'الوقص\nوهو حذف ثاني التفعيلة متى كان متحركاَ وثاني سبب، ومثاله: متَفاعلن يدخلها الوقص فتصير : مفاعلن'], 
                 34:[u'وقف',u'الوقف\nتسكين آخر الوتد المفروق في عروض البيت أو ضربه، ومثاله :مفعولاتُ تدخلها علة الوقف فتصير مفعولاتْ'],
                 35:[u'ثرم',u'الثرم\nوهو خرم فعولُ أي حذف أول متحرك فيها فتصير عولُ وتنقل إلى فعْلُ'],
                 36:[u'إذالة وخبن',u''],
                 37:[u'إذالة وطيّ',u''],
                 38:[u'إذالة وخبل',u''],
                 44:[u'إذالة وإضمار',u''],
                 45:[u'إذالة ووقص',u''],
                 46:[u'إذالة وخزل',u''], 
                 89:[u'إذالة وقطع',u''],
                 39:[u'خبن وقصر',u''], 
                 40:[u'خبن وحذف',u''],
                 41:[u'خبن وتسبيغ',u''],
                 50:[u'خبن ووقف',u''],
                 52:[u'خبن وكسف',u''],
                 63:[u'قطع وخبن',u''],
                 90:[u'ترفيل وخبن',u''],
                 42:[u'إضمار وقطع',u''],
                 43:[u'إضمار وحذذ',u''],
                 47:[u'إضمار وترفيل',u''],
                 48:[u'ترفيل ووقص',u''],
                 49:[u'ترفيل وخزل',u''],
                 51:[u'طيّ ووقف',u''],
                 53:[u'طيّ وكسف',u''],
                 54:[u'كسف وخبل',u''],
                 64:[u'قطف وقصر',u''],
                 65:[u'قطف وقبض',u''],
                 78:[u'تسبيغ وكفّ',u''],
                 79:[u'تسبيغ وشكل',u''],
                 83:[u'قطع وطيّ',u''],
                 93:[u'عصب وكفّ',u''],
                 94:[u'عصب وقبض ',u''],
                 }

#a التفعيلات العشر الرئيسة----------------------------------------------------  

Taf3ilat = {1:u'فَعُولُنْ', 
            2:u'فَاعِلُنْ', 
            3:u'مُسْتَفْعِلُنْ', 
            4:u'مَفَاعِيلُنْ', 
            5:u'فَاعِلَاتُنْ', 
            6:u'مُفَاعَلَتُنْ', 
            7:u'مُتَفَاعِلُنْ', 
            8:u'مَفْعُولَاتُ',
            9:u'مُسْتَفْعِ_لُنْ',  
            0:u'فَاعِ_لَاتُنْ', }

#a التغيرات الطارئة على التفعيلات-----------------------------------------------
#a   التغيرات عبارة عن قاموس مفاتيحه هي التفعيلات العشر الرئيسة  
#a   القيمة المقابلة لكل مفتاح هي قاموس التحولات التي تطرأ على التفعيلة  
#a   قاموس التحولات مفاتيحه الزحافات والعلل وقيمها هي صورة التفعيلة بعد التحول  
          
Changes = {
            1:{24:u'فَعُولُ',
              87:u'فَعُولُ', 
              25:u'فَعُولْ', 
              7:u'فَعْلُنْ', 
              35:u'فَعْلُ', 
              10:u'فَعَلْ',
              86:u'فَعَلْ', 
              3:u'فَعْ',},
           
            2:{12:u'فَعِلُنْ', 
              56:u'فَعِلُنْ', 
              27:u'فَعْلُنْ',
              88:u'فَعْلُنْ',
              1:u'فَاعَلَانْ',
              60:u'فَعِلَانْ',
              89:u'فَعْلَانْ',
              90:u'فَعِلَاتُنْ',
              91:u'فَعْلَاتُنْ',},
           
            3:{12:u'مَفَاعِلُنْ',
              56:u'مَفَاعِلُنْ', 
              83:u'فَاعِلُنْ', 
              19:u'مُفْتَعِلُنْ', 
              59:u'مُفْتَعِلُنْ',  
              11:u'فَعَلَتُنْ',
              55:u'فَعَلَتُنْ', 
              29:u'مُسْتَفْعِلُ', 
              17:u'مَفَاعِلُ', 
              27:u'مَفْعُولُنْ', 
              30:u'فَعُولُنْ',
              63:u'فَعُولُنْ', 
              1:u'مُسْتَفْعِلَانْ', 
              36:u'مُفَاعِلَانْ', 
              37:u'مُفْتَعِلَانْ', 
              38:u'فَعَلَتَانْ',
              60:u'مُفَاعِلَانْ', 
              61:u'مُفْتَعِلَانْ', 
              62:u'فَعَلَتَانْ',},
           
            4:{24:u'مَفَاعِلُنْ', 
              29:u'مَفَاعِيلُ', 
              57:u'مَفَاعِيلُ', 
              25:u'مَفَاعِيلْ', 
              10:u'فَعُولُنْ', 
              14:u'مَفْعُولُنْ', 
              16:u'فَاعِلُنْ', 
              13:u'مَفْعُولُ',},
           
            5:{12:u'فَعِلَاتُنْ',
              56:u'فَعِلَاتُنْ', 
              29:u'فَاعِلَاتُ',
              57:u'فَاعِلَاتُ', 
              17:u'فَعِلَاتُ',
              58:u'فَعِلَاتُ',
              25:u'فَاعِلَانْ',
              39:u'فَعِلَانْ',
              81:u'فَعِلَانْ',
              10:u'فَاعِلُنْ',
              40:u'فَعِلُنْ',
              80:u'فَعِلُنْ',
              3:u'فَعْلُنْ',
              6:u'مَفْعُولُنْ',
              85:u'مَفْعُولُنْ',
              5:u'فَاعِلَيَّانْ',
              41:u'فَعِلَيَّانْ',
              77:u'فَعِلَيَّانْ',
              78:u'فَاعِلَاتُنْ',
              79:u'فَعِلَاتُنْ',}, 
           
            6:{20:u'مَفَاعِيلُنْ',
              66:u'مَفَاعِيلُنْ',
              23:u'مَفَاعِلُنْ', 
              31:u'مَفَاعِيلُ',
              94:u'مَفَاعِلُنْ', 
              93:u'مَفَاعِيلُ', 
              92:u'مَفَاعِلُنْ', 
              95:u'مَفَاعِيلُ',
              28:u'فَعُولُنْ', 
              64:u'فَعُولْ',
              65:u'فَعُولُ',
              21:u'مَفْتَعِلُنْ', 
              26:u'مَفْعُولُنْ', 
              8:u'فَاعِلُنْ', 
              22:u'مَفْعُولُ',},
           
            7:{2:u'مُسْتَفْعِلُنْ',
              67:u'مُسْتَفْعِلُنْ', 
              33:u'مُفَاعِلُنْ',
              68:u'مُفَاعِلُنْ', 
              15:u'مُفْتَعِلُنْ',
              69:u'مُفْتَعِلُنْ', 
              27:u'فَعِلَاتُنْ', 
              42:u'مَفْعُولُنْ', 
              70:u'مَفْعُولُنْ',
              9:u'فَعِلُنْ', 
              43:u'فَعْلُنْ', 
              1:u'مُتَفَاعِلَانْ', 
              44:u'مُسْتَفْعِلَانْ', 
              71:u'مُسْتَفْعِلَانْ',
              45:u'مُفَاعِلَانْ',
              72:u'مُفَاعِلَانْ', 
              46:u'مُفْتَعِلَانْ', 
              73:u'مُفْتَعِلَانْ', 
              4:u'مُتَفَاعِلَاتُنْ', 
              47:u'مُسْتَفْعِلَاتُنْ', 
              48:u'مَفَاعِلَاتُنْ', 
              49:u'مُفْتَعِلَاتُنْ',
              74:u'مُسْتَفْعِلَاتُنْ', 
              75:u'مَفَاعِلَاتُنْ', 
              76:u'مُفْتَعِلَاتُنْ',},
           
            8:{12:u'فَعُولَاتُ', 
              19:u'فَاعِلَاتُ', 
              11:u'فَعِلَاتُ', 
              34:u'مَفْعُولَانْ', 
              50:u'فَعُولَانْ', 
              82:u'فَعُولَانْ', 
              51:u'فَاعِلَانْ', 
              32:u'مَفْعُولُنْ', 
              52:u'فَعُولُنْ', 
              84:u'فَعُولُنْ',
              53:u'فَاعِلُنْ', 
              54:u'فَعِلُنْ', 
              18:u'فَعْلُنْ',},
           
           9:{12:u'مَفَاعِلُنْ', 
              56:u'مَفَاعِلُنْ',
              29:u'مُسْتَفْعِلُ', 
              17:u'مَفَاعِلُ', 
              57:u'مُسْتَفْعِلُ', 
              58:u'مَفَاعِلُ', 
              39:u'فَعُولُنْ',  
              36:u'مُفَاعِلَانْ',},
           
           0:{29:u'فَاعِلَاتُ',
              57:u'فَاعِلَاتُ',},
            }

#a البحور الشعرية----------------------------------------------------------------

Elbehor = {
            1:u'الطَّوِيل',
            2:u'المَدِيد',
            3:u'البَسِيط',
            4:u'الوافِر',
            5:u'الكامِل',
            6:u'الهَزَج',
            7:u'الرَجَز',
            8:u'الرَّمَل',
            9:u'السَّريع',
            10:u'المُنْسَرِح',
            11:u'الخفيف',
            12:u'المضارع',
            13:u'المقتضب',
            14:u'المجتث',
            15:u'المتقارب',
            16:u'المتدارك',
             }


#a استعمالات البحور------------------------------------------------------------------
#a الاستعمال هو استعمال البحر تاما بجميع تفعيلاته أو بإنقاص بعضها  

Usage = {
         1:u'تامّ', 
         2:u'مجزوء', 
         3:u'مشطور', 
         4:u'منهوك', 
         5:u'مخلّع', 
         }

#a التفاصيل--------------------------------------------------------------------------
#a   التفاصيل عبارة عن قاموس مفاتيحه تشير إلى البحور
#a   القيمة المقابله للمفتاح عبارة عن قائمة بها قائمة ثم قاموس ثم قائمة إن وجدت
#a   القائمة الأولى بها استعمالات البحر تاما أو مجزوءا .....إلخ
#a   القائمة الأخيرة هي قائمة الزحافات الخاصة بالتفعيلة الأولى إن وجدت
#a   القاموس مفاتيحه أرقام تفعيلات الحشو بدون تكرار والقيم المقابلة قوائم بالجوازات الممكنة
#a   وكل استعمال من الاستعمالات في القائمة الأولى عبارة قائمة أول عنصر فيها هو نوع الاستعمال
#a   أما ثاني عنصر فهو تمثيل لوزن الاستعمال في الدائرة العروضية
#a   أما باقي العناصر فكل عنصر فيها يمثل عروضا لهذا الاستعمال
#a    العروض عبارة عن قائمة تحوي العروض كعنصر أول وأضربه هي باقي العناصر
#a   العروض المسبوقة بعلامة السالب هي ما يجوز في التصريع فقط

Details = { 
            1:[[[1,'1414*1414',[24,0,24,10],[-100,0],[-10,10]]],
               {1:[0,24],4:[0,24,29]},[7,35]],
            2:[[[2,'525*525',[0,0,56],[56,0,56],[57,0,56],[58,0,56],[10,10,25,3],
                 [40,40,3],[-3,3],[-25,25]],
                 [3,'52*52',[0,0]]],
               {5:[0,12,29,17],2:[0,12]}],
            3:[[[1,'3232*3232',[12,12,27]],
               [2,'323*323',[0,0,56,59,1,60,61,62,27],[56,0,56,59,1,60,61,62,27],
                [59,0,56,59,1,60,61,62,27],[27,63,27],[63,63,27],[-1,1,60,61,62],
                [-60,1,60,61,62],[-61,1,60,61,62],[-62,1,60,61,62]],
               [5,'323*323',[30,30]]],
               {3:[0,12,19,11],2:[0,12]}],
            4:[[[1,'666*666',[28,28,64],[65,28,64],[64,28,64]],
               [2,'66*66',[0,0,20],[66,0,20],[92,0,20],[95,0,20]]],
               {6:[0,20,23,31],},[8,21,22,26]],
            5:[[[1,'777*777',[0,0,27,43,67,68,69,70],[67,0,27,43,67,68,69,70],
                 [68,0,27,43,67,68,69,70],[69,0,27,43,67,68,69,70],[9,9,43],[-43,43],[-27,27,70],[-70,27,70]],
                [2,'77*77',[0,0,1,4,27,67,68,69,70,71,72,73,74,75,76],
                 [67,0,1,4,27,67,68,69,70,71,72,73,74,75,76],[68,0,1,4,27,67,68,69,70,71,72,73,74,75,76],
                 [69,0,1,4,27,67,68,69,70,71,72,73,74,75,76],[-27,27,70],[-70,27,70],
                 [-4,4,74,75,76],[-74,4,74,75,76],[-75,4,74,75,76],[-76,4,74,75,76],
                 [-1,1,71,72,73],[-71,1,71,72,73],[-72,1,71,72,73],[-73,1,71,72,73]]],
               {7:[0,2,33,15],}], 
            6:[[[2,'44*44',[0,0,10],[57,0,10],[-10,10]]],
               {4:[0,24,29],},[13,14,16]],
            7:[[[1,'333*333',[0,0,27,55,56,59,63],[55,0,27,55,56,59,63],
                 [56,0,27,55,56,59,63],[59,0,27,55,56,59,63],[-27,27,63],[-63,27,63]],
               [2,'33*33',[0,0,55,56,59],[55,0,55,56,59],[56,0,55,56,59],[59,0,55,56,59]],
               [3,'333',[0,],[55,],[56,],[59,]],
               [4,'33',[0,],[55,],[56,],[59,]]],
               {3:[0,12,19,11],}],
            8:[[[1,'555*555',[10,0,10,25,56,80,81],[80,0,10,25,56,80,81],[-100,0,56],[-56,0,56]
                 ,[-25,25,81],[-81,25,81]],
                [2,'55*55',[0,0,5,10,56,77,78,79,80],[56,0,5,10,56,77,78,79,80],
                 [57,0,5,10,56,77,78,79,80],[58,0,5,10,56,77,78,79,80],[-10,10,80],[-80,10,80],
                 [-5,5,77,78,79],[-77,5,77,78,79],[-78,5,77,78,79],[-79,5,77,78,79]]],
               {5:[0,12,17,29],}],
            9:[[[1,'338*338',[53,53,51,18],[54,54,18],[-18,18],[-51,51]],
                [3,'338',[34,82]]],
               {3:[0,12,19,11]}],
            10:[[[1,'383*383',[0,19,27,63,83],[56,19,27,63,83],[59,19,27,63,83],
                  [-27,27,63,83],[-63,27,63,83],[-83,27,63,83]],
                 [4,'38',[34,],[32,],[82,],[84,]]],
                {3:[0,12,19,11],8:[0,12,19]}],
            11:[[[1,'595*595',[0,0,56,10,80,85],[57,0,56,10,80,85],[58,0,56,10,80,85],[56,0,56,10,80,85],
                  [10,80,10],[80,80,10],[-85,85]],
                 [2,'59*59',[0,0,39,56],[56,0,39,56],[57,0,39,56],[58,0,39,56],[-39,39]]],
                {5:[0,12,17,29],9:[0,12,17,29]}],
            12:[[[2,'40*40',[0,0],[57,0]]],
                {4:[0,24,29],},[13,16]],
            13:[[[2,'83*83',[19,19]]],
                {8:[0,12,19],}],
            14:[[[2,'95*95',[0,0,56],[56,0,56],[57,0,56],[58,0,56]]],
                {9:[0,12,17,29],5:[0,12,17,29]}],
            15:[[[1,'1111*1111',[0,0,25,10,3,86],[86,0,25,10,3,86],[87,0,25,10,3,86],[-3,3],[-25,25]],
                 [2,'111*111',[10,10,3],[-3,3]]],
                {1:[0,24],},[7,35]],
            16:[[[1,'2222*2222',[0,0,56,88],[56,0,56,88],[88,0,56,88]],
                 [2,'222*222',[0,0,1,90,56,88,60,89,91],[56,0,1,90,56,88,60,89,91],
                  [88,0,1,90,56,88,60,89,91],[-1,1,60,89],[-60,1,60,89],[-89,1,60,89],
                  [-90,90,91],[-91,90,91]]],
                {2:[0,12,27],}],
             }


#a قائمة بالبحور------------------------------------------------------------

def all_baher():
    all_baher = []
    for a in Elbehor.keys():
            all_baher.append([Elbehor[a],a])
    return all_baher

#a صور البحور------------------------------------------------------

def formats_taf3ilat(a, v, f=False):
    taf3ilah = []
    for c in range(len(Details[a][1][v])):
        if Details[a][1][v][c] == 0:
            taf = Taf3ilat[v]
            taf3ilah.append([taf, u'سالمة'])
        else:
            zihaf = Zihafat_3ilal[Details[a][1][v][c]][1]
            new_format = Changes[v][Details[a][1][v][c]]
            taf3ilah.append([new_format, zihaf])
    if len(Details[a]) > 2 and f == True:
        for d in range(len(Details[a][2])):
            zihaf = Zihafat_3ilal[Details[a][2][d]][1]
            new_format = Changes[v][Details[a][2][d]]
            taf3ilah.append([new_format, zihaf])
    return taf3ilah

def formats_padding(arodh_ls, a):
    global z
    all_padding = []
    taf3ila1 = [[u'',u''],]
    taf3ila2 = [[u'',u''],]
    taf3ila3 = [[u'',u''],]
    taf3ila4 = [[u'',u''],]
    taf3ila5 = [[u'',u''],]
    taf3ila6 = [[u'',u''],]
    txt = arodh_ls[-1]
    arodh = [arodh_ls[0],arodh_ls[1]]
    if len(arodh_ls) == 5:
        dharb = [arodh_ls[2],arodh_ls[3]]
    else:
        dharb = [u'',u'']
    taf3ila1 = formats_taf3ilat(a, int(txt[0]), True)
    if len(txt) > 1:
        taf3ila2 = formats_taf3ilat(a, int(txt[1]))
    if len(txt) > 2:
        taf3ila3 = formats_taf3ilat(a, int(txt[2]))
    if len(txt) > 3:
        taf3ila4 = formats_taf3ilat(a, int(txt[3]))
    if len(txt) > 4:
        taf3ila5 = formats_taf3ilat(a, int(txt[4]))
    if len(txt) > 5:
        taf3ila6 = formats_taf3ilat(a, int(txt[5]))
    ls = list(itertools.product([[arodh, dharb],], taf3ila1, taf3ila2, taf3ila3, taf3ila4, taf3ila5, taf3ila6)) 
#    for p in ls:
#        cur.execute('INSERT INTO awzan VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
#                             (z, a, u'', u'', u'',p[0][0][1],p[0][0][0],p[0][1][1],p[0][1][0],
#                              p[1][0],p[1][1],p[2][0],p[2][1],p[3][0],p[3][1],
#                              p[4][0],p[4][1],p[5][0],p[5][1],p[6][0],p[6][1]))
#        con.commit()
#        z += 1
#        print z
           
    return all_padding

def a3aridh_tasri3(a, b, txt):
    return
                        
def formats_a3aridh(a, b, txt):
    all_a3aridh = []
    for c in range(2, len(Details[a][0][b])):
        taf3ilat = Details[a][0][b][1]
        if len(taf3ilat) > 3:
            taf3ilat = taf3ilat[:(len(taf3ilat)/2)-1]+taf3ilat[(len(taf3ilat)/2)+1:-1]
        else:
            taf3ilat = taf3ilat[:-1]
        if Details[a][0][b][c][0] < 0:
            v1 = (Details[a][0][b][c][0])*(-1)
            t1 = u' وتجوز في التصريع فقط'
        else:
            v1 = Details[a][0][b][c][0]
            t1 = u'' 
        arodh = Usage[Details[a][0][b][0]] 
        arodh += u'ة '+Zihafat_3ilal[v1][1]+t1
        if len(txt) > 3:
            for e in range(1, len(Details[a][0][b][c])):
                dharb = Zihafat_3ilal[Details[a][0][b][c][e]][2]
                cc = Details[a][0][b][c][e]
                d1 = (len(txt)/2)-1 
                if v1 != 0 and v1 != 100:
                    text_arod = Changes[int(txt[d1])][v1]
                else:
                    text_arod = Taf3ilat[int(txt[d1])]
                d2 = len(txt)-1 
                if cc != 0:
                    text_dharb = Changes[int(txt[d2])][cc]
                else:
                    text_dharb = Taf3ilat[int(txt[d2])]
                all_a3aridh.append([arodh,text_arod,dharb,text_dharb,taf3ilat])
        else:
            arodh += u' وهي الضرب نفسه'
            d3 = len(txt)-1 
            if v1 != 0:
                text_arod_dharb = Changes[int(txt[d3])][v1]
            else:
                text_arod_dharb = Taf3ilat[int(txt[d3])]
            all_a3aridh.append([arodh,text_arod_dharb,taf3ilat])
    return all_a3aridh

def formats_behor():
    for a in range(1,17):
        for b in range(len(Details[a][0])):
            txt = Details[a][0][b][1]
            a3aridh = formats_a3aridh(a, b, txt)
            for arodh in a3aridh:
                formats_padding(arodh, a)

#a لايجوز اجتماع خمس متحركات


#a ما خالف لفظه كتابته--------------------------------------------------------

list_not_rw = {u'إِلَه':u'إِلَاه',u'الرَّحْمَن':u'ارْرَحْمَان',u'لَكِن':u'لَاكِن',
             u'سَمَوَات':u'سَمَاوَات',u'هَذَا':u'هَاذَا',u'هَذِه':u'هَاذِه',u'هَؤُلَاء':u'هَاؤُلَاء',
             u'ذَلِك':u'ذَالِك',u'دَاوُد':u'دَاوُود',u'طَاوُس':u'طَاوُوس',u'مِائَة':u'مِئَة',
             u'أَنَا ':u'أَنَ ',u'أُولَات':u'أُلَات',u'أُولُو':u'أُلُو',u'أُولِي':u'أُلِي',
             u'آ':u'أَا',u'هَذِي':u'هَاذِي',u'اَ':u'َا',u'اً':u'ً',u'ىَ':u'َى',
             u'ىً':u'ً',u'ًا':u'ً',u'ًى':u'ً',u'هَهُنَا':u'هَاهُنَا',u'هَكَذَا':u'هَاكَذَا',
             u'هَذَيْن':u'هَاذَيْن',
             u'اللَّهَ ':u'الْلَاهَ ',u'اللَّهُ ':u'الْلَاهُ ',u'اللَّهِ ':u'الْلَاهِ ',
             u'للَّهِ ':u'لْلَاهِ ',u'اللَّهُمّ':u'الْلَاهُمّ',u'اللهِ ': u'الْلَاهِ ',
             u'عَمْرٍو':u'عَمْرِنْ',u'عَمْرٌو':u'عَمْرُنْ',u'عَمْرِو':u'عَمْرِ',u'عَمْرَو':u'عَمْرَ',
             u'عَمْرُو':u'عَمْرُ',
             u'عَمْروٍ':u'عَمْرِنْ',u'عَمْروٌ':u'عَمْرُنْ',u'عَمْروِ':u'عَمْرِ',u'عَمْروَ':u'عَمْرَ',
             u'عَمْروُ':u'عَمْرُ',
             u'َّ':u'2َّ', u'ُّ':u'2ُّ', u'ِّ':u'ِّ'}

def not_rw(text):
    for a in list_not_rw.keys():
        text = re.sub(a, list_not_rw[a], text)
    return text
    
#a إشباع هاء الضمير-----------------------------------------------------------------

def ishbaa_ha(text):
    ls = text.split(' ')
    txt = u''
    for a in ls:
        if len(a) >= 3: 
            if not daw_araby.isHaraka(a[-3]) or daw_araby.isSukun(a[-3]):
                pass
            else:
                if a[-2:] == u'هُ':
                    a += u'و'
                if a[-2:] == u'هِ':
                    a += u'ي'
        txt += a+' ' 
    txt = txt.strip()
    return txt
    
#a إشباع ميم الضمير-----------------------------------------------------------------

def ishbaa_mim(text):
    ls = text.split(' ')
    txt = u''
    for a in ls:
        if len(a) > 3: 
            if a[-4:] in [u'كُمُ', u'كِمُ', u'هُمُ', u'هِمُ', u'تُمُ']:
                a += u'و'
        txt += a+' ' 
    txt = txt.strip()
    return txt

#a إشباع حركة الروي-----------------------------------------------------------------

def itlak(text):
    d = {daw_araby.FATHA:daw_araby.ALEF, 
         daw_araby.DAMMA:daw_araby.WAW, 
         daw_araby.KASRA:daw_araby.YEH}
    if text[-1] in d.keys():
        text = text+d[text[-1]]
    return text

#a إلغاء الشدة في الأخير-----------------------------------------------------------------

def shadda_end(text):
    if text[-1] == daw_araby.SHADDA:
        text = text[:-1]
    elif text[-2:] == daw_araby.SHADDA+daw_araby.SUKUN:
        text = text[:-2]
    return text

#a شكل الحرف الواقع قبل الألف بالفتحة-----------------------------------------------------------------
#FIXME
def tashkil_plus(text):
    txt = text
    s = 0
    for a in range(1,len(text)):
        if text[a] == daw_araby.ALEF and\
        text[a-1] not in daw_araby.HARAKAT and\
        text[a-1] != u' ':
            txt = txt[:a+s]+daw_araby.FATHA+text[a+s:]
            s += 1
    return txt
    
#a فك التنوين----------------------------------------------

def tanwin(text):
    txt = u''
    for a in range(len(text)):
        if a < len(text)-2:
            if daw_araby.DAMMATAN == text[a]:
                if text[a+2] == daw_araby.ALEF or \
                text[a+2] == daw_araby.ALEF_WASLA:
                    txt += daw_araby.DAMMA+u'نِ'
                else: txt += daw_araby.DAMMA+u'نْ'
            elif daw_araby.FATHATAN == text[a]:
                if text[a+2] == daw_araby.ALEF or \
                text[a+2] == daw_araby.ALEF_WASLA:
                    txt += daw_araby.FATHA+u'نِ'
                else: txt += daw_araby.FATHA+u'نْ'
            elif daw_araby.KASRATAN == text[a]:
                if text[a+2] == daw_araby.ALEF or \
                text[a+2] == daw_araby.ALEF_WASLA:
                    txt += daw_araby.KASRA+u'نِ'
                else: txt += daw_araby.KASRA+u'نْ'
            else:
                txt += text[a]
        else:
            if daw_araby.DAMMATAN == text[a]:
                txt += daw_araby.FATHA+u'نْ'
            elif daw_araby.FATHATAN == text[a]:
                txt += daw_araby.FATHA+u'نْ'
            elif daw_araby.KASRATAN == text[a]:
                txt += daw_araby.KASRA+u'نْ'
            else:
                txt += text[a]
    return txt

#a تقطيع النص إلى مقاطع صوتية------------------------------
#a المقطع الصوتي عبارة عن الحرف الصامت وحركته القصيرة
#a حرف المد عبارة عن مقطع ساكن

def syllable(text):
    lst = []
    ls = text.split(' ')
    for a in ls:
        l = []
        for b in range(len(a)):
            if daw_araby.isHaraka(a[b]): continue
            if b == len(a)-1: 
                l.append([a[b], 0])
                continue
            if daw_araby.isHaraka(a[b+1]):
                if daw_araby.isSukun(a[b+1]): c = 0
                else: c = 1
                l.append([a[b:b+2], c])
            else: l.append([a[b], 0])
        lst.append(l)
    return lst

#a التحليل-------------------------------------------------

def scan_verse(text, v=0):
    text = re.sub(' +', ' ', text)
    #text = re.sub('_', '', text)
    text = daw_araby.stripTatweel(text)
    text = shadda_end(text)
    text = not_rw(text)
    text = daw_araby.take_apart_tense(text)
    if v == 0:
        text = ishbaa_ha(text)
        text = ishbaa_mim(text)
    #text = tashkil_plus(text)
    text = tanwin(text)
    text = itlak(text)
    ls = syllable(text)
    txt = u''+ls[0][0][0]
    wazn = '1'
    for a in range(len(ls)):
        for c in range(len(ls[a])):
            if a == 0 and c == 0: continue
            if a < len(ls)-1:
                if c < len(ls[a])-1:
                    if ls[a][c][1] == 0 and ls[a][c+1][1] == 0:
                        continue
                    else: 
                        txt += ls[a][c][0]
                        wazn += str(ls[a][c][1])
                else:
                    if ls[a][c][1] == 0 and ls[a+1][0][1] == 0:
                        continue
                    else: 
                        txt += ls[a][c][0]
                        wazn += str(ls[a][c][1])
            else:
                if c < len(ls[a])-2:
                    if ls[a][c][1] == 0 and ls[a][c+1][1] == 0:
                        continue
                    else: 
                        txt += ls[a][c][0]
                        wazn += str(ls[a][c][1])
                else:
                    txt += ls[a][c][0]
                    wazn += str(ls[a][c][1])
        txt += u' '
    if wazn[-1] == '1':
        wazn += '0'
    takti3 = re.sub('1',u'/', wazn)
    return txt, takti3, wazn

#a الكتابة العروضية----------------------------------------

def writing_spoken(text, v):
    txt, takti3, wazn = scan_verse(text, v)
    return txt

#a الكتابة التقطيعية---------------------------------------

def writing_scan(text, v):
    txt, takti3, wazn = scan_verse(text, v)
    return takti3

#a الوزن---------------------------------------

def writing_wazn(text, v):
    txt, takti3, wazn = scan_verse(text, v)
    return wazn

#a أيجاد البحور المحتملة-----------------------------------

def meter_verse(text):
    result = myawzan.meter_verse(text)
    return result
