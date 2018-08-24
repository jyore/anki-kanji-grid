#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Contact: frony0@gmail.com, Modified by CalculusAce, Original Add-on Code: 1049174162

import time,codecs,math,os,unicodedata
from aqt import mw
from anki.js import jquery
from aqt.utils import showInfo
from anki.utils import ids2str
from anki.hooks import addHook
from aqt.webview import AnkiWebView
from aqt.qt import *

#_time = None
_pattern = "expression"
_literal = False
_interval = 180
_thin = 20
_wide = 48
_group = 0
_unseen = True
_tooltips = False
_kanjionly = True
_ignore = u"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + \
          u"ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ" + \
          u"ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ" + \
          u"1234567890１２３４５６７８９０" + \
          u"あいうゔえおぁぃぅぇぉかきくけこがぎぐげごさしすせそざじずぜぞ" + \
          u"たちつてとだぢづでどなにぬねのはひふへほばびぶべぼぱぴぷぺぽ" + \
          u"まみむめもやゃゆゅよょらりるれろわをんっ" + \
          u"アイウヴエオァィゥェォカキクケコガギグゲゴサシスセソザジズゼゾ" + \
          u"タチツテトダヂヅデドナニヌネノハヒフヘホバビブベボパピプペポ" + \
          u"マミムメモヤャユュヨョラリルレロワヲンッ" + \
          u"!\"$%&'()|=~-^@[;:],./`{+*}<>?\\_" + \
          u"＠「；：」、。・‘｛＋＊｝＜＞？＼＿！”＃＄％＆’（）｜＝．〜～ー＾ ゙゙゚" + \
          u"☆★＊○●◎〇◯“…『』#♪ﾞ〉〈→》《π×"
_heisig = [ (u'Non-RTK Kanji', ''),
    (u'RTK1 Kanji', u'一二三四五六七八九十口日月田目古吾冒朋明唱晶品呂昌早旭世胃旦胆亘凹凸旧自白百中千舌升昇丸寸肘専博占上下卓朝嘲只貝唄貞員貼見児元頁頑凡負万句肌旬勺的首乙乱直具真工左右有賄貢項刀刃切召昭則副別丁町可頂子孔了女好如母貫兄呪克小少大多夕汐外名石肖硝砕砂妬削光太器臭嗅妙省厚奇川州順水氷永泉腺原願泳沼沖汎江汰汁沙潮源活消況河泊湖測土吐圧埼垣填塡圭封涯寺時均火炎煩淡灯畑災灰点照魚漁里黒墨鯉量厘埋同洞胴向尚字守完宣宵安宴寄富貯木林森桂柏枠梢棚杏桐植椅枯朴村相机本札暦案燥未末昧沫味妹朱株若草苦苛寛薄葉模漠墓暮膜苗兆桃眺犬状黙然荻狩猫牛特告先洗介界茶脊合塔王玉宝珠現玩狂旺皇呈全栓理主注柱金銑鉢銅釣針銘鎮道導辻迅造迫逃辺巡車連軌輸喩喻前煎各格賂略客額夏処条落冗冥軍輝運冠夢坑高享塾熟亭京涼景鯨舎周週士吉壮荘売学覚栄書津牧攻敗枚故敬言警計詮獄訂訃討訓詔詰話詠詩語読調談諾諭式試弐域賊栽載茂戚成城誠威滅減蔑桟銭浅止歩渉頻肯企歴武賦正証政定錠走超赴越是題堤建鍵延誕礎婿衣裁装裏壊哀遠猿初巾布帆幅帽幕幌錦市柿姉肺帯滞刺制製転芸雨雲曇雷霜冬天妖沃橋嬌立泣章競帝諦童瞳鐘商嫡適滴敵匕叱匂頃北背比昆皆楷諧混渇謁褐喝葛旨脂詣壱毎敏梅海乞乾腹複欠吹炊歌軟次茨資姿諮賠培剖音暗韻識鏡境亡盲妄荒望方妨坊芳肪訪放激脱説鋭曽増贈東棟凍妊廷染燃賓歳県栃地池虫蛍蛇虹蝶独蚕風己起妃改記包胞砲泡亀電竜滝豚逐遂家嫁豪腸場湯羊美洋詳鮮達羨差着唯堆椎誰焦礁集准進雑雌準奮奪確午許歓権観羽習翌曜濯曰困固錮国団因姻咽園回壇店庫庭庁床麻磨心忘恣忍認忌志誌芯忠串患思恩応意臆想息憩恵恐惑感憂寡忙悦恒悼悟怖慌悔憎慣愉惰慎憾憶惧憧憬慕添必泌手看摩我義議犠抹拭拉抱搭抄抗批招拓拍打拘捨拐摘挑指持拶括揮推揚提損拾担拠描操接掲掛捗研戒弄械鼻刑型才財材存在乃携及吸扱丈史吏更硬梗又双桑隻護獲奴怒友抜投没股設撃殻支技枝肢茎怪軽叔督寂淑反坂板返販爪妥乳浮淫将奨采採菜受授愛曖払広勾拡鉱弁雄台怠治冶始胎窓去法会至室到致互棄育撤充銃硫流允唆出山拙岩炭岐峠崩密蜜嵐崎崖入込分貧頒公松翁訟谷浴容溶欲裕鉛沿賞党堂常裳掌皮波婆披破被残殉殊殖列裂烈死葬瞬耳取趣最撮恥職聖敢聴懐慢漫買置罰寧濁環還夫扶渓規替賛潜失鉄迭臣姫蔵臓賢腎堅臨覧巨拒力男労募劣功勧努勃励加賀架脇脅協行律復得従徒待往征径彼役徳徹徴懲微街桁衡稿稼程税稚和移秒秋愁私秩秘称利梨穫穂稲香季委秀透誘稽穀菌萎米粉粘粒粧迷粋謎糧菊奥数楼類漆膝様求球救竹笑笠笹箋䇳筋箱筆筒等算答策簿築篭籠人佐侶但住位仲体悠件仕他伏伝仏休仮伎伯俗信佳依例個健側侍停値倣傲倒偵僧億儀償仙催仁侮使便倍優伐宿傷保褒傑付符府任賃代袋貸化花貨傾何荷俊傍俺久畝囚内丙柄肉腐座挫卒傘匁以似併瓦瓶宮営善膳年夜液塚幣蔽弊喚換融施旋遊旅勿物易賜尿尼尻泥塀履屋握屈掘堀居据裾層局遅漏刷尺尽沢訳択昼戸肩房扇炉戻涙雇顧啓示礼祥祝福祉社視奈尉慰款禁襟宗崇祭察擦由抽油袖宙届笛軸甲押岬挿申伸神捜果菓課裸斤析所祈近折哲逝誓斬暫漸断質斥訴昨詐作雪録剥剝尋急穏侵浸寝婦掃当彙争浄事唐糖康逮伊君群耐需儒端両満画歯曲曹遭漕槽斗料科図用庸備昔錯借惜措散廿庶遮席度渡奔噴墳憤焼暁半伴畔判拳券巻圏勝藤謄片版之乏芝不否杯矢矯族知智挨矛柔務霧班帰弓引弔弘強弥弱溺沸費第弟巧号朽誇顎汚与写身射謝老考孝教拷者煮著箸署暑諸猪渚賭峡狭挟頬頰追阜師帥官棺管父釜交効較校足促捉距路露跳躍践踏踪骨滑髄禍渦鍋過阪阿際障隙随陪陽陳防附院陣隊墜降階陛隣隔隠堕陥穴空控突究窒窃窟窪搾窯窮探深丘岳兵浜糸織繕縮繁縦緻線綻締維羅練緒続絵統絞給絡結終級紀紅納紡紛紹経紳約細累索総綿絹繰継緑縁網緊紫縛縄幼後幽幾機畿玄畜蓄弦擁滋慈磁系係孫懸遜却脚卸御服命令零齢冷領鈴勇湧通踊疑擬凝範犯氾厄危宛腕苑怨柳卵留瑠貿印臼毀興酉酒酌酎酵酷酬酪酢酔配酸猶尊豆頭短豊鼓喜樹皿血盆盟盗温蓋監濫鑑藍猛盛塩銀恨根即爵節退限眼良朗浪娘食飯飲飢餓飾餌館餅養飽既概慨平呼坪評刈刹希凶胸離璃殺爽純頓鈍辛辞梓宰壁璧避新薪親幸執摯報叫糾収卑碑陸睦勢熱菱陵亥核刻該骸劾述術寒塞醸譲壌嬢毒素麦青精請情晴清静責績積債漬表俵潔契喫害轄割憲生星醒姓性牲産隆峰蜂縫拝寿鋳籍春椿泰奏実奉俸棒謹僅勤漢嘆難華垂唾睡錘乗剰今含貪吟念捻琴陰予序預野兼嫌鎌謙廉西価要腰票漂標栗慄遷覆煙南楠献門問閲閥間闇簡開閉閣閑聞潤欄闘倉創非俳排悲罪輩扉侯喉候決快偉違緯衛韓干肝刊汗軒岸幹芋宇余除徐叙途斜塗束頼瀬勅疎辣速整剣険検倹重動腫勲働種衝薫病痴痘症瘍痩疾嫉痢痕疲疫痛癖匿匠医匹区枢殴欧抑仰迎登澄発廃僚瞭寮療彫形影杉彩彰彦顔須膨参惨修珍診文対紋蚊斑斉剤済斎粛塁楽薬率渋摂央英映赤赦変跡蛮恋湾黄横把色絶艶肥甘紺某謀媒欺棋旗期碁基甚勘堪貴遺遣潰舞無組粗租狙祖阻査助宜畳並普譜湿顕繊霊業撲僕共供異翼戴洪港暴爆恭選殿井丼囲耕亜悪円角触解再講購構溝論倫輪偏遍編冊柵典氏紙婚低抵底民眠捕哺浦蒲舗補邸郭郡郊部都郵邦那郷響郎廊盾循派脈衆逓段鍛后幻司伺詞飼嗣舟舶航舷般盤搬船艦艇瓜弧孤繭益暇敷来気汽飛沈枕妻凄衰衷面麺革靴覇声眉呉娯誤蒸承函極牙芽邪雅釈番審翻藩毛耗尾宅託為偽畏長張帳脹髪展喪巣単戦禅弾桜獣脳悩厳鎖挙誉猟鳥鳴鶴烏蔦鳩鶏島暖媛援緩属嘱偶遇愚隅逆塑遡岡鋼綱剛缶陶揺謡鬱就蹴懇墾貌免逸晩勉象像馬駒験騎駐駆駅騒駄驚篤罵騰虎虜膚虚戯虞慮劇虐鹿麓薦慶麗熊能態寅演辰辱震振娠唇農濃送関咲鬼醜魂魔魅塊襲嚇朕雰箇錬遵罷屯且藻隷癒璽潟丹丑羞卯巳'),
	(u'RTK3 Kanji', u'此柴些砦髭禽檎憐燐麟鱗奄庵掩悛駿峻竣犀皐畷綴鎧凱呑韮籤懺芻雛趨尤厖或兎也巴疋菫曼云莫而倭侠倦俄佃仔仇伽儲僑倶侃偲侭脩倅做冴凋凌凛凧凪夙鳳剽劉剃厭雁贋厨仄哨咎囁喋嘩噂咳喧叩嘘啄吠吊噛叶吻吃噺噌邑呆喰埴坤壕垢坦埠堰堵嬰姦婢婉娼妓娃姪嬬姥姑姐嬉孕孜宥寓宏牢宋宍屠屁屑屡屍屏嵩崚嶺嵌帖幡幟庖廓庇鷹庄廟彊弛粥挽撞扮捏掴捺掻撰揃捌按播揖托捧撚挺擾撫撒擢摺捷抉怯惟惚怜惇恰恢悌澪洸滉漱洲洵滲洒沐泪渾涜梁澱洛汝漉瀕濠溌湊淋浩汀鴻潅溢湛淳渥灘汲瀞溜渕沌濾濡淀涅斧爺猾猥狡狸狼狽狗狐狛獅狒莨茉莉苺萩藝薙蓑苔蕩蔓蓮芙蓉蘭芦薯菖蕉蕎蕗茄蔭蓬芥萌葡萄蘇蕃苓菰蒙茅芭苅葱葵葺蕊茸蒔芹苫蒼藁蕪藷薮蒜蕨蔚茜莞蒐菅葦迪辿這迂遁逢遥遼逼迄逗鄭隕隈憑惹悉忽惣愈恕昴晋晟暈暉旱晏晨晒晃曝曙昂昏晦膿腑胱胚肛脆肋腔肱胡楓楊椋榛櫛槌樵梯柑杭柊柚椀栂柾榊樫槙楢橘桧棲栖桔杜杷梶杵杖樽櫓橿杓李棉楯榎樺槍柘梱枇樋橇槃栞椰檀樗槻椙彬桶楕樒毬燿燎炬焚灸煽煤煉燦灼烙焔烹牽牝牡琳琉瑳琢珊瑚瑞玖瑛玲畢畦痒痰疹痔癌痺眸眩雉矩磐碇碧硯砥碗碍碩磯砺碓禦祷祐祇祢禄禎秤黍禿稔稗穣稜稀穆窺窄穿竃竪颯站靖妾衿袷袴襖笙筏簾箪竿箆箔笥箭筑篠纂竺箕笈篇筈簸粕糟糊籾糠糞粟繋綸絨絆緋綜紐紘纏絢繍紬綺綾絃縞綬紗舵聯聡聘耽耶蚤蟹蛋蟄蝿蟻蝋蝦蛸螺蝉蛙蛾蛤蛭蛎罫袈裟截哉詢諄讐諌諒讃訊訣詫誼謬訝諺誹謂諜註譬轟輔輻輯豹賎貰賑贖躓蹄蹟跨跪醤醍醐醇麹釦銚鋤鋸錐鍬鋲錫錨釘鑓鋒鎚鉦錆鍾鋏閃悶閤雫霞翰斡鞍鞭鞘鞄靭鞠顛穎頗頌頚餐饗蝕飴駕騨馳騙馴駁駈驢鰻鯛鰯鱒鮭鮪鮎鯵鱈鯖鮫鰹鰍鰐鮒鮨鰭鴎鵬鸚鵡鵜鷺鷲鴨鳶梟塵麒舅鼠鑿艘瞑暝坐朔曳洩彗慧爾嘉兇兜靄劫歎輿歪翠黛鼎鹵鹸虔燕嘗殆牌覗齟齬秦雀隼耀夷嚢暢廻欣毅斯匙匡肇麿叢肴斐卿翫於套叛尖壷叡酋鴬赫臥甥瓢琵琶叉乖畠圃丞亮胤疏膏魁馨牒瞥睾巫敦奎翔皓黎赳已棘祟甦剪躾夥鼾陀粁糎粍噸哩浬吋呎梵薩菩唖牟迦珈琲檜轡淵伍什萬邁燭逞燈裡薗鋪嶋峯埜龍寵聾慾嶽國脛勁祀祓躇壽躊饅嘔鼈')
	]
_css = "body { background: #ccc url(/img/noise.png); }" + \
    ".info-wrapper { height: auto; width: 500px; margin: 4em auto; padding: 0 0 2em 0; position: relative; }" + \
    ".info { max-height: 120px; height: auto; padding: .5em 0; border-bottom: solid 1px #fff; border-radius: 0 0 1em 1em;" + \
    "	overflow: hidden; position: relative; transition: 1s; } p { margin: 1em; }" + \
    ".info:after, .aftershadow { bottom: 0; width: 100%; height: 3em; border-radius: 0 0 1em 1em; position: absolute;" + \
    "	background: linear-gradient(rgba(192,192,192,0), #ccc); content: ''; }" + \
    ".aftershadow { filter: progid:DXImageTransform.Microsoft.gradient(startColorstr=#00cccccc, endColorstr=#ffcccccc); }" + \
    ".info-wrapper input[type=checkbox] { display: none; } .info-wrapper label { left: 50%; bottom: 1.5em; width: 9em;" + \
    "	height: 1.25em; margin:  0 0 0 -4.5em; border-bottom: solid 1px #fff; border-radius: 0 0 1em 1em; overflow: hidden;" + \
    "	position: absolute; font: 700 .67em/1.25em Arial; text-align: center; text-shadow: 0 1px 0 #fff; cursor: pointer; }" + \
    ".info-wrapper label .more { margin: -.1em 0 .35em; transition: 1s; } .info-wrapper .switch { width: 4em; display: inline-block; }" + \
    ".info-wrapper input[type=checkbox]:checked ~ .info { max-height: 15em; } .info-wrapper input[type=checkbox]:checked + label .more { margin-top: -1.65em; }"

class TestedUnit:
    def __init__(self, value):
        self.idx = 0
        self.value = value
        self.avg_interval = 0.0
        self.due = 0.0
        self.odue = 0.0
        self.count = 0
        self.mod = 0

    def addDataFromCard(self, idx, card, timeNow):
        if card.type > 0:
            newTotal = (self.avg_interval * self.count) + card.ivl

            self.count += 1
            self.avg_interval = newTotal / self.count
        if card.type == 2:
            if card.due < self.due or self.due == 0:
                self.due = card.due

            if card.odue < self.odue or self.odue == 0:
                self.odue = card.odue
                self.mod = self.odue

        if idx < self.idx or self.idx == 0:
            self.idx = idx

def isKanji(unichar):
    try:
        return unicodedata.name(unichar).find('CJK UNIFIED IDEOGRAPH') >= 0
    except ValueError:
        # a control character
        return False

def scoreAdjust(score):
    score += 1
    return 1 - 1 / (score * score)

def addUnitData(units, unitKey, i, card, timeNow):
    validKey = _ignore.find(unitKey) == -1 and (not _kanjionly or isKanji(unitKey))
    if validKey:
        if unitKey not in units:
            unit = TestedUnit(unitKey)
            units[unitKey] = unit

        units[unitKey].addDataFromCard(i, card, timeNow)

def hsvrgbstr(h, s=0.8, v=0.9):
    i = int(h*6.0)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0: return "#%0.2X%0.2X%0.2X" % (v*256,t*256,p*256)
    if i == 1: return "#%0.2X%0.2X%0.2X" % (q*256,v*256,p*256)
    if i == 2: return "#%0.2X%0.2X%0.2X" % (p*256,v*256,t*256)
    if i == 3: return "#%0.2X%0.2X%0.2X" % (p*256,q*256,v*256)
    if i == 4: return "#%0.2X%0.2X%0.2X" % (t*256,p*256,v*256)
    if i == 5: return "#%0.2X%0.2X%0.2X" % (v*256,p*256,q*256)

class KanjiGrid:
    def __init__(self, mw):
        if mw:
            self.menuAction = QAction("Generate Kanji Grid", mw)
            mw.connect(self.menuAction, SIGNAL("triggered()"), self.setup)
            mw.form.menuTools.addSeparator()
            mw.form.menuTools.addAction(self.menuAction)

    def generate(self, units, timeNow, saveMode=False):
        deckname = mw.col.decks.name(self.did).rsplit('::',1)[-1]
        if saveMode: cols = _wide
        else: cols = _thin
        self.html  = "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/>\n"
        self.html += "<html><head><title>Anki Kanji Grid</title></head><body bgcolor=\"#FFF\">\n"
        self.html += "<span style=\"font-size: 3em;color: #888;\">Kanji Grid - %s</span><br>\n" % deckname
        self.html += "<div style=\"margin-bottom: 24pt;padding: 20pt;\"><p style=\"float: left\">Key:</p>"
        self.html += "<style type=\"text/css\">.key{display:inline-block;width:3em}a,a:visited{color:#000;text-decoration:none;}</style>"
        self.html += "<p style=\"float: right\">Weak&nbsp;"
        for c in [n/6.0 for n in range(6+1)]:
            self.html += "<span class=\"key\" style=\"background-color: %s;\">&nbsp;</span>" % hsvrgbstr(c/2)
        self.html += "&nbsp;Strong</p></div>\n"
        self.html += "<div style=\"clear: both;\"><br><hr style=\"border-style: dashed;border-color: #666;width: 60%;\"><br></div>\n"
        self.html += "<center>\n"	
        if _group == 0:
            gc = 0
            kanji = list([u.value for u in units.values()])
            for i in range(1,len(_heisig)):
                self.html += "<h2 style=\"color:#888;\">%s</h2>\n" % _heisig[i][0]
                table = "<table width='85%'><tr>\n"
                count = -1
                for unit in [units[c] for c in _heisig[i][1] if c in kanji]:
                    if unit.count != 0 or _unseen:
                        score = "NaN"
                        count += 1
                        if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                        if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                        else: bgcolour = "#FFF"
                        if _tooltips:
                            tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                            tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                            tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                            table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                        else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                        table += "<a href=\"https://jisho.org/kanji/details/%s\">%s</a></td>\n" % (2*(unit.value,))
                table += "</tr></table>\n"
                n = count+1
                t = len(_heisig[i][1])
                gc += n
                if _unseen:
                    table += "<details><summary>Missing Kanji</summary><table style=\"max-width:75%;\"><tr>\n"
                    count = -1
                    for char in [c for c in _heisig[i][1] if c not in kanji]:
                        score = "NaN"
                        count += 1
                        if count % cols == 0: table += "</tr>\n<tr>\n"
                        if _tooltips:
                            tooltip  = "Character: %s" % (unicodedata.name(char))
                            table += "\t<td align=center valign=top style=\"background:#EEE;color:#FFF;\" title=\"%s\">" % (tooltip)
                        else: table += "\t<td align=center valign=top style=\"background:#EEE;color:#FFF;\">"
                        table += "<a href=\"https://jisho.org/kanji/details/%s\" style=\"color:#888;\">%s</a></td>\n" % (2*(char,))
                    if count == -1: table += "<strong style=\"color:#CCC\">None</strong>"
                    table += "</tr></table></details>\n"
                    self.html += "<h4 style=\"color:#888;\">%d of %d - %0.2f%%</h4>\n" % (n, t, n*100.0/t)
                    self.html += table
            chars = reduce(lambda x,y: x+y, dict(_heisig).values())
            table = "<table width='85%'><tr>\n"
            count = -1
            for unit in [u for u in units.values() if u.value not in chars]:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                    else: bgcolour = "#FFF"
                    if _tooltips:
                        tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                        tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                        tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                        table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                    else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                    table += "<a href=\"https://jisho.org/kanji/details/%s\">%s</a></td>\n" % (2*(unit.value,))
            table += "</tr></table>\n"
            n = count+1
            if count != -1:
                self.html += "<h2 style=\"color:#888;\">%s</h2>" % _heisig[0][0]
                self.html += "<h4 style=\"color:#888;\">%d</h4>\n" % n
                self.html += table		
        else:
            table = "<table width='85%'><tr>\n"
            if _group == 1: # Order found
                unitsList = sorted( units.values(), key=lambda unit: (unit.idx, unit.count) )
            if _group == 2: # Unicode index
                unitsList = sorted( units.values(), key=lambda unit: (unicodedata.name(unit.value), unit.count) )
            if _group == 3: # Character score
                unitsList = sorted( units.values(), key=lambda unit: (scoreAdjust(unit.avg_interval / _interval), unit.count), reverse=True)
            if _group == 4: # Deck frequency
                unitsList = sorted( units.values(), key=lambda unit: (unit.count, scoreAdjust(unit.avg_interval / _interval)), reverse=True)
            count = -1
            for unit in unitsList:
                if unit.count != 0 or _unseen:
                    score = "NaN"
                    count += 1
                    if count % cols == 0 and count != 0: table += "</tr>\n<tr>\n"
                    if unit.count != 0: bgcolour = hsvrgbstr(scoreAdjust(unit.avg_interval / _interval)/2)
                    else: bgcolour = "#FFF"
                    if _tooltips:
                        tooltip  = "Character: %s | Count: %s | " % (unicodedata.name(unit.value), unit.count)
                        tooltip += "Avg Interval: %s | Score: %s | " % (unit.avg_interval, score)
                        tooltip += "Background: %s | Index: %s" % (bgcolour, count)
                        table += "\t<td align=center valign=top style=\"background:%s;\" title=\"%s\">" % (bgcolour, tooltip)
                    else: table += "\t<td align=center valign=top style=\"background:%s;\">" % (bgcolour)
                    table += "<a href=\"https://jisho.org/kanji/details/%s\">%s</a></td>\n" % (2*(unit.value,))
            table += "</tr></table>\n"
            self.html += "<h4 style=\"color:#888;\">%d total unique kanji</h4>\n" % (count+1)
            self.html += table
        self.html += "</center></body></html>\n"

    def displaygrid(self, units, timeNow):
        self.generate(units, timeNow)
        #print("%s: %0.3f" % ("HTML generated",time.time()-_time))
        self.win = QDialog(mw)
        self.wv = AnkiWebView()
        vl = QVBoxLayout()
        vl.setMargin(0)
        vl.addWidget(self.wv)
        self.wv.stdHtml(self.html)
        hl = QHBoxLayout()
        vl.addLayout(hl)
        sh = QPushButton("Save HTML")
        hl.addWidget(sh)
        sh.connect(sh, SIGNAL("clicked()"), self.savehtml)
        sp = QPushButton("Save Image")
        hl.addWidget(sp)
        sp.connect(sp, SIGNAL("clicked()"), self.savepng)
        bb = QPushButton("Close")
        hl.addWidget(bb)
        bb.connect(bb, SIGNAL("clicked()"), self.win, SLOT("reject()"))
        self.win.setLayout(vl)
        self.win.resize(500, 400)
        #print("%s: %0.3f" % ("Window complete",time.time()-_time))
        return 0

    def savehtml(self):
        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QDesktopServices.storageLocation(QDesktopServices.DesktopLocation), "Web Page (*.html *.htm)")
        if fileName != "":
            mw.progress.start(immediate=True)
            if not ".htm" in fileName:
                fileName += ".html"
            fileOut = codecs.open(fileName, 'w', 'utf-8')
            (units, timeNow) = self.kanjigrid()
            self.generate(units, timeNow, True)
            fileOut.write(self.html)
            fileOut.close()
            mw.progress.finish()
            showInfo("Page saved to %s!" % os.path.abspath(fileOut.name))
        return
    
    def savepng(self):
        fileName = QFileDialog.getSaveFileName(self.win, "Save Page", QDesktopServices.storageLocation(QDesktopServices.DesktopLocation), "Portable Network Graphics (*.png)")
        if fileName != "":
            mw.progress.start(immediate=True)
            if not ".png" in fileName:
                fileName += ".png"
            p = self.wv.page()
            oldsize = p.viewportSize()
            p.setViewportSize(p.mainFrame().contentsSize())
            image = QImage(p.viewportSize(), QImage.Format_ARGB32)
            painter = QPainter(image)
            p.mainFrame().render(painter)
            painter.end()
            image.save(fileName, "png")
            p.setViewportSize(oldsize)
            mw.progress.finish()
            showInfo("Image saved to %s!" % os.path.abspath(fileName))
        return

    def kanjigrid(self):
        self.did = mw.col.conf['curDeck']

        dids = [self.did]
        for name, id in mw.col.decks.children(self.did):
            dids.append(id)
        #print("%s: %0.3f" % ("Decks selected",time.time()-_time))
        cids = mw.col.db.list("select id from cards where did in %s or odid in %s" % (ids2str(dids),ids2str(dids)))
        #print("%s: %0.3f" % ("Cards selected",time.time()-_time))

        units = dict()
        notes = dict()
        timeNow = time.time()
        for id,i in enumerate(cids):
            card = mw.col.getCard(i)
            if card.nid not in notes.keys():
                keys = card.note().keys()
                unitKey = None
                if _literal:
                    for s,key in ((key.lower(),key) for key in keys):
                        if _pattern == s.lower():
                            unitKey = card.note()[key]
                            break
                else:
                    for s,key in ((key.lower(),key) for key in keys):
                        if _pattern in s.lower():
                            unitKey = card.note()[key]
                            break
                notes[card.nid] = unitKey
            else:
                unitKey = notes[card.nid]
            if unitKey != None:
                for ch in unitKey:
                    addUnitData(units, ch, i, card, timeNow)
        #print("%s: %0.3f" % ("Units created",time.time()-_time))
        return units,timeNow

    def makegrid(self):
        #global _time
        #_time = time.time()
        #print("%s: %0.3f" % ("Start",time.time()-_time))
        (units, timeNow) = self.kanjigrid()
        if units is not None:
            self.displaygrid(units, timeNow)

    def setup(self):
        global _pattern, _literal
        global _interval, _thin, _wide
        global _group, _unseen, _tooltips
        swin = QDialog(mw)
        vl = QVBoxLayout()
        frm = QGroupBox("Settings")
        vl.addWidget(frm)
        il = QVBoxLayout()
        fl = QHBoxLayout()
        field = QLineEdit()
        field.setPlaceholderText("e.g. \"Expression\" or \"Kanji\" (Default: \"Expression\")")
        il.addWidget(QLabel("Pattern or Field name to search for (first used, case insensitive):"))
        fl.addWidget(field)
        liter = QCheckBox("Match exactly")
        liter.setChecked(_literal)
        fl.addWidget(liter)
        il.addLayout(fl)
        stint = QSpinBox()
        stint.setRange(1,65536)
        stint.setValue(_interval)
        il.addWidget(QLabel("Card interval considered strong:"))
        il.addWidget(stint)
        ttcol = QSpinBox()
        ttcol.setRange(1,99)
        ttcol.setValue(_thin)
        il.addWidget(QLabel("Number of Columns in the in-app table:"))
        il.addWidget(ttcol)
        wtcol = QSpinBox()
        wtcol.setRange(1,99)
        wtcol.setValue(_wide)
        il.addWidget(QLabel("Number of Columns in the exported table:"))
        il.addWidget(wtcol)
        group = QComboBox()
        group.addItems(["RTK",
                        "None, Sorted by Order Found",
                        "None, Sorted by Unicode Order",
                        "None, Sorted by Score",
                        "None, Sorted by Frequency"])
        group.setCurrentIndex(_group)
        il.addWidget(QLabel("Group by:"))
        il.addWidget(group)
        shnew = QCheckBox("Show units not yet seen")
        shnew.setChecked(_unseen)
        il.addWidget(shnew)
        toolt = QCheckBox("Show informational tooltips")
        toolt.setChecked(_tooltips)
        il.addWidget(toolt)
        frm.setLayout(il)
        hl = QHBoxLayout()
        vl.addLayout(hl)
        gen = QPushButton("Generate")
        hl.addWidget(gen)
        gen.connect(gen, SIGNAL("clicked()"), swin, SLOT("accept()"))
        cls = QPushButton("Close")
        hl.addWidget(cls)
        cls.connect(cls, SIGNAL("clicked()"), swin, SLOT("reject()"))
        swin.setLayout(vl)
        swin.setTabOrder(gen,cls)
        swin.setTabOrder(cls,field)
        swin.setTabOrder(field,liter)
        swin.setTabOrder(liter,stint)
        swin.setTabOrder(stint,ttcol)
        swin.setTabOrder(ttcol,wtcol)
        swin.setTabOrder(wtcol,group)
        swin.setTabOrder(group,shnew)
        swin.setTabOrder(shnew,toolt)
        swin.resize(500, 400)
        if swin.exec_():
            mw.progress.start(immediate=True)
            if len(field.text().strip()) != 0: _pattern = field.text().lower()
            _literal = liter.isChecked()
            _interval = stint.value()
            _thin = ttcol.value()
            _wide = wtcol.value()
            _group = group.currentIndex()
            _unseen = shnew.isChecked()
            _tooltips = toolt.isChecked()
            self.makegrid()
            mw.progress.finish()
            self.win.show()

if __name__ != "__main__":
    # Save a reference to the toolkit onto the mw, preventing garbage collection of PyQT objects
    if mw: mw.kanjigrid = KanjiGrid(mw)
else:
    print "This is a plugin for the Anki Spaced Repition learning system and cannot be run directly."
    print "Please download Anki2 from <http://ankisrs.net/>"

# vim:expandtab:
