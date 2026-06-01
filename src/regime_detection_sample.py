"""
AI Capital — Illustrative code sample: regime detection
========================================================

This is a SIMPLIFIED, ILLUSTRATIVE version of the regime-detection logic,
provided to demonstrate code style and approach. Production thresholds and
parameters are intentionally omitted, as this is an active strategy.

The real system runs on QuantConnect / LEAN with additional layers
(risk-parity weighting, volatility targeting, hard caps, trailing-drawdown
monitoring, crisis routing) documented in /docs/architecture.md.
"""

import numpy as np


def detect_regime(price, sma200, sma_slope_positive, breadth,
                  vol_annualized, short_term_drawdown,
                  vol_bear_threshold, vol_crisis_threshold,
                  breadth_riskon, breadth_riskoff):
    """
    Classify the market into one of four regimes using a 6-indicator score.

    Parameters
    ----------
    price : float
        Current benchmark (SPY) price.
    sma200 : float
        200-day simple moving average.
    sma_slope_positive : bool
        Whether the SMA200 slope is rising.
    breadth : float
        Fraction of tracked equity ETFs in an uptrend (0..1).
    vol_annualized : float
        Annualized short-window volatility of the benchmark.
    short_term_drawdown : float
        Drawdown over the recent window (e.g. 63 days), as a negative fraction.
    *_threshold / breadth_* : float
        Regime thresholds (values kept generic here).

    Returns
    -------
    str : one of "RISKON", "NEUTRAL", "RISKOFF", "CRISIS"
    """
    # CRISIS override: extreme volatility AND weak breadth -> protect capital
    if vol_annualized > vol_crisis_threshold and breadth <= breadth_riskoff:
        return "CRISIS"

    score = 0

    # 1. Trend: price vs long moving average
    score += 1 if price > sma200 else -1

    # 2. Trend direction: slope of the moving average
    score += 1 if sma_slope_positive else -1

    # 3. Market breadth
    if breadth >= breadth_riskon:
        score += 1
    elif breadth <= breadth_riskoff:
        score -= 1

    # 4. Volatility regime
    if vol_annualized > vol_crisis_threshold:
        score -= 2
    elif vol_annualized > vol_bear_threshold:
        score -= 1
    else:
        score += 1

    # 5. Short-term drawdown
    if short_term_drawdown < -0.10:
        score -= 1

    # Map score to regime
    if score >= 2:
        return "RISKON"
    elif score <= -1:
        return "RISKOFF"
    else:
        return "NEUTRAL"


def inverse_volatility_weights(volatilities):
    """
    Risk-parity weighting: allocate inversely to each asset's volatility,
    so each position contributes comparable risk to the portfolio.

    Parameters
    ----------
    volatilities : dict[str, float]
        Mapping of asset ticker -> annualized volatility.

    Returns
    -------
    dict[str, float] : normalized weights summing to 1.0
    """
    inv = {t: 1.0 / v for t, v in volatilities.items() if v > 0}
    total = sum(inv.values())
    if total <= 0:
        return {}
    return {t: w / total for t, w in inv.items()}


def apply_volatility_target(weights, estimated_portfolio_vol,
                            target_vol=0.10, max_leverage=1.0):
    """
    Scale portfolio weights toward a target volatility, without leverage.
    If estimated vol exceeds target, scale down. Never scale above 1.0x.
    """
    if estimated_portfolio_vol <= 0:
        return weights
    scale = min(target_vol / estimated_portfolio_vol, max_leverage)
    return {t: w * scale for t, w in weights.items()}


if __name__ == "__main__":
    # Illustrative example (generic thresholds)
    regime = detect_regime(
        price=720.0, sma200=680.0, sma_slope_positive=True,
        breadth=0.75, vol_annualized=0.14, short_term_drawdown=-0.03,
        vol_bear_threshold=0.22, vol_crisis_threshold=0.30,
        breadth_riskon=0.60, breadth_riskoff=0.35,
    )
    print("Regime:", regime)  # -> RISKON

    vols = {"QQQ": 0.22, "IWM": 0.21, "DBC": 0.14}
    weights = inverse_volatility_weights(vols)
    print("Risk-parity weights:", {k: round(v, 3) for k, v in weights.items()})
