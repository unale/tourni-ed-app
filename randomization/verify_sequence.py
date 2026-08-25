#!/usr/bin/env python3
"""
TOURNI-ED (NCT07617103) — tahsis (allocation) dizisi doğrulaması

Tahsis dizisi bu depoda ÜRETİLMEZ. Araştırmacı tarafından dışarıdan sağlanmıştır
ve kaynak kayıt `randomization/allocation_sequence.csv` dosyasıdır.

Bu betik iki şeyi yapar:

1. `index.html` içine gömülü `RAND_LIST` ile CSV'nin birebir aynı olduğunu
   doğrular. Uygulamadaki dizi sessizce değişmiş olamaz.
2. Dizinin istatistiksel özelliklerini raporlar (denge, en büyük kol farkı,
   en uzun aynı-kol serisi, blok yapısı olup olmadığı).

    python3 randomization/verify_sequence.py

Çıkış kodu 0 = tüm kontroller geçti, 1 = en az bir kontrol başarısız.
"""

import csv
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CSV_PATH = os.path.join(HERE, "allocation_sequence.csv")
HTML_PATH = os.path.join(ROOT, "index.html")
EXPECTED_N = 792
ARMS = ("A", "B")


def read_csv():
    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    nos = [int(r["patient_no"]) for r in rows]
    if nos != list(range(1, len(nos) + 1)):
        raise SystemExit("HATA: patient_no 1..n şeklinde ardışık değil")
    return [r["arm"].strip() for r in rows]


def read_embedded():
    src = open(HTML_PATH, encoding="utf-8").read()
    m = re.search(r"const RAND_LIST=(\[.*?\]);", src, re.S)
    if not m:
        raise SystemExit("HATA: index.html içinde RAND_LIST bulunamadı")
    return json.loads(m.group(1))


def block_boundaries(seq):
    """Kümülatif dengenin sıfıra döndüğü noktalar ve aralarındaki mesafeler."""
    bal, bounds = 0, []
    for i, g in enumerate(seq):
        bal += 1 if g == ARMS[0] else -1
        if bal == 0:
            bounds.append(i + 1)
    gaps = [bounds[0]] + [bounds[i] - bounds[i - 1] for i in range(1, len(bounds))]
    return bounds, gaps


def main():
    csv_seq = read_csv()
    html_seq = read_embedded()
    lines, ok = [], True

    def t(label, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        lines.append(f"  [{'OK ' if passed else 'HATA'}] {label}{detail}")

    t("index.html ile CSV birebir aynı", csv_seq == html_seq,
      "" if csv_seq == html_seq else
      f" — {sum(1 for a, b in zip(csv_seq, html_seq) if a != b)} konumda farklı")
    t(f"uzunluk {EXPECTED_N}", len(csv_seq) == EXPECTED_N, f" — {len(csv_seq)}")
    t("yalnızca A/B değerleri", set(csv_seq) <= set(ARMS),
      f" — bulunan: {sorted(set(csv_seq))}")

    na, nb = csv_seq.count("A"), csv_seq.count("B")
    t("kollar eşit", na == nb, f" — A:{na} B:{nb}")

    worst, bal = 0, 0
    for g in csv_seq:
        bal += 1 if g == "A" else -1
        worst = max(worst, abs(bal))
    t("çalışma boyunca kol farkı ≤ 4", worst <= 4, f" — en büyük: {worst}")

    run = longest = 1
    for i in range(1, len(csv_seq)):
        run = run + 1 if csv_seq[i] == csv_seq[i - 1] else 1
        longest = max(longest, run)
    t("en uzun aynı-kol serisi ≤ 8", longest <= 8, f" — {longest}")

    bounds, gaps = block_boundaries(csv_seq)
    t("dizi sonunda denge kapanıyor", bounds and bounds[-1] == len(csv_seq))

    lines.append("")
    lines.append("  Yapı (bilgi amaçlı, geçme/kalma kriteri değil)")
    lines.append(f"    dengenin sıfırlandığı nokta sayısı: {len(bounds)}")
    lines.append(f"    aralık dağılımı: {dict(sorted(Counter(gaps).items()))}")
    fixed4 = all(csv_seq[i:i + 4].count("A") == 2 for i in range(0, len(csv_seq), 4))
    lines.append(f"    sabit 4'lü permüte blok mu: {'evet' if fixed4 else 'HAYIR'}")
    lines.append(f"    ilk 24 tahsis: {' '.join(csv_seq[:24])}")

    print("TOURNI-ED tahsis dizisi doğrulaması")
    print(f"kaynak: randomization/allocation_sequence.csv")
    print("\n".join(lines))
    print("\n" + ("TÜM KONTROLLER GEÇTİ" if ok else "KONTROL BAŞARISIZ"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
