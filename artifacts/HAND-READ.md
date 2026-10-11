# EDGAR 8-K/A — the hand-read: what Item 4.02 amendments actually do

Twenty-one filings (2025Q1–2026Q3) where an 8-K/A amends an Item 4.02 non-reliance
disclosure — every filing our language flags (non_reliance ∧ item_402) matched. All 21
read by hand (excerpts: `core21-excerpts.json`). The flag caught the EVENT layer, but the
amendments do five different things to it:

| type | n | what the amendment does | examples |
|---|---|---|---|
| A. expand | 5 | adds periods/companies to the non-reliance (Crypto Co #1+#2 widen 2023→2024→interims; Next Technology ×2 tax under-provision detail; La Rosa rewrite) | Crypto Co, Next Technology, La Rosa, ABVC |
| B. correct | 6 | fixes the original 4.02's disclosure (SEC comment-letter response, missing requirements, wrong item cross-refs) | GraphJet ("solely to clarify, in response to a comment from the SEC's staff"), Cytta ("did not comply with all the requirements"), Spectral #1, SHF, NEONC |
| C. retract / soften | 4 | walks the non-reliance BACK: change "not material", "will not restate", original 4.02 "was inaccurate", "did not identify any specific items…incorrect" | Apple iSports ×2, Spectral #2, Northann |
| D. reclassify | 1 | fixes the item number itself (the event was never non-reliance) | Nukkleus ("4.02 → 8.01"), Bancorp |
| E. boilerplate FP | 1 | quotes the item title without the event ("any such determination, if made, would be disclosed…") | Groovy (Nukkleus reclassified to D) |

Counts are hand-judgment on 21 filings, not a coded rubric — borderline calls: Bancorp
(D), ABVC (A), Pacific Green (A but "will not affect reported net income" → C-leaning).

## The finding worth carrying

**A 4.02 is a process, not an event — and the amendment layer is where it gets edited.**
Of 21 amendments: 9 expand/confirm, 6 correct its compliance, 4 retract or soften, 1 reclassify, 1 is boilerplate. Per-filing assignment: core21-assignment.json (all 21 rows, one primary category each + justification notes).
For anyone consuming EDGAR signals mechanically: an Item 4.02 8-K/A can mean the non-reliance
got WORSE, got fixed, or never happened. The direction is in the amendment text. Precision measured on the hand-read: 15/21 (71%) flag+item → true ongoing non-reliance; flag alone 15/91 (16%).

## Caveats

- 21 filings = every language-flag hit in 2025Q1–2026Q3, so the "base rate" of true
  non-reliance amendments is ~14/2,510 (0.6%) — the flag alone is not a signal.
- Micro-cap-dominated sample (most filers OTC/small-cap; one filing agent, 0001213900,
  accounts for 7 of 21 accessions). Not a large-cap restatement story.
- auditor_change regex was too rigid (0 hits) — not used.
- Our amendment→base join is nearest-preceding-8-K heuristic (15 business days); the
  originals referenced in the texts confirmed the join on every hand-read where the
  original's date was stated (18 of 21 stated it; all matched).
