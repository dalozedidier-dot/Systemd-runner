SystemD — v0.3.1 (Clean Bundle)
===============================

This bundle provides a single entry point (v0.3.1) with a canonical OSF-ready structure:

- 00_core/              Core runner + specs + templates + examples + reference docs
- 01_tests_multisector/ Cross-sector test harness (“profiles-as-contract”) + fixtures + expected outputs
- SXX_TEMPLATE_sector/  Template component structure for sector splits
- 99_releases/          Original source zips + integrity indexes (optional)
- requirements.txt      Minimal deps (tests harness)
- RUNNING.md            How to run core + tests

Notes:
- Core runner is stdlib-only (no external dependencies).
- Test harness requires PyYAML (see requirements.txt).



## References — Tryptique strict (DD / DD-R / E)

Les documents du bundle "Tryptique_DD_DDR_E_strict_v2" sont inclus dans :

- `00_core/docs/strict_triptique_v2/`

Objectif : conserver une séparation stricte entre code (runner/harness) et références formelles (formules/clarifications) sans dépendances d’exécution.
