# Teacher-guided corrective residuals in BrainCAD locomotion

This repository contains the public reproducibility package for a Neuromatch Impact Scholars micropublication by Team RNNematode. The project asks a narrow motor-control question: when a simulated animal is pushed, slipped, or sensor-corrupted, does a biologically inspired corrective circuit help by architecture alone, or does it need a structured teaching signal?

The full BrainCAD codebase used for the original locomotion experiments is available at [andrestrocyte/braincad](https://github.com/andrestrocyte/braincad).

The main result is that PPO-only corrective modules did not reliably learn fast recovery in this BrainCAD/ReflexBench setting. A teacher-guided cerebellar residual did. The result is intentionally framed as a learning-signal result, not as a claim that we discovered a new biological mechanism.

## Scientific claim

A cerebellar-style residual controller improved reflex-like recovery when it was trained to imitate a perturbation-trained teacher's correction:

```text
base action:       u_ctx = cortex(obs)
teacher target:    Δu* = u_teacher - u_ctx
executed action:   u = clip(u_ctx + α Δu_cb)
```

The same trained checkpoint was evaluated with the residual switched ON and OFF under identical perturbation schedules. The residual reduced fall AUC and improved return AUC in Humanoid across 20 seeds. The correction could also be distilled into a cortex-only policy, suggesting that the residual can act as a training scaffold rather than permanent inference-time machinery.

## Quick reproduction

The command below validates the packaged result tables and regenerates lightweight SVG plots from the saved CSV files. It does not retrain policies and does not require LaTeX, Jupyter, pandas, or matplotlib.

```bash
git clone https://github.com/andrestrocyte/rnnematode-micropublication.git
cd rnnematode-micropublication
./commands_session.sh
```

Expected output:

```text
RNNematode reproducibility check: OK
Generated scientific plots:
- generated_plots/cross_environment_fall_reduction.svg
- generated_plots/humanoid_fall_auc_reduction.svg
- generated_plots/humanoid_return_auc_gain.svg
- generated_plots/teacher_quality_fall_reduction.svg
```

## What gets regenerated

`./commands_session.sh` runs two small scripts:

- `scripts/check_reproducibility.py` checks that the required CSVs, figures, and video index are present and recomputes a compact headline summary.
- `scripts/generate_scientific_plots.py` converts the packaged CSV tables into four SVG plots.

Generated outputs are written to:

- `reproducibility_check_outputs/headline_recomputed_from_packaged_tables.csv`
- `reproducibility_check_outputs/reproducibility_check_summary.json`
- `generated_plots/*.svg`
- `generated_plots/plot_manifest.csv`

## Main files

- `RNNematode-Micropublication.pdf`: short micropublication.
- `report/RNNematode-TechnicalReport.pdf`: longer technical report with equations and controls.
- `RNNematode-Micropublication.tex`: LaTeX source for the short paper.
- `myst_submission/index.md`: MyST Markdown source.
- `Figures/RNNematode-Figures.svg`: main figure sheet.
- `Figures/RNNematode-Supplementary-Figures.svg`: supplementary checks.
- `derived_tables/`: saved CSV summaries used by the figures and report.
- `Codes/`: brief notebooks for equations, headline results, and video metadata.
- `video_index/representative_video_index.csv`: index of representative ReflexBench videos.
- `RNNematode_micropublication_code.zip`: zipped code/data archive for submission systems.

## Optional notebook run

The notebooks are not required for the quick check. To execute them locally, install the optional dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
./commands_session.sh
```

If Jupyter is available, `commands_session.sh` will execute notebooks in `Codes/` after generating the lightweight plots.

## Optional PDF rebuild

The PDFs are checked in. If `latexmk` is installed, this command recompiles them:

```bash
./build.sh
```

If LaTeX is not installed, `build.sh` still runs the artifact checks and leaves the existing PDFs untouched.

## Scope of this repository

This repository is a compact reproducibility release. It includes saved result tables, figures, notebooks, and validation scripts. It does not include heavy PPO checkpoints or rerun the full training campaign. The intended use is to verify the reported scientific outputs from packaged artifacts, not to reproduce every training run from scratch.

## License

Executable code is released under the MIT License. Scientific figures, tables, and PDFs are included to document and reproduce the reported result.
