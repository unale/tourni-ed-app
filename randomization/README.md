# TOURNI-ED — Randomizasyon Belgesi

**Çalışma:** NCT07617103 · Etik kurul: 09.2026.829
**Belge tarihi:** 25.08.2026
**Durum:** Hasta alımı başlamadan önce üretilmiştir.

---

## 1. Yöntem

Permüte blok randomizasyonu, **1:1**, **değişken blok boyu**.

| | |
|---|---|
| Tahsis oranı | 1:1 (Grup A : Grup B) |
| Blok boyları | 4, 6, 8 — her blok için eşit olasılıkla çekilir |
| Blok içi denge | Her blok tam dengeli (2A/2B, 3A/3B, 4A/4B) |
| Toplam | 792 tahsis — **396 A / 396 B** |
| Blok sayısı | 126 (33 adet 4'lük, 42 adet 6'lık, 51 adet 8'lik) |

**Gruplar**

- **A — Erken bırakma:** sodyum sitrat tüpü (mavi kapak) dolunca sfingomanometre bırakılır
- **B — Geç bırakma:** son tüp K₂EDTA (mor kapak) dolana kadar sfingomanometre 60 mmHg'de tutulur

## 2. Üretim ve yeniden üretilebilirlik

Dizi `generate_sequence.py` ile üretilmiştir.

| | |
|---|---|
| PRNG | Python `random.Random` — Mersenne Twister (MT19937) |
| Seed | `20260825` |
| Betik | `randomization/generate_sequence.py` |

Betik depoda saklanır. Diziyi yeniden üretmek ve doğrulamak için:

```bash
python3 randomization/generate_sequence.py --check
```

Aynı seed her zaman birebir aynı diziyi verir. Bu, tahsis sırasının sonradan
seçilmediğini (post hoc değiştirilmediğini) bağımsız olarak doğrulanabilir kılar.

## 3. Doğrulama sonuçları

```
[OK] uzunluk 792
[OK] 396 A / 396 B
[OK] blok boyları toplamı = 792
[OK] blok boyları {4,6,8}
[OK] her blok içinde 1:1 denge
[OK] blok sınırlarında kümülatif fark 0
[OK] anlık en büyük kol farkı ≤ 4  (gözlenen: 4)
[OK] en uzun aynı-kol serisi ≤ 8   (gözlenen: 6)
```

Çalışmanın hiçbir anında kollar arası fark 4 hastayı geçmez; erken durdurma veya
ara analiz yapılsa bile kollar dengeli kalır.

## 4. Uygulama

Dizi `index.html` içinde `RAND_LIST` sabiti olarak tutulur. Tahsis, hasta sıra
numarasına göre belirlenir:

```js
assignGroup(n) === RAND_LIST[n - 1]
```

Sıra numarası yalnızca gerçek hastalar için artar; "deneme kaydı" işaretli
kayıtlar sıra tüketmez. 792 tahsis tükendiğinde uygulama kaydetmeyi durdurur ve
görünür uyarı verir — grupsuz hasta kaydı oluşmaz.

## 5. Sınırlılık: tahsis gizlenmesi (allocation concealment)

**Bu dizi gizli değildir.** Uygulama sunucusuz, tek dosyalık bir istemci
uygulaması olduğu için `RAND_LIST` kullanıcının tarayıcısına iner ve "kaynağı
görüntüle" ile okunabilir. Şifreleme çözüm değildir; anahtarın da aynı dosyada
olması gerekirdi.

Ayrıca uygulama, hasta kaydedilmeden önce sıradaki tahsisi ekranda gösterir.
Yani hastayı çalışmaya alma kararı verilmeden önce hangi kola düşeceği bilinebilir.

**Sonuç:** Bu haliyle çalışma, CONSORT madde 9 (tahsis gizleme mekanizması)
anlamında gizlenmiş tahsis sağlamaz ve seçim yanlılığına açıktır. Yayında
sınırlılık olarak bildirilmelidir.

**Kısmi azaltma (uygulanmıştır):** Değişken blok boyu, sabit 4'lük bloğa göre
tahmini zorlaştırır. Sabit 4'lük blokta bir bloğun ilk üç tahsisi bilindiğinde
dördüncüsü kesindir; değişken blokta blok sınırının nerede olduğu da bilinmez.
Bu, listeye hiç bakılmadığı senaryoda anlamlıdır — listeye bakıldığında koruma
sağlamaz.

**Tam çözüm için gereken:** Tahsisin sunucu tarafında tutulup hasta kaydı
oluşturulduğunda tek tek verilmesi, ve her tahsisin geri alınamaz biçimde
tüketilip zaman damgasıyla loglanması.

## 6. Değişiklik geçmişi

| Tarih | Değişiklik |
|---|---|
| 25.08.2026 | İlk sürüm: 800 tahsis, sabit 4'lük blok, üretim yöntemi belgelenmemiş |
| 25.08.2026 | Mevcut sürüm: 792 tahsis, değişken blok (4/6/8), seed'li ve betikle yeniden üretilebilir. Hasta alımı başlamadan önce değiştirilmiştir — kayıtlı hasta etkilenmemiştir. |
