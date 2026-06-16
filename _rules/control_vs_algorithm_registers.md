## Separate Control Registers from Algorithm Parameters

When designing register maps for hardware, strictly distinguish two categories:

### Control Registers (Infrastructure)
- Resolution, format, buffer depth, memory partitioning
- Performance gates (MAX_BLEND_SLEW, MIPMAP_LOD enable, bandwidth throttle)
- Timing constraints and hardware-specific configuration
- **C model behavior**: Affects *when* and *how much*, not the math
- **Examples**: `SRC_WIDTH`, `SRC_HEIGHT`, `OUT_WIDTH`, `OUT_HEIGHT`, `FETCH_WINDOW_LINES`, `MAX_BLEND_SLEW`, `BANDWIDTH_THRESHOLD`

### Algorithm Registers (Calibration / Data)
- LUT coefficients, mesh control points, sparse grid data
- Gain and offset tables (per-pixel or global)
- Color matrices, sensor input (SENSOR frames)
- Blend weight, interpolation thresholds
- **C model behavior**: Affects the *mathematical result*
- **Examples**: `LUT_BASE_A`, `LUT_BASE_B`, `BLEND_WEIGHT`, `CALIBRATION_GAIN_MESH`, `COLOR_MATRIX_COEFFS`

### Design Rule

1. **Do not use algorithm parameters as control valves**:
   - If you are tempted to increase a gain/offset to reduce bandwidth, that is a control decision; use a dedicated control register instead.
   - Do not hide memory optimization or timing fixes inside algorithm calibration.

2. **Do not tune control registers to fix algorithmic problems**:
   - If lowering `MAX_BLEND_SLEW` hides a color artifact, the artifact is algorithmic; fix the LUT or matrix, not the slew limiter.
   - Do not over-constrain `LUT_DELTA_THRESHOLD_X/Y` to work around mesh density issues.

3. **C ↔ RTL parity**:
   - All algorithm registers must be C-simulatable; the C model reads them and produces bit-exact results.
   - Control registers may be RTL-only if they have no algorithmic meaning (e.g., `OUTPUT_RING_DEPTH` is SoC-specific).

4. **Version and document both categories together**:
   - In the register map, mark each register as `CONTROL` or `ALGORITHM`.
   - When freezing registers for a release, document why (algorithm convergence vs. hardware optimization).
   - Separate control changes from algorithm tuning in release notes and commit messages.
