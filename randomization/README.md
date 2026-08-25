# TOURNI-ED — Randomizasyon Belgesi

**Çalışma:** NCT07617103 · Etik kurul: 09.2026.829
**Belge tarihi:** 25.08.2026
**Durum:** Hasta alımı başlamadan önce yerleştirilmiştir. Kayıtlı hasta yoktur.

---

## 1. Kaynak

Tahsis dizisi **bu depoda üretilmemiştir.** Araştırmacı tarafından dışarıdan
sağlanmış, `TOURNIED_analysis_dataset_n792.xlsx` dosyasının `arm` sütunundan
`patient_id` sırasına göre çıkarılmıştır.

Kaynak kayıt: **`randomization/allocation_sequence.csv`** (792 satır,
`patient_no, arm`). Uygulamadaki `RAND_LIST` bu dosyadan türetilmiştir ve
`verify_sequence.py` ikisinin aynı kaldığını denetler.

> ### ⚠️ Tamamlanması gereken alanlar
>
> Aşağıdakiler araştırmacı tarafından doldurulmalıdır; CONSORT madde 8'in
> (rastgele sıranın nasıl üretildiği) karşılığıdır ve şu an belgelenmemiştir.
>
> - **Üreten kişi / yazılım:** _(ör. R 4.4.1 `blockrand`, SAS PROC PLAN, randomization.com, bağımsız biyoistatistikçi)_
> - **Yöntem adı:** _(aşağıdaki §3'te gözlenen yapıya bakınız)_
> - **Seed / üretim parametreleri:** _(kaydedilmediyse bunu yazın)_
> - **Üretim tarihi:**
> - **Diziyi üreten kişi hasta alımında görev alıyor mu:** _(evet/hayır)_

## 2. Tanımlar

| Kol | Uygulama |
|---|---|
| **A — Erken bırakma** | Sodyum sitrat tüpü (mavi kapak) dolunca sfingomanometre bırakılır |
| **B — Geç bırakma** | Son tüp K₂EDTA (mor kapak) dolana kadar sfingomanometre 60 mmHg'de tutulur |

Tahsis oranı 1:1. Toplam 792 tahsis — **396 A / 396 B**.

## 3. Gözlenen yapı

Aşağıdakiler dizinin kendisinden ölçülmüştür; beyan edilen yönteme değil,
gerçekte gözlenene dayanır.

| Ölçüm | Değer |
|---|---|
| Uzunluk | 792 |
| Denge | 396 A / 396 B (tam) |
| Çalışma boyunca en büyük anlık kol farkı | **4** |
| En uzun aynı-kol serisi | **4** |
| Sabit 4'lü permüte blok mu | **Hayır** |
| Dengenin sıfırlandığı nokta sayısı | 158 |
| Bu noktalar arası mesafe | 2–42 arasında değişiyor (dağılım: 2×86, 4×34, 6×14, 8×5, kalanı 10–42) |

**Yorum.** Dizi permüte blok randomizasyonu **değildir**. Permüte blokta
kümülatif denge her blok sonunda sıfıra döner, dolayısıyla sıfırlanma
aralıkları blok boylarına eşit olurdu; burada 42'ye kadar çıkan aralıklar var.

Buna karşılık kol farkı çalışma boyunca hiç 4'ü geçmiyor. Bloksuz (basit)
randomizasyonda 792 kişide beklenen tipik fark ~28'dir. Yani dizi, azami
dengesizliği 4 ile sınırlayan **kısıtlı bir randomizasyon** ile üretilmiş
görünüyor (biased-coin / big-stick / maksimal prosedür ailesi).

Bu, tahsis gizlenmesi açısından sabit bloktan **daha iyidir**: sabit 4'lü
blokta bir bloğun ilk üç tahsisi bilindiğinde dördüncüsü kesindir; burada
öyle bir determinist nokta yoktur. Yayında yöntemin adı doğru verilmelidir —
"blok randomizasyonu" demek bu dizi için yanlış olur.

## 4. Doğrulama

```bash
python3 randomization/verify_sequence.py
```

Son çalıştırma:

```
[OK] index.html ile CSV birebir aynı
[OK] uzunluk 792
[OK] yalnızca A/B değerleri
[OK] kollar eşit — A:396 B:396
[OK] çalışma boyunca kol farkı ≤ 4 — en büyük: 4
[OK] en uzun aynı-kol serisi ≤ 8 — 4
[OK] dizi sonunda denge kapanıyor
```

## 5. Uygulama

Dizi `index.html` içinde `RAND_LIST` sabiti olarak tutulur:

```js
assignGroup(n) === RAND_LIST[n - 1]
```

Sıra numarası yalnızca gerçek hastalar için artar; "deneme kaydı" işaretli
kayıtlar sıra tüketmez. 792 tahsis tükendiğinde uygulama kaydetmeyi durdurur ve
görünür uyarı verir — grupsuz hasta kaydı oluşmaz.

## 6. Sınırlılık: tahsis gizlenmesi (allocation concealment)

**Bu dizi gizli değildir.** Uygulama sunucusuz, tek dosyalık bir istemci
uygulaması olduğu için `RAND_LIST` kullanıcının tarayıcısına iner ve "kaynağı
görüntüle" ile okunabilir. Şifreleme çözüm değildir; anahtarın da aynı dosyada
olması gerekirdi.

Ayrıca uygulama, hasta kaydedilmeden önce sıradaki tahsisi ekranda gösterir.
Yani hastayı çalışmaya alma kararı verilmeden önce hangi kola düşeceği bilinebilir.

**Sonuç:** Bu haliyle çalışma, CONSORT madde 9 (tahsis gizleme mekanizması)
anlamında gizlenmiş tahsis sağlamaz ve seçim yanlılığına açıktır. Yayında
sınırlılık olarak bildirilmelidir.

**Tam çözüm için gereken:** Tahsisin sunucu tarafında tutulup hasta kaydı
oluşturulduğunda tek tek verilmesi, ve her tahsisin geri alınamaz biçimde
tüketilip zaman damgasıyla loglanması.

## 7. Değişiklik geçmişi

| Tarih | Değişiklik |
|---|---|
| — | İlk sürüm: 800 tahsis, sabit 4'lü permüte blok, üretim yöntemi belgelenmemiş |
| 25.08.2026 | Araştırmacının sağladığı dizi ile değiştirildi: 792 tahsis, 396A/396B, kısıtlı randomizasyon (azami dengesizlik 4). Hasta alımı başlamadan önce yapılmıştır — kayıtlı hasta etkilenmemiştir. |

**Not.** Yeni dizinin ilk 80 tahsisi eski (800'lük) listeyle birebir aynıdır,
81. hastadan itibaren ayrışır. Bunun nedeni belgelenmelidir — muhtemelen yeni
dizi üretilirken eski listenin bir bölümü devralınmıştır. Metodolojik bir sorun
teşkil etmez, ancak açıklanmadığında hakem sorusu doğurabilir.
