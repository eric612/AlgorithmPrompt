## RTL-Friendly Rule

If the user asks for hardware-friendly implementation, prefer:

```text
block-based processing
streaming line-by-line loop
bounded buffers
explicit border policy
explicit latency assumption
explicit valid timing
```

Always mark the gap between:

```text
Python reference
practical demo
hardware-friendly approximation
```

If large memory is required, explain why local buffer is insufficient,
DRAM read/write bandwidth, burst pattern, tile size, and worst-case
access pattern.

Do not optimize for hardware before the algorithm behavior is clear.
