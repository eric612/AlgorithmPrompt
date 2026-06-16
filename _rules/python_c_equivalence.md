## Python/C Equivalence Rule

Python is usually the golden reference when comparing to the C model.

When comparing Python and C, report:

```text
shape
dtype
min / max
MAE
RMSE
max absolute error
mismatch count over tolerance
worst mismatch locations
```

Classify mismatches:

- expected quantization error
- rounding difference
- saturation difference
- border handling difference
- coordinate/layout difference
- C overflow
- unknown

If unknown and stuck, ask the user.
