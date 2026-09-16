"""Calculate compound interest from command-line inputs."""

from __future__ import annotations

import argparse
import math


def calculate_compound_interest(
    principal: float,
    annual_rate_percent: float,
    compounds_per_year: int,
    total_years: float,
) -> tuple[float, float]:
    """Return the final amount and interest earned.

    ``annual_rate_percent`` is expressed as a percentage, so ``7.34`` means
    an annual rate of 7.34%.
    """
    if principal < 0:
        raise ValueError("principal must be non-negative")
    if annual_rate_percent < 0:
        raise ValueError("annual rate must be non-negative")
    if compounds_per_year <= 0:
        raise ValueError("compounds per year must be greater than zero")
    if total_years < 0:
        raise ValueError("total years must be non-negative")

    periods = compounds_per_year * total_years
    periodic_rate = annual_rate_percent / 100 / compounds_per_year
    final_amount = principal * math.pow(1 + periodic_rate, periods)
    return final_amount, final_amount - principal


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments for the compound-interest calculation."""
    parser = argparse.ArgumentParser(
        description="Calculate compound interest using an annual percentage rate."
    )
    parser.add_argument("principal", type=float, help="starting principal amount")
    parser.add_argument(
        "annual_rate",
        type=float,
        help="annual interest rate as a percentage, for example 7.34",
    )
    parser.add_argument(
        "compounds_per_year",
        type=int,
        help="number of compounding periods per year, for example 12",
    )
    parser.add_argument(
        "total_years",
        type=float,
        help="investment duration in years",
    )
    return parser.parse_args()


def main() -> None:
    """Parse inputs, calculate interest, and print currency-formatted results."""
    arguments = parse_arguments()
    try:
        final_amount, interest_earned = calculate_compound_interest(
            arguments.principal,
            arguments.annual_rate,
            arguments.compounds_per_year,
            arguments.total_years,
        )
    except ValueError as error:
        raise SystemExit(f"error: {error}") from error

    print(f"Final amount: ${final_amount:,.2f}")
    print(f"Interest earned: ${interest_earned:,.2f}")


if __name__ == "__main__":
    main()
