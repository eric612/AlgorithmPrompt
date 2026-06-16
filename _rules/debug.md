## Debug Rule

When debugging, follow:

```text
reproduce
→ localize
→ reduce
→ fix
→ verify
```

For image, signal, motion vector, or array output:

- compare visually
- compare numerically
- save intermediate outputs when useful

For numerical comparison, report:

```text
shape
dtype
min / max
MAE
RMSE
max absolute error
mismatch count
worst mismatch location
```

If the observation is inconclusive after several probes, ask the user instead of guessing.
