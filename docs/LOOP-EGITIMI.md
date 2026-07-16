# LOOP EĞİTİMİ — Acil Tıp Araştırmacısı İçin Kişisel Rehber

> Bu rehber, TOURNI-ED çalışmasının sahibi, doçentlik yolundaki bir acil tıp
> uzmanı için hazırlandı. Amaç: loop (kendi kendine dönen agent döngüsü)
> mantığını hem uygulama geliştirmede hem de **akademik üretimde** (GAP bulma,
> çalışma dizaynı, makale yazımı) kullanılır hale getirmek.

---

## 0. Zihinsel model: Loop aslında zaten bildiğin bir şey

Acilde her gün loop çalıştırıyorsun:

| Acil tıp | Loop |
|---|---|
| Hasta hedefi ("hemodinamik stabilizasyon") | HEDEF |
| Müdahale (sıvı, ilaç, işlem) | Adımı uygula |
| Yeniden değerlendirme (vital, laktat, idrar çıkışı) | Sonuca bak |
| Yanıt yoksa planı değiştir | Hatayı düzelt |
| Taburculuk / yatış kriteri | BİTTİ ŞARTI |
| "3 kez denedim, olmadı → konsültasyon" | GÜVENLİK FRENİ (maks. tur) |

Loop kurmak = **taburculuk kriteri yazmak.** "Hasta iyi görünene kadar"
demezsin; "laktat < 2, MAP > 65, GKS 15" dersin. Aynı disiplini modele
uygularsın. Bitti şartın ne kadar ölçülebilirse, loop o kadar isabetli döner.

Her loop'un iskeleti 4 satır:

1. **Tetikleyici** — işi ne başlatıyor?
2. **Adımlar** — hangi adımlardan geçiyor?
3. **Bitti şartı** — tamamlandığını neyden anlayacaksın? (sayı/madde, his değil)
4. **Hata durumu** — ters giderse ne olacak? (maks. tur + durunca ne raporlayacak)

---

## 1. Seviye 1 — İşlevsel loop: kendi uygulamanda dene (bu akşamki egzersiz)

En hızlı öğrenme yolu, loop'u zaten sahibi olduğun bir şey üzerinde
çalıştırmak. TOURNI-ED tek dosyalık bir uygulama; ideal deney alanı.

Claude Code'u `tourni-ed-app` klasöründe aç ve şunu yapıştır:

```
HEDEF: TOURNI-ED uygulamasındaki (index.html) veri bütünlüğünü doğrula ve
bulduğun hataları düzelt.

ÇALIŞMA ŞEKLİN (loop): Uygulamayı yerel sunucuda aç (npx serve veya
python3 -m http.server), aşağıdaki kontrol listesini tek tek dene.
Geçmeyen ilk maddeyi bul, sebebini bir cümleyle söyle, düzelt, tekrar dene.
Her turda bana "kaç/6 madde geçti" yaz.

BİTTİ KONTROL LİSTESİ (6 madde, hepsi geçmeli):
1. Sayfa konsolda hata olmadan açılıyor.
2. A-DIVA skoru 5 sorunun toplamını her kombinasyonda doğru hesaplıyor.
3. Kronometre başlat/durdur, turnike_suresi alanına saniyeyi doğru yazıyor.
4. Zorunlu alanlar boşken kayıt engelleniyor ve kullanıcı uyarılıyor.
5. 3 sahte hasta kaydı gir → CSV export'taki satır sayısı ve kolonlar
   girilen verilerle birebir eşleşiyor (özellikle Türkçe karakterler).
6. Sayfa yenilenince (localStorage) kayıtlar kaybolmuyor.

GÜVENLİK FRENİ: En fazla 10 tur. 10'a gelince dur, geçen/kalan maddeleri
tablo halinde raporla. Bir maddeyi düzeltirken diğer maddeleri bozup
bozmadığını her turda yeniden kontrol et (regresyon).

Ben araya girmeden bu döngüyü kendin yürüt. Takıldığında durup net soru sor.
```

**Buradan öğreneceğin ders:** 5. madde gibi "birebir eşleşiyor" tarzı
doğrulanabilir maddeler loop'u keskinleştirir; "export düzgün çalışıyor"
yazsaydın model kendi kendini erken aklardı.

---

## 2. Seviye 2 — Kendi kendini puanlayan loop

İşlevsel kontrol "çalışıyor/çalışmıyor" der. Puanlamalı loop ise kaliteyi
objektif bir eşiğe kadar iyileştirir. Kural: **asla "beğenene kadar" deme;
her zaman sayı + maksimum tur ver.**

- Zayıf: "Makale özeti güzel olana kadar iyileştir."
- Güçlü: "Aşağıdaki 5 kritere 1–10 puan ver; ortalama ≥ 9 VE hiçbir kriter
  < 8 olana kadar en düşük kriteri düzelt. Maks. 8 tur."

Puanlama loop'unun püf noktası: kriterlerin **kontrol edilebilir** olması.
"Akıcı mı" kötü kriterdir; "her paragrafta tek ana fikir var mı",
"pasif cümle oranı %20'nin altında mı", "abstract kelime sayısı ≤ 250 mi"
iyi kriterdir — model bunları gerçekten sayabilir.

---

## 3. Seviye 3 — Akademik loop kütüphanesi (asıl imza atacağın yer)

### 3a. GAP Avcısı loop'u

Amacın: bir konuda literatürdeki boşluğu sistematik biçimde bulmak.

```
HEDEF: "[KONU — örn. antekübital kan alımında turnike süresi ve psödohiperkalemi]"
konusunda yayınlanabilir, özgün en az 3 araştırma boşluğu (GAP) tespit et.

ÇALIŞMA ŞEKLİN (loop):
1. PubMed'de sistematik ara (son 10 yıl + landmark eski çalışmalar).
   Her turda farklı bir arama stratejisi dene: MeSH terimleri, sinonimler,
   ilişkili sonuçlar (related articles).
2. Bulduğun her derleme/meta-analizin "limitations" ve "future research"
   bölümlerini oku — GAP'lerin yarısı orada açıkça yazar.
3. Her GAP adayı için şu 4 soruyu puanla (1-10):
   a) Gerçekten boş mu? (Aksini gösteren çalışma bulamadın mı — en az 3
      farklı arama stratejisiyle doğrula)
   b) Acil serviste pratik olarak çalışılabilir mi? (hasta akışı, etik,
      maliyet)
   c) Klinik önemi var mı? (sonuç bir kılavuzu/pratiği değiştirir mi)
   d) Tek merkez, makul sürede, makul örneklemle yapılabilir mi?
4. 4 sorudan herhangi biri < 6 puansa GAP'i ele, aramaya devam et.

BİTTİ ŞARTI: 4 kriterin hepsinden ≥ 6 alan 3 GAP bulundu. Her biri için:
tek cümlelik araştırma sorusu (PICO formatında) + "neden hâlâ yapılmamış"
hipotezi + en yakın 3 mevcut çalışmanın künyesi.

GÜVENLİK FRENİ: Maks. 12 arama turu. Dolarsa elindeki en iyi adayları
puan tablosuyla sun.
```

### 3b. "Literatürde ilk mi?" doğrulama loop'u

"İlk çalışma" iddiası hakemlerin en acımasız test ettiği cümledir.
Bunu bir **çürütme loop'u** olarak kur — model desteklemeye değil,
**yıkmaya** çalışsın:

```
HEDEF: "[ÇALIŞMA FİKRİM]" için "literatürde ilk" iddiamı ÇÜRÜTMEYE çalış.

ÇALIŞMA ŞEKLİN (loop): Her turda farklı bir açıdan benzer çalışma ara:
1. Aynı soru, farklı popülasyon (pediatri, yoğun bakım, prehospital...)
2. Aynı soru, farklı terminoloji (eski/alternatif terimler, İngilizce dışı
   literatür, tez veritabanları)
3. Aynı yöntem, komşu alanlarda (anestezi, hemşirelik, laboratuvar tıbbı)
4. Kongre bildirileri ve preprint'ler (medRxiv)
5. Kayıtlı ama yayınlanmamış protokoller (ClinicalTrials.gov)

BİTTİ ŞARTI: (a) İddiayı çürüten bir çalışma bulundu → künyesi + benim
çalışmamı ondan nasıl farklılaştırabileceğime dair 2 öneri, VEYA
(b) 5 açının hepsi tarandı ve hiçbir şey çıkmadı → "ilk" iddiasını
makalede nasıl güvenli ifade edeceğime dair cümle önerisi
("to our knowledge, ... in the ED setting" gibi sınırlı iddia).

GÜVENLİK FRENİ: Maks. 10 tur.
```

Bu loop'un mantığı sana tanıdık gelmeli: **ayırıcı tanı dışlama** gibi.
Tanıyı (özgünlüğü) koymak için önce alternatifleri agresifçe dışlarsın.

### 3c. Çalışma dizaynı loop'u (kendi kendine hakem paneli)

```
HEDEF: "[ARAŞTIRMA SORUM — PICO]" için etik kurula sunulabilir olgunlukta
bir çalışma protokolü taslağı üret.

ÇALIŞMA ŞEKLİN (loop):
1. Protokol taslağını yaz (dizayn, popülasyon, örneklem hesabı, birincil/
   ikincil sonlanımlar, istatistik planı, akış şeması).
2. Taslağı 3 ayrı hakem gözüyle acımasızca değerlendir ve her birinden
   1-10 puan ver:
   - Metodolog: bias kaynakları, karıştırıcılar, güç analizi doğru mu?
   - Acil tıp klinisyeni: acil serviste GERÇEKTEN uygulanabilir mi?
     (triaj akışını bozuyor mu, hemşire iş yükü, gece vardiyası)
   - Dergi hakemi: STROBE/CONSORT'un ilgili maddeleri karşılanıyor mu,
     "so what?" sorusuna net cevap var mı?
3. En düşük puanı veren hakemin en sert 2 eleştirisini düzelt, yeniden puanla.

BİTTİ ŞARTI: Üç hakem de ≥ 8 puan veriyor VE örneklem hesabı sayısal
olarak açık (etki büyüklüğü, alfa, güç, n).

GÜVENLİK FRENİ: Maks. 6 tur. Dolarsa kalan zayıflıkları "bilinen
limitasyonlar" listesi olarak ver — bunlar makalendeki Limitations
bölümünün ilk taslağıdır.
```

### 3d. Makale revizyonu loop'u (hakem yanıtı)

```
HEDEF: Ekteki hakem eleştirilerinin TAMAMINA nokta atışı yanıt + makalede
karşılık gelen değişiklik üret.

ÇALIŞMA ŞEKLİN (loop): Her eleştiri için: (1) eleştiriyi tek cümleyle
yeniden ifade et, (2) katılıyor muyuz karar ver, (3) yanıt + metin
değişikliği yaz, (4) kontrol: yanıt eleştirinin HER alt maddesini
karşılıyor mu, yapılan değişiklik makalenin başka yerinde çelişki
yaratıyor mu?

BİTTİ ŞARTI: Tüm eleştiriler "yanıtlandı + metin değişikliği işaretlendi +
çelişki taraması temiz" durumunda.

GÜVENLİK FRENİ: Kararsız kaldığın eleştirilerde (yöntemi değiştirmemi
isteyen, ek analiz talep eden) DUR ve bana sor — bunlar benim kararım.
```

---

## 4. Bitti şartı yazma sanatı — hızlı referans

| Zayıf (öznel) | Güçlü (ölçülebilir) |
|---|---|
| "İyi bir literatür taraması yap" | "3 farklı stratejide yeni sonuç çıkmayana kadar ara (doygunluk)" |
| "Uygulama düzgün çalışsın" | "6 maddelik kontrol listesi, hepsi geçmeli" |
| "Özet güçlü olsun" | "5 kriter × 1-10, ortalama ≥ 9, hiçbiri < 8" |
| "GAP bul" | "4 fizibilite kriterinin hepsinden ≥ 6 alan 3 GAP" |
| "Beğenene kadar" | ASLA. Her zaman sayı + maks. tur. |

Ek kurallar:

- **Doygunluk kriteri** araştırma loop'ları için altın standarttır:
  "K tur üst üste yeni bir şey çıkmazsa dur" (sistematik derlemedeki
  arama doygunluğunun aynısı).
- **Regresyon kontrolü** işlevsel loop'larda şart: "düzelttiğin madde
  geçerken önceki maddeleri de yeniden test et."
- **Çürütme çerçevesi** doğrulama loop'larında şart: modele "destekle"
  değil "yıkmaya çalış" de; hayatta kalan iddia güçlü iddiadır.

## 5. Loop sapıttığında müdahale cümleleri

- "Hedeften saptın, sadece şu tek işe odaklan."
- "Her adımın sonucunu bana göster, sonra devam et."
- "Bu hedef çok büyük, önce en küçük çalışan parçayı bitir."
- "Hata mesajını / makale künyesini olduğu gibi oku, tahmin etme."
- (Araştırma loop'larında en kritiği:) "Bu kaynağı gerçekten buldun mu,
  yoksa hafızandan mı yazdın? DOI/PMID ver, doğrula."

Son madde hayati: **literatür loop'larında her künyeyi doğrulat.**
Bitti şartına her zaman "tüm atıflar PMID/DOI ile doğrulanmış" maddesini ekle.

---

## 6. 4 haftalık pratik program

**Hafta 1 — İşlevsel loop:** Bölüm 1'deki TOURNI-ED loop'unu çalıştır.
Amaç mekaniği hissetmek: tur, kontrol listesi, fren.

**Hafta 2 — Puanlamalı loop:** Yazmakta olduğun bir abstract'ı/bölümü al,
5 objektif kriterli puanlama loop'u kur (Bölüm 2). Kriterleri kendin yaz —
asıl egzersiz kriter yazmak, metin iyileştirmek değil.

**Hafta 3 — GAP avcısı:** Aklındaki çalışma fikirlerinden BİRİNİ seç,
3a + 3b loop'larını sırayla çalıştır. Çıktı: PICO formatında, "ilk"lik
durumu doğrulanmış bir araştırma sorusu.

**Hafta 4 — Dizayn:** Hafta 3'ün çıktısını 3c hakem paneli loop'una sok.
Çıktı: etik kurul başvurusunun iskeleti.

Ay sonunda elinde: loop kurma refleksi + doğrulanmış bir çalışma fikri +
protokol taslağı. Bu döngünün kendisi de bir loop: her yeni fikirde
Hafta 3→4'ü tekrar çalıştırırsın.

---

## 7. Altın kurallar (özet)

1. Bitti şartı = taburculuk kriteri. Sayı ve madde, his değil.
2. Her loop'a güvenlik freni (maks. tur) koy.
3. Araştırma loop'larında çürütme çerçevesi + künye doğrulama zorunlu.
4. Kararın sana ait olduğu yerlerde (etik, yöntem değişikliği) loop'a
   "dur ve bana sor" talimatı ver.
5. Loop'un kalitesi = kontrol listesinin kalitesi. Vaktin çoğunu prompt'a
   değil, kontrol listesine harca.

---

## 8. Doğrulanmış kaynaklar (birincil literatür)

Loop/agent yaklaşımını tanımlayan ekip Anthropic'tir; aşağıdakiler resmî
birincil kaynaklardır. İnternetteki içeriklerin çoğu bunların sulandırılmış
anlatımıdır — şüpheye düştüğünde buraya dön.

Okuma sırasıyla:

1. **Building Effective Agents** — kurucu metin; "agent = döngüde araç
   kullanan model" tanımı ve evaluator-optimizer (kendi kendini puanlayan
   loop) deseni buradan.
   https://www.anthropic.com/engineering/building-effective-agents
2. **Claude Code: Best Practices for Agentic Coding** — loop'u Claude
   Code'da pratikte kurma rehberi (TDD döngüsü, ekran görüntüsüyle
   iyileştirme döngüsü).
   https://www.anthropic.com/engineering/claude-code-best-practices
3. **Claude Code resmî dokümantasyonu — Best Practices** — güncel tutulan
   referans; araç değiştikçe burası güncellenir.
   https://code.claude.com/docs/en/best-practices
4. **Effective Harnesses for Long-Running Agents** — ileri seviye: uzun
   süre kendi başına çalışan loop'lar nasıl raydan çıkmaz ("güvenlik
   freni"nin derinlemesine hali).
   https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Bilgi kirliliği filtresi (4 soru): (1) Birincil kaynakta karşılığı var mı?
(2) İçerik 6-12 aydan eski mi? (3) Gerçek tur/hata/düzeltme çıktısı
gösteriyor mu, sadece sonucu mu? (4) "Sihirli prompt" mu vaat ediyor?
— Sonuncusu her zaman kırmızı bayraktır: asıl beceri prompt değil,
kontrol listesi yazmaktır.
