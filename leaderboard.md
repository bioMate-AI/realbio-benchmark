# RealBio: condition comparisons

This file supersedes the historical product-ranking board. Values summarize fixed endpoint panels; item counts and model counts differ across rows. No overall rank or composite score is calculated. Values are displayed at manuscript precision. Full-precision per-file outputs and reference sets are in `reproduction/`.

## Main paired comparisons

| Endpoint | Models | Bare | Guided | Difference [95% interval] |
|---|---:|---:|---:|---|
| Routing accuracy | 14 | 0.382 | 0.913 | +0.530 [0.484, 0.578] |
| Parameter F1 | 4 | 0.079 | 0.701 | +0.622 [0.580, 0.660] |
| Parameter joint success | 4 | 0.179 | 0.371 | +0.191 [0.122, 0.260] |
| Method-selection accuracy | 8 | 0.925 | 0.988 | +0.0625 [0.022, 0.116] |

Joint parameter success requires every required value to match and no listed forbidden key to be emitted. It is not exact-object correctness: other extra keys can escape that joint criterion. Mean exact-object success under the historical value-equivalence rule is 0.078 bare and 0.371 guided. Of the 170 items, 26 require no keys; historical empty-object coercion can earn vacuous success on that subset. These scoring effects are disclosed and stratified in the supplementary analysis.

Context increases parameter completeness but also increases forbidden fills. For method selection, six of eight per-model intervals include zero; the positive aggregate difference is not a universal improvement for every endpoint.
