## Config Register Rule

For RTL-oriented work, separate registers into two categories and document each:

### 1. **Control Registers** (Infrastructure / Timing / Hardware-specific)

These registers **have no algorithmic meaning** in C code and exist only to manage hardware behavior:

- **Resolution / format control**: `SRC_W`, `SRC_H`, `OUT_W`, `OUT_H`, `FORMAT`, `INPUT_MODE`
- **Buffer / memory sizing**: `MAX_FETCH_LINES`, `OUT_RING_DEPTH_LINES`, scratchpad partition registers
- **Timing / performance gates**: `BLEND_MAX_SLEW_Q8`, `MIPMAP_MAX_LOD`, bandwidth monitor thresholds
- **Timing constraints**: `MESH_DENSITY_X/Y` (hardware architecture choice, frozen at boot)
- **Status / handshake**: `CONFIG_VALID`, interrupts, completion flags
 - **Resolution / format control**: `SRC_WIDTH`, `SRC_HEIGHT`, `OUT_WIDTH`, `OUT_HEIGHT`, `PIXEL_FORMAT`, `INPUT_MODE`
 - **Buffer / memory sizing**: `FETCH_WINDOW_LINES`, `OUTPUT_RING_DEPTH`, `SCRATCHPAD_BASE`, `SCRATCHPAD_SIZE`
 - **Timing / performance gates**: `MAX_BLEND_SLEW`, `MIPMAP_MAX_LOD`, `BANDWIDTH_THRESHOLD`
 - **Timing constraints**: `MESH_DENSITY` (hardware architecture choice, frozen at boot)
 - **Status / handshake**: `CONFIG_COMMIT`, `STATUS_FLAGS`, interrupts, completion flags

**Key property**: Changing a control register changes **how** the algorithm runs (speed, memory footprint, feature enable/disable), not **what** computation happens.

### 2. **Algorithm Data Registers** (Calibration / Algorithmic Parameters)

These registers carry the **actual algorithm state** and must remain in sync between C model and RTL:

- **LUT / mapping tables**: `LUT0_BASE`, `LUT1_BASE`, mesh coordinates, sparse-mesh control points
- **Blend / blending weights**: `BLEND_WEIGHT_Q8`, `LUT_DELTA_TH_X/Y`
- **Gain / offset tuning**: per-pixel gains, per-pixel offsets, global gain/offset
- **Color / CSC matrices**: `YUV_MATRIX_MODE`, custom coefficients, bias values
- **Sensor input**: IMU pitch, angular velocity, frame time
 - **LUT / mapping tables**: `LUT_BASE_A`, `LUT_BASE_B`, mesh coordinates, sparse-mesh control points
 - **Blend / blending weights**: `BLEND_WEIGHT`, `LUT_DELTA_THRESHOLD_X/Y`
 - **Gain / offset tuning**: `PER_PIXEL_GAIN`, `PER_PIXEL_OFFSET`, `GLOBAL_GAIN`, `GLOBAL_OFFSET`
 - **Color / CSC matrices**: `COLOR_MATRIX_MODE`, `COLOR_MATRIX_COEFFS`, bias values
 - **Sensor input**: `SENSOR_PITCH`, `SENSOR_GYRO`, frame time

**Key property**: These registers carry customer calibration, algorithmic tuning, or frame-specific input data. Changing them changes the **mathematical result**.

### Register Table Format

For each category, list registers:

| Register | Bits | Type | Default | Shadow | Update Timing | Category | Description |
|---|---:|---|---:|---|---|---|---|

Fill the **Category** column with `CONTROL` or `ALGORITHM`.

**Shadow behavior** (explicit for both types):
- **Control registers**: Often immediate (resolution, format), but timing guards like `BLEND_MAX_SLEW_Q8` may be frame-boundary shadowed
- **Algorithm registers**: Typically frame-boundary or line-boundary shadowed to avoid mid-frame inconsistency
 - **Control registers**: Often immediate (resolution, format), but timing guards like `MAX_BLEND_SLEW` may be frame-boundary shadowed
 - **Algorithm registers**: Typically frame-boundary or line-boundary shadowed to avoid mid-frame inconsistency

Every runtime parameter must be included.
