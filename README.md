Overview

The Yield Curve Project is a powerful financial tool designed for advanced curve interpolation, calibration, and volatility surface generation. This project enables smooth and accurate construction of yield curves and provides robust capabilities for pricing and risk management of financial instruments such as swaps, FRAs, basis swaps, cross-currency swaps, futures, and swaptions.

By using advanced numerical techniques, the project ensures precision and flexibility in modeling market instruments, making it an essential tool for financial institutions, quantitative analysts, and researchers.

Key Features

1. Yield Curve Interpolation and Calibration

The project supports curve interpolation and calibration using market data to create smooth and continuous yield curves. Key features include:

Linear Interpolation: Piecewise-linear interpolation between data points.

Spline Interpolation: Cubic splines for smoother and more natural curves.

Bootstrapping: Constructs the curve from market instrument prices (e.g., swaps, FRAs).

Curve Adjustments: Refines the curve to align with observed market conditions.

2. Swap Pricing and Calibration

The project provides tools for pricing and calibrating interest rate swaps:

Fixed-for-floating swaps.

Basis swaps for comparing two floating rates.

Cross-currency swaps for managing currency exposure.

3. Forward Rate Agreements (FRAs)

Accurately prices and calibrates FRAs based on the yield curve.

Uses day count conventions.

Handles both standard and custom tenors.

4. Future Pricing

Supports the calibration of interest rate futures:

Incorporates market pricing of futures contracts.

Adjusts curves to match forward rates implied by futures.

5. Swaption Volatility Surface Creation

Generates swaption volatility surfaces using SABR (Stochastic Alpha, Beta, Rho) model calibration:

Produces a smooth volatility surface for a range of strikes and maturities.

Supports market conventions for ATM volatilities and SABR parameters.

6. Cross-Currency Instruments

Handles cross-currency basis swaps, incorporating:

FX forward rates.

Basis adjustments to account for different currencies.

Technical Highlights

Scalable Architecture: Supports a wide range of financial instruments with extendable design.

Mathematical Rigor: Implements advanced interpolation techniques, such as cubic splines and SABR models.

Python Integration: Built with Python for easy integration with other quantitative tools and libraries.

Customizability: Flexible to adapt to unique market requirements and data formats.

Getting Started

Clone the repository:

git clone <repository-url>

Install dependencies:

pip install -r requirements.txt

Run example scripts:

python examples/swap_pricing.py

Use Cases

This project is ideal for:

Risk Management: Deriving curves for accurate valuations and risk assessment.

Trading: Pricing derivatives like swaps, swaptions, and futures.

Research: Studying market trends and testing pricing models.

Contributing

We welcome contributions! Feel free to submit pull requests or open issues to improve functionality, fix bugs, or add features.

License

This project is licensed under the MIT License.
