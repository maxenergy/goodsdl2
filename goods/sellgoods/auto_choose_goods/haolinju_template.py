# -*- coding:utf-8 -*-

import pymysql
import datetime
import os,django
import main.import_django_settings

from django.db import connections

origin_choose = ((1284, '3598', '6921168558049', '050203', 9900, 2026210), (1284, '3598', '6921581540102', '050302', 7700, 2026864), (1284, '3598', '6954767423579', '050402', 7220, 2019634), (1284, '3598', '6952675321123', '100301', 6400, 2032362), (1284, '3598', '6952675337735', '100303', 5800, 2034831), (1284, '3598', '6921168520015', '050102', 5600, 2004092), (1284, '3598', '6932571040007', '020201', 5520, 2025102), (1284, '3598', '6921168559176', '050103', 5400, 2033756), (1284, '3598', '6921168509256', '050101', 5400, 2004083), (1284, '3598', '6971949915585', '050204', 5280, 2044245), (1284, '3598', '20455088', '160202', 5280, 2045508), (1284, '3598', '6970725072351', '020402', 5200, 2041833), (1284, '3598', '6907992500942', '030101', 5100, 2009767), (1284, '3598', '6970399920415', '050104', 5000, 2043574), (1284, '3598', '6921355230550', '020101', 4800, 2038979), (1284, '3598', '6954767412573', '050402', 4560, 2004476), (1284, '3598', '6901826002930', '080204', 4500, 2044464), (1284, '3598', '6921581596048', '050204', 4500, 2004998), (1284, '3598', '6920202866737', '050502', 4500, 2004377), (1284, '3598', '6921581540140', '050302', 4400, 2028397), (1284, '3598', '6922279401927', '070407', 4200, 2032246), (1284, '3598', '6901236341308', '090502', 4080, 2035517), (1284, '3598', '6971140650087', '050302', 3960, 2045552), (1284, '3598', '856528008543', '120301', 3900, 2044008), (1284, '3598', '4901301262875', '090301', 3900, 2035494), (1284, '3598', '6957978700019', '020402', 3900, 2028823), (1284, '3598', '6940211889602', '020103', 3900, 2017286), (1284, '3598', '6922255451427', '050101', 3900, 2026253), (1284, '3598', '6970551560084', '090505', 3900, 2042689), (1284, '3598', '6943290507542', '160201', 3600, 2037707), (1284, '3598', '6922577727156', '020101', 3600, 2042337), (1284, '3598', '6917878056197', '050602', 3480, 2040855), (1284, '3598', '6932571040267', '020201', 3450, 2037196), (1284, '3598', '6922577722717', '020101', 3400, 2035797), (1284, '3598', '6932529211107', '050501', 3300, 2009198), (1284, '3598', '6922577726258', '020101', 3300, 2041517), (1284, '3598', '20453237', '160201', 3200, 2045323), (1284, '3598', '6935284415650', '100303', 3000, 2044196), (1284, '3598', '6923520901012', '020401', 3000, 2038489), (1284, '3598', '6940735448880', '080204', 3000, 2040664), (1284, '3598', '6970725071958', '020401', 3000, 2041826), (1284, '3598', '6901209258022', '030101', 3000, 2045293), (1284, '3598', '6970399920132', '050204', 3000, 2036329), (1284, '3598', '6971860060395', '070202', 2970, 2045235), (1284, '3598', '6928494806455', '020101', 2900, 2041192), (1284, '3598', '4891028705949', '050205', 2800, 2034697), (1284, '3598', '6931023280275', '020202', 2800, 2021927), (1284, '3598', '6970725075512', '020401', 2760, 2041824), (1284, '3598', '6932571040069', '020201', 2760, 2025909), (1284, '3598', '6971897494521', '020101', 2670, 2045006), (1284, '3598', '6917878030623', '050602', 2600, 2021662), (1284, '3598', '6921317944150', '050202', 2600, 2045324), (1284, '3598', '6912504939059', '090505', 2600, 2031681), (1284, '3598', '6917536014026', '070103', 2600, 2029278), (1284, '3598', '6935036483630', '020403', 2560, 2045611), (1284, '3598', '6928494805267', '020101', 2560, 2032525), (1284, '3598', '6923520901203', '020401', 2500, 2043260), (1284, '3598', '6970399920057', '050104', 2500, 2043573), (1284, '3598', '6918551811423', '010102', 2500, 2028900), (1284, '3598', '6925303730574', '050702', 2500, 2023591), (1284, '3598', '6927462202060', '070206', 2450, 2026853), (1284, '3598', '8802521122764', '040503', 2450, 2044872), (1284, '3598', '6906907907012', '050402', 2450, 2021612), (1284, '3598', '6938866531939', '050703', 2400, 2042847), (1284, '3598', '6921168593569', '050204', 2400, 2034688), (1284, '3598', '6921168593552', '050203', 2400, 2034689), (1284, '3598', '6943290503698', '170202', 2400, 2041038), (1284, '3598', '6954767410708', '050402', 2400, 2045108), (1284, '3598', '6970399920118', '050204', 2400, 2036330), (1284, '3598', '6943290500666', '170201', 2400, 2033797), (1284, '3598', '6907992515243', '030301', 2360, 2044075), (1284, '3598', '6922711403977', '020401', 2360, 2044032), (1284, '3598', '69025143', '140302', 2300, 2014305), (1284, '3598', '6923450657638', '140302', 2300, 2023341), (1284, '3598', '6923450656181', '140302', 2300, 2011017), (1284, '3598', '6970725073310', '020404', 2300, 2045605), (1284, '3598', '8000380005963', '140101', 2300, 2030071), (1284, '3598', '6922330911358', '170101', 2300, 2035555), (1284, '3598', '4901326013285', '100402', 2250, 2040026), (1284, '3598', '6921355220094', '020102', 2250, 2037283), (1284, '3598', '6922330913222', '170201', 2250, 2042496), (1284, '3598', '6940935200264', '100504', 2200, 2030321), (1284, '3598', '084501446314', '140101', 2200, 2006326), (1284, '3598', '6931286060843', '100202', 2200, 2036240), (1284, '3598', '6943290504442', '170201', 2200, 2031364), (1284, '3598', '6952522800047', '020101', 2100, 2026686), (1284, '3598', '6921355221381', '030101', 2100, 2003293), (1284, '3598', '6924513908551', '140302', 2080, 2044168), (1284, '3598', '6920202888883', '050502', 2040, 2004353), (1284, '3598', '6932005205149', '020302', 2000, 2042874), (1284, '3598', '6944697600744', '160202', 2000, 2036441), (1284, '3598', '6924160714017', '100304', 2000, 2036717), (1284, '3598', '4897022620516', '140301', 1990, 2041501), (1284, '3598', '6932005206696', '020302', 1980, 2044985), (1284, '3598', '6901757301805', '100301', 1980, 2022919), (1284, '3598', '6957978700262', '020401', 1950, 2028820), (1284, '3598', '6902890234487', '020401', 1950, 2022117), (1284, '3598', '6932005203077', '170201', 1950, 2037993), (1284, '3598', '6920584471017', '030101', 1950, 2008982), (1284, '3598', '8858702410823', '100201', 1950, 2032070), (1284, '3598', '6903148258064', '090301', 1900, 2043150), (1284, '3598', '5060072080701', '090301', 1900, 2036982), (1284, '3598', '6954767442075', '050402', 1900, 2004488), (1284, '3598', '8809010179605', '090301', 1900, 2033700), (1284, '3598', '6970870270534', '050601', 1850, 2045087), (1284, '3598', '6947929617398', '140101', 1800, 2043224), (1284, '3598', '6954767417684', '050401', 1800, 2044177), (1284, '3598', '6923520900909', '020401', 1800, 2038490), (1284, '3598', '6970324020036', '040401', 1800, 2035960), (1284, '3598', '6939728988236', '020101', 1800, 2044856), (1284, '3598', '6940735434456', '080204', 1800, 2036870), (1284, '3598', '6932571026278', '020101', 1800, 2042336), (1284, '3598', '6932571026285', '020101', 1800, 2042335), (1284, '3598', '6970399920972', '020101', 1780, 2045292), (1284, '3598', '6924743915763', '100101', 1780, 2027601), (1284, '3598', '6924743915770', '100101', 1780, 2027602), (1284, '3598', '6901209212215', '020101', 1780, 2045351), (1284, '3598', '4710094106118', '050702', 1760, 2044894), (1284, '3598', '40144078', '140101', 1750, 2045149), (1284, '3598', '6921317905014', '050202', 1750, 2040681), (1284, '3598', '6931023280268', '020202', 1750, 2021928), (1284, '3598', '8858279005835', '140101', 1700, 2044455), (1284, '3598', '6941722519217', '080103', 1700, 2045386), (1284, '3598', '8888077110004', '140103', 1690, 2044915), (1284, '3598', '6971057800018', '010101', 1680, 2044387), (1284, '3598', '6971539840563', '100301', 1680, 2045306), (1284, '3598', '6923450664889', '140302', 1680, 2042491), (1284, '3598', '6932005206474', '170101', 1650, 2044731), (1284, '3598', '6971949918272', '050302', 1650, 2045556), (1284, '3598', '6971949918210', '050302', 1650, 2045555), (1284, '3598', '6934660559216', '090301', 1650, 2040111), (1284, '3598', '6943290508426', '170202', 1650, 2026470), (1284, '3598', '6970182590344', '160101', 1600, 2043892), (1284, '3598', '6922330913246', '170201', 1600, 2035552), (1284, '3598', '6948969800566', '100301', 1590, 2045019), (1284, '3598', '6948969800801', '100301', 1590, 2045018), (1284, '3598', '6958770001410', '070207', 1580, 2044575), (1284, '3598', '9556622104240', '100201', 1580, 2044771), (1284, '3598', '6921355232318', '020101', 1580, 2044953), (1284, '3598', '6925303774202', '100202', 1560, 2041440), (1284, '3598', '6970182591570', '160202', 1560, 2044567), (1284, '3598', '6954767425979', '050402', 1520, 2036590), (1284, '3598', '6943290501793', '170202', 1500, 2041042), (1284, '3598', '20449926', '170201', 1500, 2044992), (1284, '3598', '6918551804593', '010102', 1500, 2022292), (1284, '3598', '6922330913062', '170201', 1500, 2040128), (1284, '3598', '6925303721398', '050202', 1500, 2005364), (1284, '3598', '6954767413877', '050403', 1500, 2004638), (1284, '3598', '6932571031241', '020103', 1500, 2025105), (1284, '3598', '6943290501632', '170201', 1500, 2026471), (1284, '3598', '6932697610030', '070303', 1490, 2037215), (1284, '3598', '4894375015860', '140204', 1450, 2044756), (1284, '3598', '6921317923001', '050201', 1400, 2044510), (1284, '3598', '4891028710882', '050203', 1400, 2044612), (1284, '3598', '6932005201820', '170201', 1400, 2033601), (1284, '3598', '6923450665701', '140302', 1390, 2044010), (1284, '3598', '6906791582555', '050704', 1380, 2034544), (1284, '3598', '6932005206252', '170202', 1360, 2043919), (1284, '3598', '6970182591747', '160101', 1360, 2044866), (1284, '3598', '6954767460116', '050402', 1350, 2044178), (1284, '3598', '6931925871847', '140301', 1350, 2036627), (1284, '3598', '6940255809703', '090502', 1350, 2041548), (1284, '3598', '6924187828544', '100401', 1350, 2016445), (1284, '3598', '6932873829447', '090502', 1300, 2043578), (1284, '3598', '6926410331425', '070207', 1290, 2044230), (1284, '3598', '6923807807129', '060204', 1280, 2017678), (1284, '3598', '6928494805250', '020101', 1280, 2033386), (1284, '3598', '6923450662021', '140302', 1250, 2037478), (1284, '3598', '6923450662113', '140302', 1250, 2037482), (1284, '3598', '6923775940330', '100201', 1250, 2045252), (1284, '3598', '6954432710256', '140302', 1250, 2032140), (1284, '3598', '6954432710195', '140302', 1250, 2028140), (1284, '3598', '4897055399311', '140304', 1240, 2044917), (1284, '3598', '6924743919211', '100102', 1240, 2026654), (1284, '3598', '6909493401001', '010102', 1200, 2028741), (1284, '3598', '6936357411111', '020101', 1200, 2038325), (1284, '3598', '6970399920514', '050204', 1200, 2044209), (1284, '3598', '6954767430768', '050402', 1200, 2044403), (1284, '3598', '4901616007536', '090101', 1200, 2040894), (1284, '3598', '6954767430836', '050402', 1200, 2044848), (1284, '3598', '4891028164456', '050205', 1200, 2030543), (1284, '3598', '6925303713058', '100202', 1200, 2041442), (1284, '3598', '6947012800010', '050101', 1200, 2029471), (1284, '3598', '6959479300316', '100404', 1200, 2034639), (1284, '3598', '6903252060065', '070101', 1200, 2035177), (1284, '3598', '6943290507283', '160201', 1200, 2036958), (1284, '3598', '8801066310520', '020401', 1200, 2038276), (1284, '3598', '20449896', '170201', 1180, 2044989), (1284, '3598', '6953949205064', '070408', 1180, 2045156), (1284, '3598', '6921136511113', '050704', 1180, 2045524), (1284, '3598', '6921136502210', '050704', 1180, 2045525), (1284, '3598', '6921355220407', '020102', 1170, 2044948), (1284, '3598', '6922307718164', '100301', 1160, 2045296), (1284, '3598', '6922307718188', '100301', 1160, 2045294), (1284, '3598', '6923450656150', '140302', 1150, 2011016), (1284, '3598', '6923450601549', '140302', 1150, 2013854), (1284, '3598', '6934660552118', '090301', 1150, 2035074), (1284, '3598', '6923450605332', '140301', 1150, 2023621), (1284, '3598', '6932583203155', '070203', 1140, 2017511), (1284, '3598', '6928590207606', '140204', 1100, 2043135), (1284, '3598', '6903148258026', '090301', 1100, 2043149), (1284, '3598', '6922300664796', '100501', 1100, 2043297), (1284, '3598', '6922300664833', '100501', 1100, 2043296), (1284, '3598', '6920180209724', '050104', 1100, 2029099), (1284, '3598', '6956416206090', '050202', 1100, 2044184), (1284, '3598', '6921168550128', '050501', 1100, 2025480), (1284, '3598', '6920698400477', '070102', 1100, 2022532), (1284, '3598', '6932005203916', '020302', 1100, 2037991), (1284, '3598', '6932850200122', '060203', 1100, 2036648), (1284, '3598', '6901668001115', '140102', 1100, 2041862), (1284, '3598', '6921253814111', '170201', 1100, 2042444), (1284, '3598', '6914782121065', '140401', 1090, 2045250), (1284, '3598', '6914782121089', '140401', 1090, 2045249), (1284, '3598', '6943290510412', '160201', 1080, 2043718), (1284, '3598', '6944697601161', '160201', 1080, 2043917), (1284, '3598', '6944697601154', '160201', 1080, 2043916), (1284, '3598', '4897043061091', '100504', 1080, 2044999), (1284, '3598', '6903244370974', '090301', 1080, 2041511), (1284, '3598', '6932005205484', '020302', 1050, 2044860), (1284, '3598', '6925432111398', '020103', 1050, 2045041), (1284, '3598', '6920612646066', '010102', 1000, 2043965), (1284, '3598', '6902934990362', '140303', 1000, 2009628), (1284, '3598', '6909493200277', '010102', 1000, 2028742), (1284, '3598', '6970399920439', '050104', 1000, 2045037), (1284, '3598', '6934660528618', '090301', 1000, 2011038), (1284, '3598', '6901180993387', '140101', 1000, 2040996), (1284, '3598', '6944697600799', '160202', 1000, 2036442), (1284, '3598', '3068320055008', '050101', 990, 2006537), (1284, '3598', '4710022036524', '100201', 990, 2043580), (1284, '3598', '8809022201035', '100404', 990, 2037690), (1284, '3598', '6971860060920', '070202', 990, 2045383), (1284, '3598', '6923985700038', '100203', 990, 2045512), (1284, '3598', '6934660522258', '090301', 990, 2041283), (1284, '3598', '6959659500727', '160103', 980, 2030994), (1284, '3598', '6920242100020', '100502', 950, 2014679), (1284, '3598', '6946954300169', '140301', 950, 2027710), (1284, '3598', '6921168593804', '050301', 950, 2035958), (1284, '3598', '6907868581587', '010102', 900, 2016126), (1284, '3598', '6956416205956', '050302', 900, 2044180), (1284, '3598', '6911988014832', '140204', 900, 2020235), (1284, '3598', '4710022037675', '100201', 900, 2043581), (1284, '3598', '6921355240030', '030101', 900, 2003286), (1284, '3598', '6902890022961', '070206', 900, 2004134), (1284, '3598', '6951157101345', '090501', 900, 2045236), (1284, '3598', '6902083881085', '030201', 900, 2017786), (1284, '3598', '6922577727163', '020101', 900, 2038689), (1284, '3598', '6925303721367', '050201', 900, 2005413), (1284, '3598', '6922577727446', '020101', 900, 2041516), (1284, '3598', '6927321721350', '020101', 900, 2042703), (1284, '3598', '6951648500091', '070206', 890, 2043121), (1284, '3598', '6932571026391', '020101', 890, 2044368), (1284, '3598', '20449902', '170201', 890, 2044990), (1284, '3598', '4710094109676', '050702', 880, 2044893), (1284, '3598', '6970182591709', '160202', 880, 2045509), (1284, '3598', '6938254754070', '020403', 880, 2045606), (1284, '3598', '80177609', '140402', 860, 2014904), (1284, '3598', '6910442944289', '030201', 850, 2027345), (1284, '3598', '6925303714857', '070102', 850, 2021478), (1284, '3598', '6914973600041', '140401', 850, 2022386), (1284, '3598', '6931925871465', '140301', 850, 2044191), (1284, '3598', '6921581597076', '050204', 850, 2036473), (1284, '3598', '6937131900739', '160401', 850, 2036445), (1284, '3598', '6934665082047', '020101', 850, 2017293), (1284, '3598', '6903148153086', '080202', 850, 2026951), (1284, '3598', '6914973604032', '140401', 820, 2022387), (1284, '3598', '8993175537469', '140101', 800, 2033434), (1284, '3598', '6970182590603', '160101', 800, 2043895), (1284, '3598', '6921355220070', '020102', 800, 2028665), (1284, '3598', '6946050104548', '140202', 800, 2034599), (1284, '3598', '6926265313010', '100201', 800, 2034207), (1284, '3598', '20455071', '160201', 800, 2045507), (1284, '3598', '6901285991219', '050101', 800, 2021667), (1284, '3598', '6901285991271', '050102', 800, 2023289), (1284, '3598', '6970011880820', '020101', 800, 2041535), (1284, '3598', '6926816979771', '100202', 790, 2045257), (1284, '3598', '6926816979795', '100202', 790, 2045258), (1284, '3598', '6922621129684', '100402', 780, 2009647), (1284, '3598', '6921355220087', '020102', 780, 2040764), (1284, '3598', '6949656160017', '070202', 780, 2042238), (1284, '3598', '6954767432076', '050402', 760, 2004482), (1284, '3598', '6950955901232', '140204', 760, 2041923), (1284, '3598', '6947954100872', '100502', 750, 2043567), (1284, '3598', '6932571031111', '020103', 750, 2025107), (1284, '3598', '6907992103051', '020101', 750, 2017307), (1284, '3598', '6901668008176', '140101', 750, 2044175), (1284, '3598', '6943290511921', '170201', 750, 2045595), (1284, '3598', '6901845040968', '140101', 750, 2017661), (1284, '3598', '69019388', '140302', 720, 2005289), (1284, '3598', '6971207395456', '050302', 700, 2044396), (1284, '3598', '6937131901026', '160401', 700, 2036446), (1284, '3598', '6941704414059', '020102', 700, 2045042), (1284, '3598', '6906907401022', '050402', 700, 2003228), (1284, '3598', '6906907403088', '050402', 700, 2003239), (1284, '3598', '6970725074713', '020402', 700, 2041835), (1284, '3598', '6927216920011', '050302', 700, 2034858), (1284, '3598', '6952522800115', '020101', 700, 2027203), (1284, '3598', '6938888887502', '070403', 690, 2035576), (1284, '3598', '6932571040106', '020201', 690, 2025104), (1284, '3598', '6906791582562', '050704', 690, 2035168), (1284, '3598', '6938888888653', '070403', 690, 2035578), (1284, '3598', '6932571040168', '020201', 690, 2025103), (1284, '3598', '6938888888615', '070403', 690, 2036500), (1284, '3598', '6938888889810', '050205', 690, 2042503), (1284, '3598', '4897036692189', '050502', 680, 2044183), (1284, '3598', '20447267', '160102', 680, 2044726), (1284, '3598', '6932002040705', '010102', 680, 2045009), (1284, '3598', '6923644269579', '030101', 680, 2018602), (1284, '3598', '6901668053916', '140103', 670, 2044154), (1284, '3598', '6932873820215', '090502', 650, 2043255), (1284, '3598', '6917536014088', '070103', 650, 2029277), (1284, '3598', '6943290510634', '170202', 650, 2043551), (1284, '3598', '6937350205127', '070207', 650, 2033398), (1284, '3598', '6925303770556', '070103', 650, 2028083), (1284, '3598', '6917536014019', '070103', 650, 2037621), (1284, '3598', '6970717330896', '170203', 650, 2045071), (1284, '3598', '6924743919273', '100102', 650, 2039052), (1284, '3598', '6907992512853', '030301', 650, 2034566), (1284, '3598', '6902538007664', '050501', 600, 2043903), (1284, '3598', '6921581540270', '050602', 600, 2019540), (1284, '3598', '6959479300323', '100404', 600, 2036716), (1284, '3598', '6922279401750', '120401', 600, 2032284), (1284, '3598', '6923450605288', '140302', 600, 2023329), (1284, '3598', '6923450658079', '140302', 600, 2028703), (1284, '3598', '6956416202634', '050602', 600, 2045559), (1284, '3598', '6943290500949', '170201', 600, 2033796), (1284, '3598', '6954767410586', '050402', 600, 2042356), (1284, '3598', '6958350504249', '050302', 590, 2044669), (1284, '3598', '6933368300335', '140301', 580, 2044735), (1284, '3598', '45129162', '140402', 580, 2045302), (1284, '3598', '6943290508686', '170201', 580, 2045594), (1284, '3598', '6935036481872', '020402', 560, 2043279), (1284, '3598', '6901668053527', '140101', 560, 2044153), (1284, '3598', '6901668053510', '140101', 560, 2044152), (1284, '3598', '6921669813678', '090504', 560, 2044471), (1284, '3598', '6972020770079', '050402', 550, 2044534), (1284, '3598', '6972020770086', '050402', 550, 2044533), (1284, '3598', '6972020770031', '050401', 550, 2044667), (1284, '3598', '6941067725106', '050302', 550, 2030865), (1284, '3598', '6941067725571', '050302', 550, 2030866), (1284, '3598', '6921581540515', '050302', 550, 2033770), (1284, '3598', '6921168550098', '050501', 550, 2025479), (1284, '3598', '6902083886455', '050704', 550, 2013136), (1284, '3598', '6943290503919', '170201', 550, 2026646), (1284, '3598', '6921355270303', '030101', 550, 2041185), (1284, '3598', '6920698400378', '070102', 550, 2022531), (1284, '3598', '6902083880781', '070204', 500, 2009288), (1284, '3598', '6937962100742', '070102', 500, 2043572), (1284, '3598', '6901180993585', '140101', 500, 2040998), (1284, '3598', '6921168594351', '050501', 500, 2043760), (1284, '3598', '6933368307631', '140301', 500, 2044734), (1284, '3598', '6901180993486', '140101', 500, 2040997), (1284, '3598', '6922279400838', '090504', 500, 2031199), (1284, '3598', '6914973607125', '140401', 500, 2037912), (1284, '3598', '6921168500956', '050501', 500, 2020054), (1284, '3598', '6946050100106', '140101', 500, 2036994), (1284, '3598', '6956416206564', '050202', 500, 2045558), (1284, '3598', '6956416206601', '050702', 500, 2045560), (1284, '3598', '6972347140098', '050202', 500, 2045553), (1284, '3598', '6903252714210', '070102', 500, 2019518), (1284, '3598', '6920180242684', '050402', 490, 2045047), (1284, '3598', '6902447168708', '100202', 480, 2041441), (1284, '3598', '6902890229421', '070206', 460, 2045401), (1284, '3598', '6923644268503', '030201', 450, 2017997), (1284, '3598', '6956416206281', '050302', 450, 2044138), (1284, '3598', '6954767460147', '050104', 450, 2044179), (1284, '3598', '6972215667535', '050501', 450, 2044244), (1284, '3598', '6921581540089', '050501', 450, 2032659), (1284, '3598', '6920609900539', '100403', 450, 2021143), (1284, '3598', '6902538004045', '050501', 450, 2004326), (1284, '3598', '6935284412918', '100303', 450, 2035037), (1284, '3598', '6930720130524', '100304', 450, 2020300), (1284, '3598', '6958620700319', '140204', 450, 2042675), (1284, '3598', '6970182591679', '160101', 420, 2044730), (1284, '3598', '6932873831785', '090503', 400, 2043254), (1284, '3598', '6925704218817', '010102', 400, 2043958), (1284, '3598', '6927462217279', '070206', 400, 2044435), (1284, '3598', '6906907129032', '050401', 400, 2045088), (1284, '3598', '6935947800533', '050401', 400, 2045425), (1284, '3598', '6950955901225', '140204', 380, 2041924), (1284, '3598', '6932583203148', '070203', 380, 2017512), (1284, '3598', '6971207392011', '050302', 350, 2040853), (1284, '3598', '6922279400265', '050101', 350, 2030338), (1284, '3598', '6971599569183', '020202', 350, 2044854), (1284, '3598', '6950955901201', '140202', 350, 2041925), (1284, '3598', '6971207396552', '050302', 350, 2041260), (1284, '3598', '6921317905168', '050201', 350, 2040684), (1284, '3598', '45129155', '140402', 290, 2045301), (1284, '3598', '6927462216074', '070206', 280, 2044434), (1284, '3598', '4605504515188', '140402', 280, 2044619), (1284, '3598', '6940996701953', '140401', 250, 2036899), (1284, '3598', '6937082260395', '060207', 250, 2020598), (1284, '3598', '6947503203450', '010102', 200, 2043959), (1284, '3598', '6910160313251', '060204', 200, 2036701), (1284, '3598', '6921168594382', '050402', 200, 2044614), (1284, '3598', '6940471600535', '140303', 200, 2040641), (1284, '3598', '20200756', '080203', 30, 2020075))


# upc_data_sql="select sum(T2.t1_nums) as ai_nums,T2.t1_shop_id as ai_shop_id ,T3.upc as ai_upc,T2.t1_create_date as  ai_create_date,DATE_FORMAT( from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))+24*3600),'%Y-%m-%d') as ai_next_date,DAYOFWEEK(DATE_FORMAT(from_unixtime(unix_timestamp(DATE_FORMAT(T2.t1_create_date ,'%Y-%m-%d'))-24*3600),'%Y-%m-%d')) as ai_week_date from ( "
# +               "select sum(T1.nums) as t1_nums,T1.shop_id as t1_shop_id,T1.shop_goods_id,T1.create_date as t1_create_date  from "
# +               "(select number nums,shop_id,shop_goods_id,DATE_FORMAT(create_time,'%Y-%m-%d') 	create_date from payment_detail "
# +        "where shop_id is not null and shop_id in {4} and goods_id is not null and number > 0 and create_time > '{0} 00:00:00' and create_time < '{1} 00:00:00' and "
# +       "payment_id in ( "
# +            "select distinct(payment.id) from payment where payment.type != 50  and create_time > '{2} 00:00:00' and create_time < '{3} 00:00:00' "
# +					") "
# +            ")  T1 "
# +               "group by T1.shop_id,T1.shop_goods_id,T1.create_date) T2 "
# +                   "left join  shop_goods T3 on T2.t1_shop_id= T3.shop_id and T2.shop_goods_id = T3.id "
# +                   "where T3.upc != '' and  T3.upc != '0' "
# +                   "group by T2.t1_create_date,T2.t1_shop_id,T3.upc "
# upc_data_sql.format()

def get_data(target,template_shop_id,days=128):
    """
    :param target: 选品店的id
    :param template_shop_id: 模板店的id
    :param days: 已模板店多少天的范围进行销量排序选择
    :return:
    """
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d %H:%M:%S')
    week_ago = (now - datetime.timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')
    sql = "select sum(p.amount),g.upc,g.corp_classify_code,g.neighbor_goods_id,g.price,p.name from dmstore.payment_detail as p left join dmstore.goods as g on p.goods_id=g.id where p.create_time > '{}' and p.create_time < '{}' and p.shop_id={} group by g.upc order by sum(p.amount) desc;"
    # conn = pymysql.connect('123.103.16.19', 'readonly', password='fxiSHEhui2018@)@)', database='dmstore',charset="utf8", port=3300, use_unicode=True)
    conn = connections['dmstore']
    cursor = conn.cursor()
    cursor.execute(sql.format(week_ago,now_date,template_shop_id))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print(results)

    data = []
    for result in results:
        list = [target,template_shop_id]
        list.append(result[1])
        list.append(result[2])
        list.append(int(result[0]))
        list.append(result[3])
        list.append(result[4])
        list.append(result[5])
        if not result[1].startswith('6901028'):       # 以此为开头的是香烟
            data.append(list)
        # if result[2][:2] in ['02','16','17']:       # 日配的商品
        #     data.append(list)
        # if result[2][:2] in ['01']:       # 冷冻的商品
        #     data.append(list)

    print('first:', len(data))

    for i in data:
        i[4] = round(i[4] / days)
    # print(data)
    return data

def storage_day_choose(data):
    # 以下查询保质期的长短
    upcs = [str(i[2]) for i in data]
    sql_02 = 'select upc from ucenter.uc_merchant_goods where upc in {} and storage_day is null'
    cursor_02 = connections['ucenter'].cursor()
    # print(tuple(upcs))
    cursor_02.execute(sql_02.format(tuple(upcs)))
    upcs = cursor_02.fetchall()
    upcs = [i[0] for i in upcs]
    cursor_02.close()

    results = []
    for i in data:
        if i[2] in upcs:
            results.append(i)


    print("upcs_len:", len(upcs))
    print("storage_result:", len(results))
    return results

def choose_goods(data,ratio=0.95):
    """
    进行选品的筛选
    需要目标店的选品量和要筛掉的类别
    :param data:
    :param ratio: 筛掉后保留的比例
    :return:
    """

    result = []
    goods_dict={}
    for d in data:
        code = d[3]
        first = code[:2]
        if not first in goods_dict:
            goods_dict[first] = {}
        second = code[2:4]
        if not second in goods_dict[first]:
            goods_dict[first][second] = {}
        third = code[4:6]
        if not third in goods_dict[first][second]:
            goods_dict[first][second][third] = []
        goods_dict[first][second][third].append(d)
        # print(d)
        # print(goods_dict)

    # print('字典表：',goods_dict)
    for f in goods_dict:
        # print(goods_dict[f])
        for s in goods_dict[f]:
            tem = []
            for t in goods_dict[f][s]:
                upcs = goods_dict[f][s][t]
                l = len(upcs)
                if l > 2:
                    m = round(l*ratio)
                    upcs.sort(key=lambda x: x[4], reverse=True)    #基于销量排序
                    result += upcs[:m]
                else:
                    tem.extend(upcs)
            tem.sort(key=lambda x: x[4], reverse=True)
            n = round(len(tem)*ratio)
            result += tem[:n]

    result.sort(key=lambda x: x[4], reverse=True)
    # print('筛完后:',result)
    print('second:',len(result))

    # print(result)
    return result

def check_order(data):
    """
    检查商品是否可订货
    :param data:
    :return:
    """
    # print(1000,data)
    upcs = []
    for i in data:
        upcs.append(i[2])
    upcs = tuple(upcs)

    # conn = pymysql.connect('10.19.68.63', 'diamond_rw', password='iMZBbBwxJZ7LUW7p', database='ls_diamond', charset="utf8",port=3306, use_unicode=True)
    conn = connections['erp']
    cursor = conn.cursor()

    select_sql = "SELECT a.status,a.start_sum,a.actual_stock from ms_sku_relation as a LEFT JOIN ls_sku as b on a.sku_id=b.sku_id and a.prod_id=b.prod_id WHERE b.model_id='6923555212749' "
    slect_sql_02 = "SELECT a.authorized_shop_id from ms_relation as a WHERE a.is_authorized_shop_id='9851' and a.status=1"
    slect_sql_03 = "SELECT a.status,b.model_id FROM ms_sku_relation as a LEFT JOIN ls_sku as b on a.sku_id=b.sku_id and a.prod_id=b.prod_id WHERE a.status=1 AND a.sku_id IN (SELECT ls_sku.sku_id FROM ls_sku WHERE ls_sku.model_id in {} AND ls_sku.prod_id IN (SELECT ls_prod.prod_id FROM ls_prod WHERE ls_prod.shop_id = '9850'))"
    cursor.execute(slect_sql_03.format(upcs))
    order_yes = cursor.fetchall()
    cursor.close()
    conn.close()

    order_upc = []
    for m in order_yes:
        order_upc.append(m[1])

    # 遍历选品列表，把能订货的上商品返回
    result = []
    for j in data:
        if j[2] in order_upc:
            result.append(j)

    print('order_yes(repeat):', len(order_yes))
    print('third_order_checked:',len(result))
    return result

def save_data(data,batch_id,uc_shopid):
    """
    选品结果存入数据库
    :param data:
    :return:
    """
    upc_list = []
    for i in data:
        i[6] = i[4]/i[6]    # 计算psd
        i = tuple(i)
        upc_list.append(i)
    upc_tuple = tuple(upc_list)
    # print(upc_tuple)

    # conn = pymysql.connect('10.19.68.63', 'gpu_rw', password='jyrMnQR1NdAKwgT4', database='goodsdl',charset="utf8", port=3306, use_unicode=True)
    conn = connections['default']
    cursor = conn.cursor()

    # insert_sql_01 = "insert into goods_firstgoodsselection(shopid,template_shop_ids,upc,code,predict_sales_amount,mch_code,mch_goods_code,predict_sales_num,name,batch_id,uc_shopid) values (%s,%s,%s,%s,%s,2,%s,%s,%s,'{}','{}')"
    insert_sql_02 = "insert into goods_goodsselectionhistory(shopid,template_shop_ids,upc,code,predict_sales_amount,mch_code,mch_goods_code,predict_sales_num,name,batch_id,uc_shopid) values (%s,%s,%s,%s,%s,2,%s,%s,%s,'{}','{}')"
    delete_sql = "delete from goods_firstgoodsselection where shopid={}"
    delete_sql_02 = "delete from goods_goodsselectionhistory where shopid={} and batch_id='{}'"
    select_sql = "select batch_id from goods_goodsselectionhistory where uc_shopid={} and batch_id='{}'"
    try:
        print('batch_id',batch_id,type(batch_id))
        # cursor.execute(delete_sql.format(upc_tuple[0][0],batch_id))
        # cursor.executemany(insert_sql_01.format(batch_id,uc_shopid), upc_tuple[:])
        cursor.execute(select_sql.format(uc_shopid,batch_id))   # 查询有该批次，没有的话，插入，有的话，先删再插入
        # print('history_batch_id', history_batch_id,type(history_batch_id))
        if cursor.fetchone():
            cursor.execute(delete_sql_02.format(uc_shopid, batch_id))
            print("删掉该批次之前的数据")
        cursor.executemany(insert_sql_02.format(batch_id,uc_shopid), upc_tuple[:])
        conn.commit()
        conn.close()
        print('ok')
    except:
        # 如果发生错误则回滚
        connections['default'].rollback()
        # 关闭数据库连接
        cursor.close()
        conn.close()
        print('error')

def second_choose(data):
    """
    最最开始的时候选品不够，所以又选了一次，所以以后基本用不着这个方法
    :param data:
    :return:
    """
    result = []
    for item in data:
        flag = 0
        for o in origin_choose:
            if item[2] == o[2]:
                flag = 1
                # print(item)
        if  flag == 0:
            result.append(item)
    print(len(result))
    # print(result)

    for i in result:
        i[4] = round(i[4]*3/7)

    result_list = []
    for i in result:
        i = tuple(i)
        result_list.append(i)
    result_tuple = tuple(result_list)
    print(result_tuple)
    return result_tuple

def start_choose_goods(batch_id,uc_shopid,pos_shopid):
    """
    开始进行选品
    :param batch_id: 批次号
    :param uc_shopid: 台账id
    :param pos_shopid: pos系统的id
    :return:
    """
    a = get_data(pos_shopid, '88')
    print("uc_shopid,pos_shopid",uc_shopid,pos_shopid)
    # a = storage_day_choose(a)
    b = choose_goods(a)
    c = check_order(b)
    save_data(c,batch_id,uc_shopid)



if __name__ == '__main__':
    start_choose_goods('a_001', 1204, None)



