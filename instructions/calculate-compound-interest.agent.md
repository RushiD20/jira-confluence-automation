# Calculate Compound Interest

Use `tools/compound_interest.py` when a request requires calculating an investment's or loan's compound-growth final amount and interest earned from a principal, annual rate, compounding frequency, and duration.

Use this tool when:
- The request provides or asks for a principal amount.
- The annual interest rate and compounding frequency are known or can be clarified.
- The duration is expressed in years, including fractional years.
- The result should include both the final amount and the interest earned.

Do not use this tool when:
- The request requires simple interest, continuous compounding, irregular deposits or withdrawals, taxes, fees, inflation, or changing rates.
- The required inputs are missing and cannot be reasonably clarified.
- The calculation requires a payment schedule or an amortization model.

Invocation:
- Run the command from the repository root.
- Use this argument order:

```powershell
python tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <total_years>
```

- Provide `annual_rate` as a percentage, not a decimal. For example, use `7.34` for 7.34%.
- Provide `compounds_per_year` as a positive integer, such as `12` for monthly compounding.
- Provide `total_years` as a non-negative number. Use a fractional year when the duration includes partial years.

Example:

```powershell
python tools/compound_interest.py 15847 7.34 12 8.583333333333333
```

Processing steps:
1. Confirm that the inputs match the tool's argument order and units.
2. Invoke the script from the repository root.
3. Capture the `Final amount` and `Interest earned` lines exactly.
4. Check for a non-zero exit or an `error:` message.
5. If the command fails, correct invalid inputs or report the specific error; do not invent a result.

Result presentation:
- Report the final amount and total interest earned in currency, rounded to two decimal places.
- Label the values clearly as `Final amount` and `Interest earned`.
- State the principal, annual rate, compounding frequency, duration, and number of periods when explaining the result.
- Mention that the annual rate was interpreted as a percentage when there could be ambiguity.
- Do not present unrounded intermediate floating-point values as the financial result.

Constraints:
- Principal and annual rate must be non-negative.
- Compounds per year must be greater than zero.
- Total years must be non-negative.
- Do not silently reinterpret a decimal rate such as `0.0734`; clarify whether the user means 0.0734% or 7.34%.
- Preserve the script's output labels and report command failures explicitly.
