## Fixed-Point C Rule

Only port to C after the Python behavior is validated.

For hardware-oriented C:

Hard rules:

- no runtime division unless explicitly justified
- no floating point unless in reference-only code
- no malloc/free unless approved
- no recursion
- no unbounded loops
- no large frame-sized stack arrays
- no silent overflow
- use fixed-width integer types

Every important signal must document:

```text
signedness
integer bits
fraction bits
total bits
range
rounding
saturation
```

### Fixed-Point Notation

**Do not use ambiguous `Qm.n` notation.** Use only:

- `S<I>.<F>` — signed (1 sign bit + I integer bits + F fractional bits)
- `U<I>.<F>` — unsigned (I integer bits + F fractional bits)

Examples:

- `S1.10` = 1 sign + 1 integer + 10 fractional = 12 bits total
- `U2.10` = 2 integer + 10 fractional = 12 bits total
- `S0.15` = 1 sign + 0 integer + 15 fractional = 16 bits total
- `U8.8`  = 8 integer + 8 fractional = 16 bits total

Required fixed-point table:

| Signal | Signed | Integer Bits | Fraction Bits | Total Bits | Format | Range | Rounding | Saturation | Notes |
|---|---|---:|---:|---:|---|---|---|---|---|

Required multiplier table:

| ID | A Format | A Bits | B Format | B Bits | Product Format | Product Bits | Output Format | Shift | Rounding | Saturation |
|---|---|---:|---|---:|---|---:|---|---:|---|---|

### Right-Shift Rounding

A right shift in fixed-point code is a quantization decision, not just
a bit operation. **Do not silently truncate.** Classify each fractional
down-shift:

- truncate (intentional)
- unsigned round-to-nearest
- signed symmetric round
- round-half-up / round-away-from-zero / round-to-even
- saturate-after-shift
- other explicitly documented policy

Hardware-friendly round-to-nearest (unsigned):
```c
y = (x + (1u << (F - 1))) >> F;     // F = fractional bits dropped
```

Signed symmetric round:
```c
static inline int32_t round_shift_s32(int32_t x, int F) {
    int32_t half = 1 << (F - 1);
    return (x >= 0) ? ((x + half) >> F)
                    : -(((-x) + half) >> F);
}
```

For division-heavy formulas, prefer:

```text
threshold comparison
reciprocal LUT
reciprocal multiply
shift-based scaling
fixed-point approximation
```
