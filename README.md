# Cutoffs of unlabeled trees

Supplement for the research notes on ordered minors of labeled trees. The table lists every unlabeled tree on \(4 \le p \le 8\) vertices, with only the four quantities needed for the appendix: the number of vertices \(p\), the shape, the diameter, and the cutoff.

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
