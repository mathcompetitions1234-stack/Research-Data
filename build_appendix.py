#!/usr/bin/env python3
"""Build the four-column cutoff appendix from the enumerated chart.

Reads ../cutoff_table.tsv. Replaces the three p=8 entries recorded there as
"c > 12" with the exact cutoff 13 from the later complete count. Adds the four
p=8 shapes that are not in that chart; their cutoffs are the lower bounds from
cutoffs.txt.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CHART = ROOT.parent / "cutoff_table.tsv"
OUT_CSV = ROOT / "cutoffs.csv"
OUT_TABLE = ROOT / "cutoff_table.tex"
OUT_DOC = ROOT / "cutoff_appendix.tex"

# Exact values established after cutoff_table.tsv was written.
EXACT_OVERRIDE = {
    (8, "hubs 4–3, adjacent, arms (2,1,1) | (1,1)"): 13,
    (8, "spider, legs 2, 2, 2, 1"): 13,
    (8, "hubs 3–3, adjacent, arms (2,2) | (1,1)"): 13,
}

# Shapes absent from the chart. Bounds are those stated in cutoffs.txt.
LOWER_BOUNDS = [
    (8, "spider, legs 3, 3, 1", 6, 12),
    (8, "spider, legs 5, 1, 1", 6, 14),
    (8, "spider, legs 4, 2, 1", 6, 14),
    (8, "path", 7, 14),
]

HUB_RE = re.compile(
    r"hubs (\d+)[\-\u2013](\d+), (adjacent|distance \d+), arms (.+)$"
)
SPIDER_RE = re.compile(r"spider, legs (.+)$")


def shape_plain_and_tex(raw: str) -> tuple[str, str]:
    raw = raw.strip()
    if raw in ("star", "path"):
        return raw, raw

    spider = SPIDER_RE.match(raw)
    if spider:
        legs = ",".join(part.strip() for part in spider.group(1).split(","))
        plain = f"spider with legs ({legs})"
        return plain, f"spider with legs $({legs})$"

    hub = HUB_RE.match(raw)
    if hub:
        left_deg, right_deg, where, arms = hub.groups()
        if where == "adjacent":
            distance = "1"
        else:
            distance = where.split()[1]
        left_arm, right_arm = (part.strip() for part in arms.split("|"))
        plain = (
            f"hubs of degrees {left_deg} and {right_deg}, "
            f"distance {distance}, arms {left_arm} and {right_arm}"
        )
        tex = (
            f"hubs of degrees ${left_deg}$ and ${right_deg}$, "
            f"distance ${distance}$, arms ${left_arm}$ and ${right_arm}$"
        )
        return plain, tex

    if raw == "three degree-3 vertices, distances 1, 1, 2":
        plain = "three vertices of degree 3, distances 1, 1, 2"
        tex = r"three vertices of degree $3$, distances $1$, $1$, $2$"
        return plain, tex

    raise SystemExit(f"unrecognized shape: {raw}")


def load_rows() -> list[dict]:
    rows = []
    for line in CHART.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#") or line.startswith("canon"):
            continue
        shape_raw, p_text, cutoff_text, _leaves, diameter_text = line.split("\t")[1:6]
        p = int(p_text)
        diameter = int(diameter_text)
        if cutoff_text == "c > 12":
            cutoff = EXACT_OVERRIDE[(p, shape_raw)]
        else:
            cutoff = int(cutoff_text)
        plain, tex = shape_plain_and_tex(shape_raw)
        rows.append(
            {
                "p": p,
                "shape": plain,
                "shape_tex": tex,
                "diameter": diameter,
                "cutoff": cutoff,
                "bound": False,
            }
        )

    for p, shape_raw, diameter, bound in LOWER_BOUNDS:
        plain, tex = shape_plain_and_tex(shape_raw)
        rows.append(
            {
                "p": p,
                "shape": plain,
                "shape_tex": tex,
                "diameter": diameter,
                "cutoff": bound,
                "bound": True,
            }
        )

    rows.sort(key=lambda row: (row["p"], row["diameter"], row["bound"], row["cutoff"], row["shape"]))
    expected = {4: 2, 5: 3, 6: 6, 7: 11, 8: 23}
    got: dict[int, int] = {}
    for row in rows:
        got[row["p"]] = got.get(row["p"], 0) + 1
    if got != expected:
        raise SystemExit(f"tree counts {got} do not match {expected}")
    return rows


def cutoff_csv(row: dict) -> str:
    if row["bound"]:
        return f">={row['cutoff']}"
    return str(row["cutoff"])


def cutoff_tex(row: dict) -> str:
    if row["bound"]:
        return f"$\\ge {row['cutoff']}^{{*}}$"
    return f"${row['cutoff']}$"


def write_csv(rows: list[dict]) -> None:
    with OUT_CSV.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["p", "shape", "diameter", "cutoff"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "p": row["p"],
                    "shape": row["shape"],
                    "diameter": row["diameter"],
                    "cutoff": cutoff_csv(row),
                }
            )


def write_table(rows: list[dict]) -> None:
    body = []
    previous_p = None
    for row in rows:
        if previous_p is not None and row["p"] != previous_p:
            body.append(r"\addlinespace[0.35em]")
        previous_p = row["p"]
        body.append(
            f"${row['p']}$ & {row['shape_tex']} & ${row['diameter']}$ & {cutoff_tex(row)} \\\\"
        )

    OUT_TABLE.write_text(
        r"""\small
\begin{longtable}{@{} c >{\raggedright\arraybackslash}p{4.55in} c c @{}}
\caption{Cutoffs of unlabeled trees on $4\le p\le 8$ vertices.}
\label{tab:cutoffs}\\
\toprule
$p$ & Shape & Diameter & Cutoff \\
\midrule
\endfirsthead
\multicolumn{4}{@{}l}{\tablename\ \thetable, continued}\\[0.4em]
\toprule
$p$ & Shape & Diameter & Cutoff \\
\midrule
\endhead
\midrule
\multicolumn{4}{r@{}}{\emph{Continued on the next page}}\\
\endfoot
\bottomrule
\endlastfoot
"""
        + "\n".join(body)
        + "\n"
        + r"""\end{longtable}
\normalsize
\noindent{\footnotesize $^{*}$Lower bound. A non-reversal collision remains on the tables computed for this shape, and no complete table has separated its labelings.}
""",
        encoding="utf-8",
    )


def write_document() -> None:
    OUT_DOC.write_text(
        r"""\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage[hidelinks]{hyperref}

\title{Appendix. Cutoffs of unlabeled trees}
\author{}
\date{}

\begin{document}
\maketitle
\thispagestyle{plain}
\vspace{-2.5em}

Let $p\ge 2$, and let a \emph{shape} be an unlabeled tree on $p$ vertices. The \emph{diameter} of a shape is the number of edges on a longest path. For a labeling $P$ of a shape and a host order $t\ge p$, write $N(P,t)$ for the number of labeled trees on the vertex set $[t]$ that avoid $P$ as an ordered minor. Write $C(P)$ for the labeling obtained by replacing each label $i$ with $p+1-i$.

The \emph{cutoff} of a shape is the smallest integer $t$ such that, for labelings $P$ and $Q$ of that shape,
\[
N(P,t)=N(Q,t) \quad\text{implies}\quad Q=P \text{ or } Q=C(P).
\]
At $t=p$ every labeling has the same count, so every cutoff is at least $p+1$. A cutoff is recorded only when every labeling has been counted at that host order and at every smaller host order down to $p+1$, and each of those smaller orders still has a collision outside a reversal pair.

A \emph{spider} has a single vertex of degree greater than $2$; its legs are the path lengths from that vertex to the leaves. A pair of \emph{hubs} is the pair of vertices of degree greater than $2$. Their distance is the number of edges of the unique path joining them, and an arm length is the number of edges from that hub out to a leaf along a path that does not contain the other hub. The two lists of arm lengths are written in the same order as the two degrees. The one remaining shape has three vertices of degree $3$, and the three numbers are the pairwise distances among those vertices.

Table~\ref{tab:cutoffs} lists every unlabeled tree on $4\le p\le 8$ vertices. Forty-one cutoffs are exact. The four marked entries on eight vertices are lower bounds.

\input{cutoff_table.tex}

\end{document}
""",
        encoding="utf-8",
    )


def main() -> None:
    rows = load_rows()
    write_csv(rows)
    write_table(rows)
    write_document()
    exact = sum(1 for row in rows if not row["bound"])
    print(f"wrote {len(rows)} rows ({exact} exact) to {ROOT}")


if __name__ == "__main__":
    main()
