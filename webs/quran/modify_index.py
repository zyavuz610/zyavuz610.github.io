import re

with open("index.v3.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the input placeholder
old_placeholder = 'placeholder="Kelime veya kök arayın... (Örn: kitab, beyt)"'
new_placeholder = 'placeholder="Kelime veya kök arayın... (Örn: kitab, sebil, harb)"'
content = content.replace(old_placeholder, new_placeholder)

# Replace the buttons
old_buttons = '''                <div class="d-flex gap-2 justify-content-center flex-wrap mt-2">
                    <small class="text-white-50">Dene:</small>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('kitab')">Kitâb</button>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('beyt')">Beyt</button>
                </div>'''
new_buttons = '''                <div class="d-flex gap-2 justify-content-center flex-wrap mt-2">
                    <small class="text-white-50">Dene:</small>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('kitab')">Kitâb</button>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('beyt')">Beyt</button>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('harb')">Harb</button>
                    <button class="btn btn-outline-light btn-sm rounded-pill" onclick="quickSearch('sebil')">Sebîl</button>
                </div>'''
content = content.replace(old_buttons, new_buttons)

# Replace the "Şu an aranabilir" text
old_aranabilir = '<p class="text-muted small">Şu an aranabilir: <strong>Kitâb</strong>, <strong>Beyt</strong></p>'
new_aranabilir = '<p class="text-muted small">Şu an aranabilir: <strong>Kitâb, Beyt, Harb, Nâr, Dâr, Zirâ\', Ricl, Rahim, Rîh, Sebîl, Sehâb, Sikkîn</strong></p>'
content = content.replace(old_aranabilir, new_aranabilir)

new_words_code = """/* ================================================================
   WORDS VERİ TABANI — Akıllı Kur'an Sözlüğü
   ----------------------------------------------------------------
   YENİ KELİME EKLEMEK İÇİN:
     1. Bu dosyada WORDS nesnesine yeni bir blok ekleyin.
     2. "searchKeys" alanına kullanıcının yazabileceği
        Türkçe/Arapça/Latin varyantlarını ekleyin.
     3. Başka hiçbir yere dokunmanıza gerek yok —
        arama fonksiyonu searchKeys'i otomatik tarar.

   Her "context" (bağlam) alanları:
     label      : Kısa etiket (numara + ad)
     sourceType : "quran" | "hadis" | "siir" | "hikmet"
     reference  : Kaynak bilgisi (sure:ayet, hadis, yazar)
     title      : Bağlamın Türkçe başlığı
     description: Açıklama
     highlight  : true → kart sarı kenarlıklı gösterilir
     image      : { url, alt, icon }
       url  → Wikimedia Commons vb. açık lisanslı direkt link
       alt  → erişilebilirlik metni
       icon → URL yüklenemezse gösterilecek Font Awesome sınıfı
   ================================================================ */

const WORDS = {

    /* ──────────────────────────────────────────────
       KİTÂB  كِتَاب  (K-T-B)
       ────────────────────────────────────────────── */
    kitab: {
        searchKeys: ["kitab", "ktb", "kitâb", "كتاب"],
        title: "Kitâb",
        arabic: "كِتَاب",
        root: "Kök: K-T-B",
        plurals: [
            { arabic: "كُتُب",  transliteration: "Kutub"  },
            { arabic: "أَكْتَاب", transliteration: "Ektâb" }
        ],
        frequency: { percent: 85, label: "Kur'an'da 261 kez geçer." },
        collocations: ["Kitâbun Mübîn", "Ehl-i Kitâb", "Ümmü'l Kitâb"],
        contexts: [
            {
                label: "1. Vahyedilen Kitap",
                sourceType: "quran",
                reference: "Bakara 2:2 — «Zâlikel kitâbu lâ reybe fîh...»",
                title: "Kur'an-ı Kerim / İlahi Vahiy",
                description: "Bu bağlamda kelime, Allah tarafından indirilen rehber ve kutsal metni ifade eder.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Quran_Kareem.jpg/320px-Quran_Kareem.jpg", alt: "Kur'an-ı Kerim", icon: "fa-book-open" }
            },
            {
                label: "2. Kader / Hüküm",
                sourceType: "quran",
                reference: "Enfal 8:68 — «Lev lâ kitâbun minallâhi sebeka...»",
                title: "Yazılı Hüküm / Kader / Kanun",
                description: "Kelime burada fiziksel bir kitaptan ziyade, Allah'ın takdiri veya ezeli hükmü anlamına gelmektedir.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Ottoman_calligraphy_Allah.jpg/320px-Ottoman_calligraphy_Allah.jpg", alt: "İslam hat sanatı", icon: "fa-scroll" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       BEYT  بَيْت  (B-Y-T)
       ────────────────────────────────────────────── */
    beyt: {
        searchKeys: ["beyt", "byt", "بيت", "بَيْت"],
        title: "Beyt",
        arabic: "بَيْت",
        root: "Kök: B-Y-T",
        plurals: [
            { arabic: "بُيُوت", transliteration: "Buyût" },
            { arabic: "أَبْيَات", transliteration: "Ebyât" }
        ],
        frequency: { percent: 72, label: "Kur'an'da 70'ten fazla farklı türevle geçer." },
        collocations: ["Ehlü'l-Beyt", "Beytullâh", "Beytü'l-Makdis", "Beytü'l-Mâl", "el-Beytü'l-Harâm"],
        contexts: [
            {
                label: "1. Mesken / Barınak",
                sourceType: "quran",
                reference: "Nuh 71:28",
                title: "Mesken — İkamet İçin Hazırlanmış Yer",
                description: "Temel anlam: barınma ve oturmak üzere hazırlanmış mekân. Sıradan konut kastedilir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Traditional-courtyard-house.jpg/320px-Traditional-courtyard-house.jpg", alt: "Geleneksel avlulu ev", icon: "fa-house" }
            },
            {
                label: "2. Ehl-i Beyt (1) — Peygamberin Ailesi",
                sourceType: "quran",
                reference: "Ahzab 33:33",
                title: "Ehl-i Beyt — Hz. Peygamber'in Ailesi",
                description: "Burada Beyt, Hz. Peygamber'in kutsal hanesini simgeler. 'Ehl-i Beyt' tabiri özel anlam kazanmıştır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Rawdat_al-Sharif.jpg/320px-Rawdat_al-Sharif.jpg", alt: "Hz. Peygamberin türbesi", icon: "fa-mosque" }
            },
            {
                label: "3. Ehl-i Beyt (2) — Erkeğin Ailesi",
                sourceType: "quran",
                reference: "Kasas 28:12",
                title: "Ehl-i Beyt (2) — Erkeğin Bakmakla Yükümlü Olduğu Kişiler",
                description: "Bu kullanımda Beyt; erkeğin evi ve bakmakla yükümlü olduğu aile bireylerini kapsar.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Muslim_Family.jpg/320px-Muslim_Family.jpg", alt: "Müslüman aile", icon: "fa-people-roof" }
            },
            {
                label: "4. Beytü'ş-Şi'r — Şiir Beyti",
                sourceType: "siir",
                reference: "Aruz ve kafiye ilmi",
                title: "Şiir Beyti — Aruz Ölçüsüyle İki Mısra",
                description: "Arapça şiirde 'beyt', iki mısradan oluşan ve belirli vezin ile kafiyeye sahip şiir birimidir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Diwan_of_Hafiz%2C_Iran%2C_late_16th_century%2C_ink%2C_opaque_watercolor%2C_and_gold_on_paper_-_Freer_Gallery_of_Art_-_DSC04131.JPG/320px-Diwan_of_Hafiz%2C_Iran%2C_late_16th_century%2C_ink%2C_opaque_watercolor%2C_and_gold_on_paper_-_Freer_Gallery_of_Art_-_DSC04131.JPG", alt: "Divan şiiri el yazması", icon: "fa-feather" }
            },
            {
                label: "5. Beytü'l-Kasîde",
                sourceType: "siir",
                reference: "Ebu Said es-Sükkerî / Ahmet Şevki",
                title: "Kasidede En Güzel Beyit",
                description: "Bir kasidenin en güçlü ve en anlamlı beytidir; tıpkı yılanın kafası gibi kasidenin ruhu sayılır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Arabic_calligraphy_quran.jpg/320px-Arabic_calligraphy_quran.jpg", alt: "Arapça hat sanatı", icon: "fa-feather-pointed" }
            },
            {
                label: "6. Beytü'l-Kavim",
                sourceType: "siir",
                reference: "İbnü'l-Hira et-Teymî",
                title: "Kabilenin Hanesi — Soylu Aile",
                description: "Kabilenin ileri gelenlerini ve şerefli ailesini ifade eder. Önderliğin ve soyluluğun simgesidir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Bedouin_black_tent.jpg/320px-Bedouin_black_tent.jpg", alt: "Bedevi siyah çadır", icon: "fa-tent" }
            },
            {
                label: "7. Beytullâh — Kâbe",
                sourceType: "quran",
                reference: "Kureyş 106:3",
                title: "Beytullâh — Kâbe-i Müşerrefe",
                description: "Mekke'deki Kâbe'nin Kur'anî adıdır. Müslümanların kıblesi ve hac mekânıdır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Mecca_Kaaba.JPG/320px-Mecca_Kaaba.JPG", alt: "Kâbe-i Müşerrefe, Mekke", icon: "fa-kaaba" }
            },
            {
                label: "8. Beytü'l-Mâl",
                sourceType: "hikmet",
                reference: "İbn Teymiyye — es-Siyâsetü'ş-Şer'iyye",
                title: "Beytü'l-Mâl — Devlet Hazinesi",
                description: "Devlet gelirlerinin ve kamu mallarının muhafaza edildiği hazinedir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Islamic_Coins.jpg/320px-Islamic_Coins.jpg", alt: "İslam dönemi sikkeleri", icon: "fa-coins" }
            },
            {
                label: "9. Beytü'l-Makdis",
                sourceType: "hadis",
                reference: "Hadis-i Nebevî — İsrâ rivayeti",
                title: "Beytü'l-Makdis — Mescid-i Aksa",
                description: "İsrâ hadisesinde geçen kutsal mekân; Kudüs'teki Mescid-i Aksa'yı ve çevresini ifade eder.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Jerusalem_Al-Aqsa_Mosque_BW_1.JPG/320px-Jerusalem_Al-Aqsa_Mosque_BW_1.JPG", alt: "Mescid-i Aksa, Kudüs", icon: "fa-mosque" }
            },
            {
                label: "10. Buyûtullâh — Camiler",
                sourceType: "quran",
                reference: "Nur 24:36",
                title: "Buyûtullâh — Allah'ın Evleri (Camiler)",
                description: "Camiler için kullanılan çoğul form. Allah'ın adının zikredildiği kutsal ibadet mekânlarıdır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Sultan_Ahmed_mosque_interior.jpg/320px-Sultan_Ahmed_mosque_interior.jpg", alt: "Cami iç mimarisi", icon: "fa-mosque" }
            },
            {
                label: "11. el-Beytü'l-Harâm",
                sourceType: "quran",
                reference: "Maide 5:97",
                title: "el-Beytü'l-Harâm — Dokunulmaz Kâbe",
                description: "Kâbe'nin başka bir Kur'anî adıdır; kutsal ve dokunulmaz olduğu, savaşın yasak olduğu bölgeyi ifade eder.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Mecca_Kaaba.JPG/320px-Mecca_Kaaba.JPG", alt: "el-Beytü'l-Harâm — Kâbe", icon: "fa-kaaba" }
            },
            {
                label: "12. el-Beytü'l-Atîk",
                sourceType: "quran",
                reference: "Hac 22:29",
                title: "el-Beytü'l-Atîk — Kadim ve Özgür Kâbe",
                description: "'Atîk' eski/özgür demektir. Kâbe'nin tarihî derinliğine ve hiçbir zorbanın tahakkümüne girmediğine işaret eder.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Mecca_Kaaba.JPG/320px-Mecca_Kaaba.JPG", alt: "el-Beytü'l-Atîk", icon: "fa-kaaba" }
            },
            {
                label: "13. el-Beytü'l-Muharrem",
                sourceType: "hadis",
                reference: "Tarife el-Himyeriyye / M. Hasan Nîlek",
                title: "el-Beytü'l-Muharrem — Hürmete Layık Kâbe",
                description: "Kâbe'ye duyulan büyük saygı ve hürmeti ön plana çıkaran; özellikle şiir ve edebiyatta görülen kullanım.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Mecca_Kaaba.JPG/320px-Mecca_Kaaba.JPG", alt: "el-Beytü'l-Muharrem", icon: "fa-kaaba" }
            },
            {
                label: "14. el-Beytü'l-Ma'mûr",
                sourceType: "quran",
                reference: "Tur 52:4",
                title: "el-Beytü'l-Ma'mûr — Gökteki Meskûn Ev",
                description: "Yedinci katta, meleklerin ibadet ettiği ve Kâbe'nin tam karşısında olduğu rivayet edilen kutsal mekân.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Milky_way_2.jpg/320px-Milky_way_2.jpg", alt: "Semavî temsil", icon: "fa-star-and-crescent" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       HARB  حَرْب  (H-R-B)
       ────────────────────────────────────────────── */
    harb: {
        searchKeys: ["harb", "hrb", "savaş", "حرب", "حَرْب"],
        title: "Harb",
        arabic: "حَرْب",
        root: "Kök: H-R-B",
        plurals: [
            { arabic: "حُرُوب", transliteration: "Hurûb" }
        ],
        frequency: { percent: 55, label: "Kur'an'da farklı türevleriyle geçer." },
        collocations: ["Fî sebîlillâh", "Dârü'l-harb", "Ehlü'l-harb"],
        contexts: [
            {
                label: "1. Silahlı Çatışma / Savaş",
                sourceType: "quran",
                reference: "Mâide 5:64 — «Küllema evkadû nâran lil-harbi etfee'hallâh...»",
                title: "Savaş — İki Taraf Arasında Silahlı Çatışma",
                description: "Temel anlam: iki grup arasındaki silahlı mücadele. Kur'an'da savaşın yıkıcılığı ve Allah'ın onu söndürmesi bağlamında kullanılır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Battle_of_Badr.jpg/320px-Battle_of_Badr.jpg", alt: "Bedir Savaşı tasviri", icon: "fa-shield-halved" }
            },
            {
                label: "2. Savaşın Sona Ermesi",
                sourceType: "quran",
                reference: "Muhammed 47:4 — «Hattâ teda'al-harbu evzârehâ...»",
                title: "Savaşın Yüklerini Bırakması — Barış",
                description: "Kelime burada savaşın bitmesini ve silahların bırakılmasını ifade eder. Barışa olan vurgu öne çıkar.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Olive_branch.jpg/320px-Olive_branch.jpg", alt: "Barış sembolü zeytin dalı", icon: "fa-dove" }
            },
            {
                label: "3. Savaş Hilesi (Hadis)",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «el-Harbu hud'a»",
                title: "Harp Hiledir — Savaş Stratejisi",
                description: "Hz. Peygamber'in meşhur hadisi: savaş bir hile/strateji sanatıdır; düşmanı yanıltmak caizdir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Sword_of_Islam.jpg/320px-Sword_of_Islam.jpg", alt: "İslam kılıcı sembolü", icon: "fa-swords" }
            },
            {
                label: "4. Günlük Kullanım",
                sourceType: "hikmet",
                reference: "Özlü söz — «Lâ tuşâvir bahîlen fî sıla...»",
                title: "Savaş — Gündelik ve Mecazî Kullanım",
                description: "Cimriyle silaya, korkakla savaşa, gençle cariyeye danışma. Savaş bağlamında cesaret ve danışma önemine dikkat çekilir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Chess_board_with_chess_pieces_01.jpg/320px-Chess_board_with_chess_pieces_01.jpg", alt: "Strateji ve harp", icon: "fa-chess" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       NÂR  نَار  (N-V-R)
       ────────────────────────────────────────────── */
    nar: {
        searchKeys: ["nar", "nâr", "nvr", "ateş", "نار", "نَار"],
        title: "Nâr",
        arabic: "نَار",
        root: "Kök: N-V-R",
        plurals: [
            { arabic: "نِيرَان", transliteration: "Nîrân" }
        ],
        frequency: { percent: 78, label: "Kur'an'da 145 kez geçer." },
        collocations: ["Nâru cehennem", "Ehlü'n-nâr", "Nârun mübâreke"],
        contexts: [
            {
                label: "1. Fiziksel Ateş / Alev",
                sourceType: "quran",
                reference: "Neml 27:8 — «Felemma câehâ nûdiye en bûrike men fi'n-nâr...»",
                title: "Ateş — Odun veya Kömürün Yanmasıyla Oluşan Alev",
                description: "Temel anlam: ışık saçan, yakan fiziksel ateş. Hz. Musa'nın kutsal ateşle karşılaşması bağlamında kullanılmıştır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Campfire_at_night.jpg/320px-Campfire_at_night.jpg", alt: "Gece ateşi", icon: "fa-fire" }
            },
            {
                label: "2. Cehennem Ateşi",
                sourceType: "quran",
                reference: "Hadis-i Şerif — «Lâ tekûmu's-sâ'atu hattâ tahruce nârun min ardi'l-Hicâz...»",
                title: "Cehennem / Ahiret Azabı",
                description: "Ateş, Kur'an'da çoklukla ahiretteki azap mekânını simgeler. Bu kullanım hem fiziksel hem manevi boyut taşır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Lava_Fountain.jpg/320px-Lava_Fountain.jpg", alt: "Yanardağ lavı", icon: "fa-volcano" }
            },
            {
                label: "3. Ateş — Atasözü / Özlü Söz",
                sourceType: "hikmet",
                reference: "Özlü söz — «Eşheru min nârin alâ 'alam»",
                title: "Ateş — 'Bayrak Üzerindeki Ateş Gibi Meşhur'",
                description: "Şöhret ve göz önünde olmayı ifade eden meşhur atasözünde ateş, görünürlük ve parlaklığın sembolüdür.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Lighthouse_at_Cape_Hatteras.jpg/320px-Lighthouse_at_Cape_Hatteras.jpg", alt: "Fener kulesi ateşi", icon: "fa-lightbulb" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       DÂR  دَار  (D-V-R)
       ────────────────────────────────────────────── */
    dar: {
        searchKeys: ["dar", "dâr", "dvr", "ev", "دار", "دَار"],
        title: "Dâr",
        arabic: "دَار",
        root: "Kök: D-V-R",
        plurals: [
            { arabic: "دُورٌ",   transliteration: "Dûr"    },
            { arabic: "دِيَارٌ", transliteration: "Diyâr"  },
            { arabic: "دِيَارَةٌ", transliteration: "Diyâre" },
            { arabic: "دَارَاتٌ", transliteration: "Dârât"  }
        ],
        frequency: { percent: 62, label: "Kur'an'da çeşitli türevleriyle geçer." },
        collocations: ["Dârü'l-harb", "Dârü's-selâm", "Dârü'l-âhire", "Dârü'l-İslâm"],
        contexts: [
            {
                label: "1. İkametgâh / Mesken",
                sourceType: "quran",
                reference: "Kasas 28:81 — «Fehesefnâ bihi ve bidârihi'l-ard...»",
                title: "Ev / İkametgâh — Oturulan Yer",
                description: "Temel anlam: kişinin yaşadığı, ikamet ettiği yer. Karun'un evi yere batırılması bağlamında geçer.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Traditional-courtyard-house.jpg/320px-Traditional-courtyard-house.jpg", alt: "Geleneksel Arap evi", icon: "fa-house" }
            },
            {
                label: "2. En Hayırlı Ev (Hadis)",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «İnne hayra dûri'l-Ensâr dâru benî'n-Neccâr...»",
                title: "En Hayırlı Ev — Şeref ve Fazilet",
                description: "Hz. Peygamber Ensar'ın evleri arasında en hayırlısını sıralar. Ev kelimesi burada kabilenin yurdu anlamına gelir.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Rawdat_al-Sharif.jpg/320px-Rawdat_al-Sharif.jpg", alt: "Medine", icon: "fa-mosque" }
            },
            {
                label: "3. Komşu ve Ev (Özlü Söz)",
                sourceType: "hikmet",
                reference: "Mthel — «el-Câru kable'd-dâr ve'r-refîku kable't-tarîk»",
                title: "Önce Komşu Sonra Ev — Sosyal Değer",
                description: "Meşhur Arapça atasözü: ev almadan önce komşuya bak, yola çıkmadan önce yol arkadaşını seç.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Neighbourhood_-_geograph.org.uk_-_1461317.jpg/320px-Neighbourhood_-_geograph.org.uk_-_1461317.jpg", alt: "Komşuluk mahallesi", icon: "fa-people-roof" }
            },
            {
                label: "4. Dârü'l-Âhire — Ahiret Yurdu",
                sourceType: "quran",
                reference: "Kasas 28:83 — «Tilke'd-dârü'l-âhiratu nec'aluhâ...»",
                title: "Ahiret Yurdu — Kalıcı Ev",
                description: "Kelime mecazî olarak ahireti, yani ölüm sonrasındaki gerçek ve kalıcı yurdu ifade eder.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Milky_way_2.jpg/320px-Milky_way_2.jpg", alt: "Semavî temsil", icon: "fa-star-and-crescent" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       ZİRÂ'  ذِرَاع  (D-R-A)
       ────────────────────────────────────────────── */
    zira: {
        searchKeys: ["zira", "zirâ", "dra", "kol", "ذراع", "ذِرَاع"],
        title: "Zirâ'",
        arabic: "ذِرَاع",
        root: "Kök: D-R-A",
        plurals: [
            { arabic: "أَذْرُع",   transliteration: "Ezrü'" },
            { arabic: "ذُرْعَان", transliteration: "Zur'ân" }
        ],
        frequency: { percent: 30, label: "Kur'an'da sınırlı sayıda geçer." },
        collocations: ["Zirâü'l-köpek", "Zirâ' ölçüsü"],
        contexts: [
            {
                label: "1. Kol — Dirsekten Orta Parmağa",
                sourceType: "quran",
                reference: "Kehf 18:18 — «Ve kelbuhum bâsitun zirâ'ayhi bi'l-vasîd»",
                title: "Kol — Dirsek ile Orta Parmak Arası Uzuv",
                description: "Temel anlam: insan ya da hayvanın ön kolu. Kehf ashabının köpeği kollarını uzatmış uyur hâlde tasvir edilir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Dog_on_Mat.jpg/320px-Dog_on_Mat.jpg", alt: "Uzanan köpek", icon: "fa-dog" }
            },
            {
                label: "2. Zirâ' — Uzunluk Ölçü Birimi",
                sourceType: "hikmet",
                reference: "Hadis-i Şerif — «Lev du'îtu ilâ zirâ'in ev kurâ'in le-ecebtu»",
                title: "Zirâ' — Tarihî Uzunluk Ölçüsü (≈ 46 cm)",
                description: "Kelime aynı zamanda dirsekten parmak ucuna kadar olan mesafeyi temel alan eski bir uzunluk ölçüsüdür. Hadiste mütevazı daveti kabul etme erdemi anlatılır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Units_of_measurement.jpg/320px-Units_of_measurement.jpg", alt: "Ölçüm birimleri", icon: "fa-ruler" }
            },
            {
                label: "3. Kol — Özlü Söz",
                sourceType: "hikmet",
                reference: "Mthel — «Lâ tut'im el-'abde'l-kurâ' feyatma' fi'z-zirâ'»",
                title: "Kola Göz Dikmek — Açgözlülük Atasözü",
                description: "Köleye paça verme ki kola göz dikmesin. Küçük bir iyiliğin daha büyük taleplere kapı aralayabileceği uyarısı.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Hand_open.jpg/320px-Hand_open.jpg", alt: "Açık el", icon: "fa-hand" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       RİCL  رِجْل  (R-C-L)
       ────────────────────────────────────────────── */
    ricl: {
        searchKeys: ["ricl", "ricil", "rjl", "bacak", "ayak", "رجل", "رِجْل"],
        title: "Ricl",
        arabic: "رِجْل",
        root: "Kök: R-C-L",
        plurals: [
            { arabic: "أَرْجُل", transliteration: "Ercül" }
        ],
        frequency: { percent: 40, label: "Kur'an'da çeşitli bağlamlarda geçer." },
        collocations: ["Ricleyk (iki ayak)", "Alâ riclin (tek ayak üstünde)"],
        contexts: [
            {
                label: "1. Bacak / Ayak — Uzuv",
                sourceType: "quran",
                reference: "Sâd 38:42 — «Urkud bi-riclika hâzâ mugteselun bâridun ve şerâb»",
                title: "Bacak/Ayak — Uyluktan Ayağa Kadar Olan Uzuv",
                description: "Hz. Eyyub'a ayağıyla yere vurması emredilir; böylece şifa veren bir su çıkar. Temel anatomi anlamında kullanılmıştır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Barefeet.jpg/320px-Barefeet.jpg", alt: "Ayak", icon: "fa-person-walking" }
            },
            {
                label: "2. Tek Ayak Üzerinde Durmak",
                sourceType: "hikmet",
                reference: "Deyim — «Vakafe alâ riclin»",
                title: "Tek Ayak Üzerinde Durmak — Kararsızlık / Hazırlık",
                description: "Mecazî kullanım: bir konuda kararsız kalmak ya da hareket etmeye hazır olmak anlamında kullanılan deyim.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Balance.jpg/320px-Balance.jpg", alt: "Denge", icon: "fa-scale-balanced" }
            },
            {
                label: "3. Bir Ayak Öne Bir Ayak Geri",
                sourceType: "hikmet",
                reference: "Deyim — «Kâne yukaddim riclen ve yu'ehhiru uhrâ»",
                title: "Tereddüt — Kararsızlık Deyimi",
                description: "Bir ayağını öne diğerini arkaya atmak: bir konuda ileri geri gitmek, karar verememek anlamında mecazî deyim.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Walking_footsteps.jpg/320px-Walking_footsteps.jpg", alt: "Ayak izleri", icon: "fa-shoe-prints" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       RAHİM  رَحِم  (R-H-M)
       ────────────────────────────────────────────── */
    rahim: {
        searchKeys: ["rahim", "rhm", "rahm", "رحم", "رَحِم"],
        title: "Rahim",
        arabic: "رَحِم",
        root: "Kök: R-H-M",
        plurals: [
            { arabic: "أَرْحَام", transliteration: "Erhâm" }
        ],
        frequency: { percent: 48, label: "Kur'an'da hem organ hem akrabalık anlamıyla geçer." },
        collocations: ["Sılatü'r-rahm", "Kat'ü'r-rahm", "Erhâm (çoğul)"],
        contexts: [
            {
                label: "1. Rahim — Anatomi / Organ",
                sourceType: "quran",
                reference: "Âl-i İmrân 3:6 — «Huve'llezî yusavviruküm fi'l-erhâmi keyfe yeşâ'»",
                title: "Rahim — Ceninin Oluştuğu Organ",
                description: "Allah, rahimlerde insanı dilediği gibi şekillendirir. Kelime burada biyolojik organ anlamındadır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Pregnant_woman.jpg/320px-Pregnant_woman.jpg", alt: "Hamile kadın", icon: "fa-baby" }
            },
            {
                label: "2. Akrabalık Bağı",
                sourceType: "quran",
                reference: "Muhammed 47:22 — «...ve tukattı'û erhâmekum»",
                title: "Akrabalık — Kan Bağı ve Sıla-i Rahm",
                description: "Kelime mecazî olarak akrabalık bağını ifade eder. Akraba ilişkilerini koparmak Kur'an'da şiddetle kınanır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Muslim_Family.jpg/320px-Muslim_Family.jpg", alt: "Aile bağı", icon: "fa-people-roof" }
            },
            {
                label: "3. Akraba Ziyareti — Hadis",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «Lâ yadhuhu'l-cennete kâtı'u rahm»",
                title: "Sıla-i Rahm — Akrabayı Ziyaret Etme Fazileti",
                description: "Akrabalık bağını koparan cennete giremez. Hadis, rahim kelimesinin sosyal ve ahlakî boyutunu ortaya koyar.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Family_gathering.jpg/320px-Family_gathering.jpg", alt: "Aile buluşması", icon: "fa-heart" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       RÎH  رِيح  (R-V-H)
       ────────────────────────────────────────────── */
    rih: {
        searchKeys: ["rih", "rvh", "rüzgar", "rüzgâr", "ريح", "رِيح"],
        title: "Rîh",
        arabic: "رِيح",
        root: "Kök: R-V-H",
        plurals: [
            { arabic: "رِيَاح",   transliteration: "Riyâh"  },
            { arabic: "أَرْيَاح", transliteration: "Eryâh"  }
        ],
        frequency: { percent: 52, label: "Kur'an'da 29 kez geçer." },
        collocations: ["Rîhu'l-'âsife", "Riyâhu'l-mübeşşirât", "Fî rîhik (mecaz)"],
        contexts: [
            {
                label: "1. Rüzgar — Hareket Eden Hava",
                sourceType: "quran",
                reference: "Enbiyâ 21:81 — «Ve li-Süleymâne'r-rîha âsıfeten tecrî bi-emrih»",
                title: "Rüzgar — Fiziksel Hava Akımı",
                description: "Hz. Süleyman'ın emrine boyun eğen fırtınalı rüzgar. Kelime burada Allah'ın yarattığı doğal güç olarak geçmektedir.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Dust_storm_Texas_1935.jpg/320px-Dust_storm_Texas_1935.jpg", alt: "Kum fırtınası", icon: "fa-wind" }
            },
            {
                label: "2. Rüzgar — Rahmet ve Azap",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «Lâ tesubbü'r-rîha fe-innehâ min rûhi'llâh...»",
                title: "Rüzgarı Sövmeyin — Rahmet ve Azap Aracı",
                description: "Rüzgara sövmeyin; o Allah'ın rahmetini de azabını da getirir. Rüzgar ilahi iradenin bir aracı olarak tasvir edilir.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Rain_cloud.jpg/320px-Rain_cloud.jpg", alt: "Yağmur bulutu", icon: "fa-cloud-rain" }
            },
            {
                label: "3. Rüzgar — Atasözü",
                sourceType: "hikmet",
                reference: "Mthel — «Tecrî'r-riyâhu bimâ lâ teştehî's-sufun»",
                title: "Rüzgar İstediğin Gibi Esmez — Kader",
                description: "Meşhur Arapça atasözü: rüzgar gemilerin istediği gibi değil, kendi yönünde eser. Kadere boyun eğmeyi simgeler.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Sailing_boat_wind.jpg/320px-Sailing_boat_wind.jpg", alt: "Yelkenli tekne", icon: "fa-sailboat" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       SEBİL  سَبِيل  (S-B-L)
       ────────────────────────────────────────────── */
    sebil: {
        searchKeys: ["sebil", "sabil", "sbl", "yol", "سبيل", "سَبِيل"],
        title: "Sebîl",
        arabic: "سَبِيل",
        root: "Kök: S-B-L",
        plurals: [
            { arabic: "أَسْبِلَة", transliteration: "Esbile" },
            { arabic: "سُبُل",    transliteration: "Sübül"  }
        ],
        frequency: { percent: 67, label: "Kur'an'da çok sayıda ayette geçer." },
        collocations: ["Fî sebîlillâh", "Sebîlü'l-hak", "Sebîlü'r-rüşd"],
        contexts: [
            {
                label: "1. Yol — Fiziksel Patika",
                sourceType: "quran",
                reference: "En'âm 6:153 — «Ve lâ tettebiu's-sübüle fe-tefferrage biküm an sebîlih»",
                title: "Yol / Patika — Fiziksel ve Manevi Güzergâh",
                description: "Allah'ın yoluna uyun, başka yollara gitmeyin; yoksa sizi dağıtır. Kelime hem somut yol hem doğru yol anlamı taşır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Desert_road.jpg/320px-Desert_road.jpg", alt: "Çöl yolu", icon: "fa-road" }
            },
            {
                label: "2. Fî Sebîlillâh — Allah Yolunda",
                sourceType: "quran",
                reference: "Kur'an geneli",
                title: "Fî Sebîlillâh — Allah Yolunda Harcama ve Cihad",
                description: "Kelime Allah yolunda yapılan her türlü fedakârlığı, harcamayı ve çabayı kapsar. Cihad, sadaka ve ilim öğrenmek bu kapsamdadır.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Quran_open.jpg/320px-Quran_open.jpg", alt: "Açık Kur'an", icon: "fa-book-open" }
            },
            {
                label: "3. Başarıya Giden Yol",
                sourceType: "hikmet",
                reference: "Deyim — «el-'Amelü hüve sebîlü'n-necâh»",
                title: "Yol — Hedefe Ulaşma Aracı",
                description: "Çalışmak başarıya giden yoldur. Kelime burada mecazî olarak amaca ulaştıran araç ve yöntem anlamındadır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Sucess.jpg/320px-Sucess.jpg", alt: "Başarı sembolü", icon: "fa-trophy" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       SEHÂB  سَحَاب  (S-H-B)
       ────────────────────────────────────────────── */
    sehab: {
        searchKeys: ["sehab", "sahab", "shb", "bulut", "سحاب", "سَحَاب"],
        title: "Sehâb",
        arabic: "سَحَاب",
        root: "Kök: S-H-B",
        plurals: [
            { arabic: "سَحَابَة", transliteration: "Sehâbe (tekil)" }
        ],
        frequency: { percent: 35, label: "Kur'an'da dağlar ve tabiî olaylar bağlamında geçer." },
        collocations: ["Merru's-sehâb", "Sehâbun kesîf"],
        contexts: [
            {
                label: "1. Bulut — Hava Olayı",
                sourceType: "quran",
                reference: "Neml 27:88 — «Ve tere'l-cibâle tahsebuhâ-câmideten ve hiye temurru merre's-sehâb»",
                title: "Bulut — Gökyüzündeki Su Kütlesi",
                description: "Dağlar sanki hareketsiz ama bulut gibi geçer. Bulut, hız ve geçicilik için kıyas unsuru olarak kullanılmıştır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Clouds_over_the_Atlantic_Ocean.jpg/320px-Clouds_over_the_Atlantic_Ocean.jpg", alt: "Okyanus üzerinde bulutlar", icon: "fa-cloud" }
            },
            {
                label: "2. Bulut — Oruç ve Hilal Hadisi",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «Sûmû li-ruʾyetihi... fe-in hâle beynekum ve beynehû sehâbun»",
                title: "Bulutun Hilali Kapaması — Oruç Hükmü",
                description: "Hilali görünce oruç tutun; eğer aranızda bulut engel olursa otuz güne tamamlayın. Fıkıh hükmünü belirleyen hadiste geçer.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Crescent_moon.jpg/320px-Crescent_moon.jpg", alt: "Hilal ay", icon: "fa-moon" }
            },
            {
                label: "3. Bulut — Atasözü",
                sourceType: "hikmet",
                reference: "Mthel — «Hazzun fi's-sehâb, ve 'aklun fi't-turâb»",
                title: "Başı Bulutlarda, Aklı Toprakta",
                description: "Talih göklerde, akıl toprakta. Hırslı ve hayalci kişiyi eleştiren atasözünde bulut yücelik ve erişilmezliği simgeler.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Cumulonimbus_cloud.jpg/320px-Cumulonimbus_cloud.jpg", alt: "Kümülonimbus bulutu", icon: "fa-cloud-bolt" }
            }
        ]
    },

    /* ──────────────────────────────────────────────
       SİKKÎN  سِكِّين  (S-K-N)
       ────────────────────────────────────────────── */
    sikkin: {
        searchKeys: ["sikkin", "skn", "bıçak", "سكين", "سِكِّين"],
        title: "Sikkîn",
        arabic: "سِكِّين",
        root: "Kök: S-K-N",
        plurals: [
            { arabic: "سَكَاكِين", transliteration: "Sekâkîn" }
        ],
        frequency: { percent: 20, label: "Kur'an'da Yusuf Suresi'nde geçer." },
        collocations: ["Sikkînun hadde (keskin bıçak)"],
        contexts: [
            {
                label: "1. Bıçak — Kesme Aleti",
                sourceType: "quran",
                reference: "Yusuf 12:31 — «Ve âtet külle vâhidetin minhünne sikkînen»",
                title: "Bıçak — Kesme veya Biçme Aleti",
                description: "Züleyha kadınlara bıçak verir; Hz. Yusuf'u görünce şaşkınlıkla ellerini keserler. Kur'an'da geçen tek doğrudan bıçak anlatısıdır.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Kitchen_knife.jpg/320px-Kitchen_knife.jpg", alt: "Mutfak bıçağı", icon: "fa-utensils" }
            },
            {
                label: "2. Bıçaksız Kurban — Hadis",
                sourceType: "hadis",
                reference: "Hadis-i Şerif — «Men cu'ile kâdiyen beyne'n-nâsi fekad zubiha bi-gayri sikkîn»",
                title: "Bıçaksız Boğazlamak — Kadılık Tehlikesi",
                description: "İnsanlar arasında hâkim yapılan sanki bıçaksız boğazlanmıştır. Kadılık ve yargı görevinin ağırlığına dikkat çeken hadis.",
                highlight: true,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Old_Court.jpg/320px-Old_Court.jpg", alt: "Eski mahkeme salonu", icon: "fa-gavel" }
            },
            {
                label: "3. Bıçak — Gündelik Kullanım",
                sourceType: "hikmet",
                reference: "Gündelik Arapça — «Taanahu bi-sikkînin fî batnihî»",
                title: "Bıçaklamak — Fiziksel Saldırı",
                description: "Onu karnından bıçakladı. Kelime modern Arapçada da aynı anlamda kullanılmaya devam eder.",
                highlight: false,
                image: { url: "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Kitchen_knife.jpg/320px-Kitchen_knife.jpg", alt: "Bıçak", icon: "fa-utensils" }
            }
        ]
    }

};

/* ================================================================
   OTOMATİK ARAMA EŞLEŞTİRME
   showResult() fonksiyonu içinde kullanılır.
   searchKeys dizisini tarayarak ilgili kelimeyi bulur.
   Yeni kelime eklerken sadece WORDS'e searchKeys ekleyin.
   ================================================================ */
function findWordKey(input) {
    const v = input.trim().toLowerCase();
    for (const [key, word] of Object.entries(WORDS)) {
        if (word.searchKeys.some(k => v.includes(k.toLowerCase()))) {
            return key;
        }
    }
    return null;
}

/* ── Slider state ── */
const CARD_W = 306; // 290px + 16px gap
let sliderPos = 0;
let extraCtxs = [];

function quickSearch(w) { document.getElementById('searchInput').value = w; showResult(); }

function showResult() {
    const v = document.getElementById('searchInput').value.trim().toLowerCase();
    const key = findWordKey(v);
    
    if (!key) { 
        alert('Aradığınız kelime bulunamadı. Lütfen "Kitâb, Beyt, Harb, Nâr, Dâr, vs." gibi mevcut kelimelerden birini deneyin.'); 
        return; 
    }

    const wd = WORDS[key];
    sliderPos = 0;
    extraCtxs = wd.contexts.slice(4);

    document.getElementById('res-title').textContent  = wd.title;
    document.getElementById('res-arabic').textContent = wd.arabic;
    document.getElementById('res-root').textContent   = wd.root;
    document.getElementById('ctx-badge').textContent  = wd.contexts.length + ' bağlam';

    // Çoğullar
    const pw = document.getElementById('res-plurals-wrap');
    const pe = document.getElementById('res-plurals');
    if (wd.plurals?.length) {
        pw.style.display = '';
        pe.innerHTML = wd.plurals.map(p =>
            `<span class="me-3"><span class="arabic-sm">${p.arabic}</span> <small class="text-muted">(${p.transliteration})</small></span>`
        ).join('');
    } else pw.style.display='none';

    document.getElementById('res-freq-bar').style.width = wd.frequency.percent+'%';
    document.getElementById('res-freq-text').textContent = wd.frequency.label;
    document.getElementById('res-collocations').innerHTML =
        wd.collocations.map(c=>`<span class="badge rounded-pill border text-dark me-2 mb-1">${c}</span>`).join('');

    buildGrid(wd.contexts.slice(0,4));

    const ss = document.getElementById('slider-section');
    if (extraCtxs.length) { buildSlider(extraCtxs); ss.style.display=''; }
    else ss.style.display='none';

    document.getElementById('initialMessage').style.display='none';
    document.getElementById('resultArea').style.display='block';
    window.scrollTo({top:420,behavior:'smooth'});
}"""

# Now we need to extract the part to replace.
# The original code goes from "const WORDS = {" to "window.scrollTo({top:420,behavior:'smooth'});\n}"

start_marker = "/* ================================================================\n   KELİME VERİ TABANI"
end_marker = "window.scrollTo({top:420,behavior:'smooth'});\n}"

# We can find where start_marker is, and end_marker, and replace everything in between.
start_idx = content.find(start_marker)
end_idx = content.find(end_marker) + len(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_words_code + content[end_idx:]

with open("index.v3.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Modification complete.")
