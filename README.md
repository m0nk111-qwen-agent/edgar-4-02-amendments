# The amendment layer: what Item 4.02 8-K/A filings actually do

SEC EDGAR, 2025Q1–2026Q3. We collected every **Form 8-K/A amendment** in seven quarters of
EDGAR full-index master files (2,575 amendments), joined each to its nearest preceding base
8-K by filer CIK (within 15 business days), and language-flagged the amendment full
submissions for non-reliance language. 91 amendments (3.6%) matched non-reliance language;
23 mentioned Item 4.02; **21 matched both — and all 21 were read by hand.**

The 21 are not 21 confirmations of non-reliance. They are five different moves on the same
red flag (one primary category per filing — `artifacts/core21-assignment.json` has all 21
rows with the note that justified each call):

| type | n | what the amendment does | examples |
|---|---|---|---|
| A. expand / confirm | 9 | adds periods/companies, or confirms the event (incl. one auditor-opinion-withdrawal: the "related audit report" branch of the item) | Crypto Co (widens 2023→2024→interims), Next Technology Holding ×2, La Rosa, ABVC, American Resources |
| B. correct | 6 | completes/corrects the original 4.02's own disclosure (SEC comment-letter response, missing requirements) | GraphJet ("solely to clarify, in response to a comment from the SEC's staff"), Cytta ("did not comply with all the requirements"), Bancorp |
| C. retract / soften | 4 | walks the non-reliance back: change "not material", "will not restate", original "was inaccurate" | Apple iSports ×2, Spectral, Northann |
| D. reclassify | 1 | the event was never non-reliance (item number fixed) | Nukkleus ("4.02→8.01") |
| E. boilerplate FP | 1 | quotes the item title without the event ("any such determination, if made, would be disclosed…") | Groovy |

**Precision of the language flag, measured on the hand-read:** 15 of 21 (71%) describe a
real, ongoing non-reliance; the flag alone is worse — 15 of 91 language-flagged filings
(16%). So: flag-only is noise, flag+item-number is a coin-flip-plus, and neither replaces
reading the amendment.

**The finding:** an Item 4.02 8-K/A can mean the non-reliance got *worse*, got *fixed*, or
*never happened*. The direction lives in the amendment text. Floor base rate of true
non-reliance amendments among all 8-K/A: 15/2,510 (**0.6%**) — a floor because recall of the
regexes is unmeasured (filings can restate without saying "non-reliance"). With n=15 events
the 95% binomial band is roughly 0.3–1.0%; treat 0.6% as an order of magnitude, not a rate.

The investor one-liner we consider defensible — *attributed to prior legal context, not to
our measurements*: "A 4.02 says past reported results are unreliable — it routinely precedes
restatements, auditor departures, litigation and enforcement; but watch the amendment,
because it can also take the claim back." (Item 4.02 of Form 8-K, SEC Release No. 33-8400,
requires filing within 4 business days when prior financials are determined unreliable or
the accountant advises the same; SAB 99/108's little-r "revision" path exists partly so
companies can avoid this item — which is exactly why the amendment layer is informative.)

## Timing: when amendments land

Gap between a base 8-K and its 8-K/A (all 2,510 paired amendments, business days):
**median 3, p75 12, p95 36.** Only 45% land within 72 hours — a 72-hour join window would
silently drop over half the distribution. Amendments to *non-reliance* disclosures take even
longer (median 5 business days; 19% within 72h).

## Files

- `data/edgar-8ka-pairs.json` — the 2,510 paired amendments (of 2,575 collected; 65 had no preceding base 8-K inside the 7-quarter history). Schema: each row = amendment with `base_accession`, `gap_bus_days`, `gap_cal_days`, `filer_prefix_match`, `within_72h`, `window:'15bd'`.
- `data/edgar-8ka-flags.jsonl` — one row per amendment: language flags (`non_reliance`, `item_402`, `restatement`, `material_weakness`), the pair fields, fetch status.
- `data/core21-excerpts.json` — the non-reliance-language excerpts from the 21 hand-read filings.
- `artifacts/core21-assignment.json` — all 21 filings, one primary category each, with the justification note. (Counts above derive from this file.)
- `artifacts/summary.json` — every count quoted in this README, in one file.
- `artifacts/HAND-READ.md` — the full typology with caveats and borderline calls.
- `code/edgar_8ka_collect.py` — full-index downloader + joiner (7 quarters, descriptive User-Agent required by SEC).
- `code/edgar_8ka_flag.py` — resumable flagger (0.35 s pacing, one fetch per full submission).

## Caveats (read before citing)

- **21 filings is small** and micro-cap-dominated: most filers are OTC/small-cap; one filing
  agent (0001213900) accounts for 7 of 21 accessions. This is not a large-cap restatement story.
- The amendment→base join is a **nearest-preceding-8-K heuristic** (15 business days), validated
  only within the hand-read subset: 18 of 21 filings stated the original's filing date in-text
  and all 18 matched the join. Outside the 21, the join is unverified.
- `auditor_change` regex was too rigid (0 hits) and is **not used** in any count.
- Typology counts are hand-judgment on one pass by one coder, not a coded rubric; borderline
  calls are flagged in the assignment file (e.g. Pacific Green "will not affect reported net
  income" → A-leaning; Bancorp → B on the same borderline logic).
- We did not verify each filing's SGML header submission type beyond the master-index form
  string; the master-index format was fetched live 2026-10-11 (`full-index/YYYY/QTRn/master.gz`).
- 8-K/A volume per quarter was steady (~390/quarter); nothing here is a trend claim — the
  typology and the measured precisions are the claims.

## Provenance

Collected 2026-10-11 from `sec.gov/Archives/edgar/full-index/` (7 quarters, 2025Q1–2026Q3).
Public data; descriptive User-Agent per SEC fair-access policy. MIT license. By
[Pennyforge](https://dev.to/pennyforgehq) — small research studio; the Show HN launch-age
dataset ([showhn-repo-age](https://github.com/m0nk111-qwen-agent/showhn-repo-age)) is a sibling.
