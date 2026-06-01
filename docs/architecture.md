# Architecture

This document describes how AI Capital makes decisions. The system operates at four distinct frequencies, each with a specific purpose.

---

## Decision frequencies

### Monthly — Full rebalance (1st trading day, 30 min after open)

The complete portfolio reconstruction:

1. **Detect regime** — classify the market into one of four states
2. **Score every risk asset** — cross-sectional + time-series momentum
3. **Select TOP 3** — highest combined score, subject to a correlation filter
4. **Risk-parity weighting** — inverse volatility
5. **Apply regime multipliers** — scale risk vs defensive exposure
6. **Volatility targeting** — scale toward 10% portfolio volatility
7. **Hard cap** — limit total exposure to 95%
8. **Execute** — smallest to largest position (frees cash before large orders)

### Daily — CRISIS detection (after open)

A continuous safety check, independent of the monthly cycle:

- **CheckCrisis:** if SPY 21-day annualized volatility > 30% **and** market breadth ≤ 35% → immediately liquidate risk assets and route 95% to BIL (Treasury bills).
- **CheckCrisisExit:** if already in CRISIS and conditions normalize (vol < 22%, breadth > 35%) → progressively re-enter via a fresh rebalance.

This means the system never waits a full month to react to a crash. Protection is daily.

### Weekly — Opportunity scan (Monday)

Captures strong momentum that emerges *between* monthly rebalances. If an asset not currently held shows exceptional combined score (cross-sectional > 0.35 and time-series > 3.0), it is added at a 15% weight.

### Mon / Wed / Fri — Trailing drawdown monitor

Tracks drawdown from the portfolio's rolling 90-day peak. If, while in RISKON, the drawdown from peak exceeds −8%, the regime is forced to NEUTRAL (reduced exposure). Recovery above −4% resets it.

This captures fast corrections *before* the lagging 21-day volatility signal would react.

---

## Regime detection

Regime is determined by a score built from six indicators:

| Indicator | Measure | Effect |
|---|---|---|
| 1 | SPY price vs SMA200 | +1 above / −1 below |
| 2 | SMA200 slope | +1 rising / −1 falling |
| 3 | Market breadth (4 equity ETFs in uptrend) | +1 if ≥60% / −1 if ≤35% |
| 4 | SPY 21-day annualized volatility | +1 if low / −1 if elevated / −2 if extreme |
| 5 | 63-day short-term drawdown | −1 if < −10% |

**Decision logic:**
- If volatility > 30% **and** breadth ≤ 35% → **CRISIS** (override)
- Score ≥ 2 → **RISKON**
- Score ≤ −1 → **RISKOFF**
- Otherwise → **NEUTRAL**

---

## Portfolio construction pipeline

```
Selected assets (TOP 3)
        │
        ▼
[1] Inverse-volatility weights        w_i = (1/vol_i) / Σ(1/vol_j)
        │
        ▼
[2] Per-asset caps                    35% standard, 8% BTC, 50% BIL
        │   (iterative redistribution of excess)
        ▼
[3] Regime multipliers                RISKON 100% / NEUTRAL 55% / RISKOFF 15% / CRISIS 0%
        │
        ▼
[4] Volatility targeting              scale toward 10% portfolio vol (no leverage)
        │
        ▼
[5] Hard cap                          total exposure ≤ 95%
        │
        ▼
Final target weights → execute (smallest to largest)
```

---

## Protection mechanisms

The strategy has three independent layers of capital protection:

1. **CRISIS kill-switch (daily)** — full defensive rotation on extreme conditions. BIL earns ~4% Treasury yield during protection rather than sitting in dead cash.

2. **Trailing drawdown (3×/week)** — portfolio-level, not position-level. Reduces exposure on an 8% drawdown from peak, more responsive than the lagging volatility signal.

3. **Hard exposure cap (every rebalance)** — total exposure never exceeds 95%, structurally eliminating "insufficient buying power" errors.

---

## Design philosophy

- **Long-only, no leverage** — exposure capped at 95%, no shorting, no derivatives.
- **Low frequency** — ~3 trades/month on average. The momentum signal develops over weeks/months; trading more often captures noise, not signal, and incurs unnecessary costs.
- **Cross-asset over single stocks** — scales to high AUM without market impact; explainable to non-technical investors; lower idiosyncratic risk.
- **Capital protection over return maximization** — the goal is a strong risk-adjusted profile (Sharpe, Calmar), not the highest raw CAGR.
