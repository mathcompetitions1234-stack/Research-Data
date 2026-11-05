# Research data

Supplements for the research notes on ordered minors of labeled trees.

## Star centers

Let \(S_{p,r}\) be the star on \(\{1,2,\ldots,p\}\) with center \(r\), and let \(N(S_{p,r},t)\) be the number of labeled trees on \(\{1,2,\ldots,t\}\) that avoid it as an ordered minor. For \(r \ge 1\) and \(p > 2r\),

\[
N(S_{p,r}, t) > N(S_{p,r+1}, t)
\]

for every \(t \ge p+1\). The cases \(t = p+1\) and \(t = p+2\) are proved. [`star_inequality_t_ge_p_plus_3.txt`](star_inequality_t_ge_p_plus_3.txt) records every exact computation available for \(t \ge p+3\).

There are 56 comparisons, on \(3 \le p \le 8\) and \(6 \le t \le 14\), and none fails. Thirty-two slices have every center. On each of those, the counts fall strictly toward the middle and satisfy \(N(S_{p,r},t) = N(S_{p,p+1-r},t)\). A contraction census and an independent count of the trees with exactly \(p-1\) leaves agree on all 102 values that both produced. There is no complete run for \(p \ge 9\). At \(p = 8\), the orders \(t = 13\) and \(t = 14\) have only the center \(r = 1\), so they are listed and not used as comparisons.

## Cutoffs of unlabeled trees

The table has five columns: \(p\), shape, diameter, cutoff, and one sample Prüfer code on those \(p\) vertices.

| File | Use |
| --- | --- |
| `cutoff_appendix.pdf` | The table. |
| `cutoff_table.tex` | The same table, for `\input` into a paper. |
| `cutoffs.csv` | The same rows as data. |

A cutoff written `>=12` or `>=14` is a lower bound. The paper preamble needs `booktabs`, `longtable`, and `array`.
