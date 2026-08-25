#!/usr/bin/env python3
"""
TOURNI-ED (NCT07617103) — tahsis (allocation) sırası üreteci

YÖNTEM
------
Permüte blok randomizasyonu, 1:1, değişken blok boyu.

- Blok boyları {4, 6, 8} kümesinden eşit olasılıkla çekilir.
- Her blok tam dengelidir (2A/2B, 3A/3B, 4A/4B), blok içi sıra karıştırılır.
- Toplam uzunluk hedef örneklem büyüklüğüne (792) tam eşitlenir; blok boyu
  seçimi, geriye 2 kişilik (hiçbir blok boyuna bölünemeyen) artık kalmayacak
  şekilde kısıtlanır.
- Sonuç: 396 A / 396 B, ve her blok sınırında kollar dengede.

Değişken blok boyu, sabit blok boyuna (eski liste 4'lüktü) göre blok sonu
tahminini zorlaştırır: sabit 4'lük blokta bir bloğun ilk 3 tahsisi bilindiğinde
4.'sü kesindir; değişken blokta blok sınırının nerede olduğu da bilinmez.

YENİDEN ÜRETİLEBİLİRLİK
-----------------------
PRNG: Python `random.Random` (Mersenne Twister, MT19937).
SEED: 20260825
Betiği çalıştıran herkes birebir aynı diziyi elde eder — üretilen sıranın
sonradan seçilmediği (post hoc değiştirilmediği) böyle doğrulanabilir.

    python3 randomization/generate_sequence.py --check

KULLANIM
--------
    python3 randomization/generate_sequence.py            # JS dizisini yazdır
    python3 randomization/generate_sequence.py --check    # doğrulama raporu

UYARI
-----
Bu dizi istemci tarafındaki index.html içine gömülüdür, dolayısıyla açık
metindir ve gizli değildir. Gerçek anlamda gizlenmiş tahsis (allocation
concealment) için tahsisin sunucu tarafında tutulup hasta kaydedildiğinde
tek tek verilmesi gerekir. Ayrıntı için randomization/README.md.
"""

import argparse
import json
import random

SEED = 20260825
TARGET_N = 792
BLOCK_SIZES = (4, 6, 8)
ARMS = ("A", "B")


def generate(seed=SEED, n=TARGET_N, block_sizes=BLOCK_SIZES):
    """Permüte blok randomizasyonu ile n uzunluğunda tahsis dizisi üretir."""
    rng = random.Random(seed)
    seq, blocks, remaining = [], [], n

    while remaining > 0:
        # Geriye hiçbir blok boyuna bölünemeyen artık (ör. 2) bırakma
        allowed = [
            s for s in block_sizes
            if s <= remaining and (remaining - s == 0 or remaining - s >= min(block_sizes))
        ]
        if not allowed:
            raise RuntimeError(f"kalan {remaining} için uygun blok boyu yok")
        size = rng.choice(allowed)
        block = [ARMS[0]] * (size // 2) + [ARMS[1]] * (size // 2)
        rng.shuffle(block)
        seq.extend(block)
        blocks.append(size)
        remaining -= size

    return seq, blocks


def check(seq, blocks):
    """Diziyi doğrula; (rapor_satırları, hepsi_geçti) döndürür."""
    lines, ok = [], True

    def t(label, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        lines.append(f"  [{'OK ' if passed else 'HATA'}] {label}{detail}")

    t("uzunluk 792", len(seq) == TARGET_N, f" — {len(seq)}")
    t("396 A / 396 B", seq.count("A") == 396 and seq.count("B") == 396,
      f" — A:{seq.count('A')} B:{seq.count('B')}")
    t("blok boyları toplamı = 792", sum(blocks) == TARGET_N, f" — {sum(blocks)}")
    t("blok boyları {4,6,8}", set(blocks) <= set(BLOCK_SIZES),
      f" — kullanılan: {sorted(set(blocks))}")

    # Her blok kendi içinde dengeli mi
    i, balanced = 0, True
    for size in blocks:
        if seq[i:i + size].count("A") != size // 2:
            balanced = False
        i += size
    t("her blok içinde 1:1 denge", balanced)

    # Her blok sınırında kümülatif denge
    i, drift_ok, worst = 0, True, 0
    for size in blocks:
        i += size
        drift = abs(seq[:i].count("A") - seq[:i].count("B"))
        worst = max(worst, drift)
        if drift != 0:
            drift_ok = False
    t("blok sınırlarında kümülatif fark 0", drift_ok, f" — en kötü: {worst}")

    # Çalışma boyunca kollar arası fark
    max_imb = max(abs(seq[:i].count("A") - seq[:i].count("B"))
                  for i in range(1, len(seq) + 1))
    t("anlık en büyük kol farkı ≤ 4", max_imb <= 4, f" — {max_imb}")

    # En uzun aynı-kol serisi
    run = longest = 1
    for j in range(1, len(seq)):
        run = run + 1 if seq[j] == seq[j - 1] else 1
        longest = max(longest, run)
    t("en uzun aynı-kol serisi ≤ 8", longest <= 8, f" — {longest}")

    lines.append("")
    lines.append(f"  blok sayısı: {len(blocks)}")
    lines.append(f"  blok boyu dağılımı: " +
                 ", ".join(f"{s}'lik: {blocks.count(s)}" for s in BLOCK_SIZES))
    lines.append(f"  ilk 24 tahsis: {' '.join(seq[:24])}")
    return lines, ok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="doğrulama raporu yazdır")
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    seq, blocks = generate(seed=args.seed)

    if args.check:
        print(f"TOURNI-ED tahsis dizisi — seed={args.seed}")
        lines, ok = check(seq, blocks)
        print("\n".join(lines))
        print("\n" + ("TÜM KONTROLLER GEÇTİ" if ok else "KONTROL BAŞARISIZ"))
        raise SystemExit(0 if ok else 1)

    print("const RAND_LIST=" + json.dumps(seq, separators=(",", ":")) + ";")


if __name__ == "__main__":
    main()
