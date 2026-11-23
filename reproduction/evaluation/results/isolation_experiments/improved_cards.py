# Improved BioMate method cards (v2) — benchmark-driven improvement of the harness.
# Rationale: v1 protocol card gave no WARN criterion -> models collapsed to PASS (balanced
# accuracy dropped). v1 PBPK card had the right formula but models fumbled arithmetic (within-2fold
# ~0.9 not 1.0). These are FIXED GENERAL METHOD KNOWLEDGE, never per-item answers.

KB_V2 = {
"protocol_thresholds":
"""HARNESS KB -- protocol-aware QC interpretation (BioMate rule knowledge). Decide PASS / WARN / FAIL
by applying THREE steps IN ORDER. Do NOT default to PASS: ~30% of cases are WARN or FAIL.

STEP 1 - GENUINE FAILURE -> FAIL.
The sample FAILS, regardless of protocol, when the problem is a true technical/quality defect with
no protocol-level excuse: contamination (rRNA, adapter, index hopping), barcode/UMI collisions or
all-identical barcodes, run/instrument failure (pore blockage, >50% of reads unusably short), sample
swap, or anything described as 'genuinely defective' / 'None (no protocol reason)'. A STANDARD
(non-specialized) protocol with an out-of-spec metric and no protocol reason also FAILs.

STEP 2 - FULLY EXPECTED DEVIATION -> PASS.
If the flagged metric is an EXPECTED consequence of a SPECIALIZED protocol's design AND its value is
within the normal range for that protocol, the sample is VALID -> PASS. Examples: low UMIs/genes on
10x Flex / low-input / single-cell / Smart-seq; short inserts & lower mapping on FFPE / cfDNA /
ancient; extreme duplication & uneven coverage on amplicon / 16S / targeted panels; higher intronic
fraction (and sometimes %mito) on snRNA; low contrast on standard small-protein cryo-EM; PCR-free vs
PCR duplication differences.

STEP 3 - EXPECTED IN KIND BUT EXTREME, OR ONLY PARTIALLY VALID -> WARN (advisory).
If the deviation is of a protocol-expected KIND but is MORE EXTREME than the protocol normally
excuses, OR the data is usable only with caveats / for a subset, call WARN -- do not silently PASS it
and do not FAIL usable data. Signals of WARN: 'valid for selected genes only', reads/cell or
UMIs/cell far below even the protocol's already-low range, 10-year / severely degraded FFPE,
very-small-protein cryo-EM below even the relaxed picking confidence, borderline/advisory metrics.
WARN is correct whenever the data is still scientifically usable but the deviation is notable enough
that a reviewer must be flagged.

Return exactly one of PASS / WARN / FAIL. Apply 1 -> 2 -> 3 in order; reach PASS only if neither a
genuine failure (1) nor an extreme/partial-validity caveat (3) applies.""",

"pbpk_benchmark":
"""HARNESS KB -- standardized one-compartment oral exposure method. COMPUTE STEP BY STEP and show each
intermediate number (do the arithmetic explicitly; keep >=3 significant figures; do not approximate).

Cmax (uM) = F * (dose_mg / MW / Vd_L) * 1000
  Step 1:  moles_mmol = dose_mg / MW            (MW in g/mol  -> mmol)
  Step 2:  conc_mM     = moles_mmol / Vd_L       (-> mM)
  Step 3:  Cmax_uM     = conc_mM * 1000 * F      (mM->uM, times bioavailability fraction F in [0,1])

WORKED EXAMPLE (dose_mg=100, MW=500, Vd_L=50, F=0.5):
  Step 1:  moles_mmol = 100 / 500 = 0.200 mmol
  Step 2:  conc_mM     = 0.200 / 50 = 0.00400 mM
  Step 3:  Cmax_uM     = 0.00400 * 1000 * 0.5 = 2.00 uM

Read F, MW, Vd_L, dose_mg from the inputs. Report Cmax in uM to 3 significant figures. A common error
is dropping the *1000 (mM->uM) or forgetting *F -- carry every factor exactly.""",

"boin_benchmark":
"""HARNESS KB -- standardized exposure-response (Emax) dose-selection method for a BOIN trial.
COMPUTE STEP BY STEP for EVERY dose level; show the numbers.
For each dose level d (mg) in the dose grid:
  Step 1:  C_nM  = F * (d / MW / Vd_L) * 1e6     (d/MW = mmol; /Vd_L = mM; *1e6 = nM)
  Step 2:  DLT(d) = ER_E0 + ER_Emax * C_nM / (ER_EC50_nM + C_nM)        (Emax model)
Then:
  Step 3:  admissible = { d : DLT(d) <= DLT_rate_target + 0.10 }.
           If the LOWEST dose already exceeds target + 0.10 -> NO SAFE DOSE (no MTD).
  Step 4:  MTD = admissible dose whose DLT(d) is CLOSEST to the target; on a tie choose the HIGHER dose.
WORKED PATTERN: compute DLT at every d, list them, then pick by Step 3-4. Use ER_E0, ER_Emax,
ER_EC50_nM, F, MW, Vd_L and the dose grid from the inputs. Report the selected MTD dose in mg.""",
}
