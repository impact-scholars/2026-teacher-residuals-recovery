# Validation notes

I checked the saved statistics and the source-code pathways used by the micropublication figures.

## Result table checks
- Humanoid headline rows report N=20 seeds: `True`.
- Imitation fall AUC confidence intervals exclude zero: `{'push': True, 'sensor': True, 'slip': True}`.
- Consolidated cortex fall AUC confidence intervals exclude zero: `{'push': True, 'sensor': True, 'slip': True}`.

## Perturbation sanity checks
The four environment summaries report zero event rates in no-perturb controls, positive applied push forces only during push windows, lower friction during slip windows, and larger observation differences during sensor-corruption windows.

## Source-code checks
- Bounded cerebellar residual: `True`.
- Imitation target is teacher minus cortex: `True`.
- Final policy action uses cortex plus gated residual: `True`.
- Consolidation data target uses executed final action: `True`.

## Caveats
- The main Humanoid result is strong and uses N=20. Cross-environment results use smaller replication counts and are presented more cautiously.
- The morphology/evolutionary discussion is a hypothesis-generating observation, not a formal phylogenetic or evolutionary test.
