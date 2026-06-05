RNNematode BrainCAD reproducibility code

Purpose
-------
This package checks the saved BrainCAD/ReflexBench result artifacts used in the micropublication figures and technical report. It also regenerates lightweight SVG plots from the packaged CSV tables. It does not rerun policy training.

Quick run
---------

   ./commands_session.sh

Expected output includes:

   RNNematode reproducibility check: OK
   Generated scientific plots:

The quick check uses only the Python standard library. It validates required input artifacts, writes a recomputed headline CSV/JSON summary, and regenerates SVG plots under generated_plots/.

Generated outputs
-----------------
- reproducibility_check_outputs/headline_recomputed_from_packaged_tables.csv
- reproducibility_check_outputs/reproducibility_check_summary.json
- generated_plots/humanoid_fall_auc_reduction.svg
- generated_plots/humanoid_return_auc_gain.svg
- generated_plots/teacher_quality_fall_reduction.svg
- generated_plots/cross_environment_fall_reduction.svg

Optional notebook execution
---------------------------
Install optional dependencies if you want to execute the notebooks:

   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ./commands_session.sh

Included notebooks
------------------
- Codes/01_model_equations_and_action_decomposition.ipynb
- Codes/02_reproduce_main_humanoid_results.ipynb
- Codes/03_reflexbench_video_index.ipynb

Packaged input data
-------------------
- derived_tables/humanoid20_key_results.csv
- derived_tables/cross_environment_summary_micropublication.csv
- derived_tables/morphology_vs_benefit.csv
- derived_tables/teacher_quality_replication_summary.csv
- video_index/representative_video_index.csv
- Figures/RNNematode-Figures.svg
