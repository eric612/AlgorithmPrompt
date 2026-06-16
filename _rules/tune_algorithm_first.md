## Tune Algorithm First, Then Parameters

When results are unsatisfactory:

1. **First diagnose the algorithm** - Identify structural deficiencies or flaws:
   - Does the algorithm fundamentally solve the problem?
   - Are there missing steps or incorrect logic?
   - Is the mathematical foundation sound?
   - Can you visualize where the algorithm breaks?

2. **Fix the algorithm** before tuning parameters:
   - Correct flawed assumptions or logic errors.
   - Add missing algorithmic steps or improvements.
   - Verify the fixed algorithm works better conceptually.

3. **Only then adjust parameters**:
   - Once the algorithm is sound, optimize parameters for performance.
   - Tune with diverse datasets, not just the current problem case.

4. **Avoid scenario-specific over-tuning**:
   - Do not add hacks or parameters solely for one edge case.
   - Maintain algorithm generality and reusability.
   - If a parameter only helps one scenario, it signals an algorithm flaw.

5. **Test generality**:
   - Verify tuned parameters work across multiple datasets and conditions.
   - If performance degrades on new data, return to step 1 (algorithm diagnosis).
