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

The table lists every unlabeled tree on \(4 \le p \le 8\) vertices, with only the four quantities needed for the appendix: the number of vertices \(p\), the shape, the diameter, and the cutoff.

The diameter is the number of edges on a longest path. The cutoff is the smallest host order \(t\) at which equal avoidance counts force two labelings of the shape to be equal or reversals of each other. Reversal replaces each label \(i\) by \(p+1-i\).

Forty-one cutoffs are exact. Four shapes on eight vertices still collide on the tables computed so far; those rows are lower bounds and are marked in the cutoff column.

## Files

| File | Use |
| --- | --- |
| `cutoff_appendix.tex` | Standalone appendix. Compiles to the PDF. |
| `cutoff_appendix.pdf` | The appendix, ready to attach. |
| `cutoff_table.tex` | The table alone, for `\input` into the paper. |
| `cutoffs.csv` | The same rows as data: `p`, `shape`, `diameter`, `cutoff`. |

A cutoff written `>=12` or `>=14` in the CSV is a lower bound, matching the starred inequalities in the table.

## Include it in the paper

The paper preamble needs `booktabs`, `longtable`, and `array`. Then, inside the appendix:

```latex
\input{cutoff_table.tex}
```

The paragraphs that define shape, diameter, and cutoff are in `cutoff_appendix.tex`, above the `\input`. Copy those as well if the paper does not already contain them.

Compile the standalone copy with:

```bash
tectonic cutoff_appendix.tex
```
