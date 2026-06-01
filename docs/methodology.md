# Methodology

This document covers the academic basis of the strategy, the signal construction, and — importantly — the version-iteration process that led to the current production version.

---

## Academic foundation

The strategy rests on three well-documented bodies of research:

- **Cross-asset momentum** — Asness, Moskowitz & Pedersen (2013), *"Value and Momentum Everywhere"* (Journal of Finance). Momentum persists across asset classes and 40+ markets.
- **Time-series momentum** — Moskowitz, Ooi & Pedersen (2012), *"Time Series Momentum"* (Journal of Financial Economics).
- **Momentum crash management** — Han, Zhou & Zhu (2016), *"Taming Momentum Crashes"*; Kaminski & Lo (2014), *"When do stop-loss rules stop losses?"* — informing why position-level stops are *avoided* in favor of portfolio-level regime and drawdown controls.

---

## Signal construction

### Cross-sectional momentum (CS)

Relative performance rank of an asset versus the rest of the universe:

```
CS_i = rank(12m_return_i) / N − 0.5
```

Range −0.5 (worst) to +0.5 (best).

### Time-series momentum (TS)

Absolute performance, triple lookback, volatility-normalized:

```
raw = 0.20 × return_1m + 0.40 × return_3m + 0.40 × return_12m
TS  = raw / volatility_60d
```

A preliminary filter excludes assets with a sharp recent decline (1-month return below threshold) or trading below their moving averages.

### Combined score

```
Combined = 0.50 × CS + 0.50 × TS
```

Only assets with a positive combined score are eligible. The top 3 are selected, then passed through a correlation filter (reject if correlation > 0.85 with an already-selected asset).

---

## Version iteration — and why rigor matters

A core part of this project is the disciplined rejection of variants that did not improve risk-adjusted performance. This is the opposite of curve-fitting: when a modification failed to help, it was abandoned, even when it was more "sophisticated."

| Version | Change | Result | Decision |
|---|---|---|---|
| **v10.6.1** | Base (hard cap 95%, daily crisis check, trailing DD) | CAGR 12.46% / DD −17.1% / Sharpe 0.633 / **Calmar 0.729** | **SELECTED** |
| v10.6 Patched | Predecessor | CAGR 13.62% / DD −20.6% / Calmar 0.661 | Rejected (worse Calmar) |
| v10.6.2 | Extended universe (+EEM, PDBC, IEF) | CAGR 11.55% / Sharpe 0.585 | Rejected (worse) |
| v10.6.4 | Extended universe + TOP_N=4 | CAGR 11.23% / DD −23.2% | Rejected (worst) |
| v10.7 | + macro overlays (VIX, HYG, DXY, yields) | CAGR 11.23% / Sharpe 0.586 | Rejected (no improvement) |
| v11.1 | + multi-agent LLM layer | DD −28.5% / 4 buying-power errors | Rejected (unstable, non-deterministic) |

**Key lesson demonstrated:** more complexity ≠ better performance. The cleanest version with the best Calmar ratio won. Adding assets, increasing concentration, layering macro signals, and adding LLM agents all *degraded* risk-adjusted performance and were rejected on objective evidence.

This also reflects a deliberate position on LLMs in trading: no tier-1 systematic fund uses LLMs for core position decisions, due to non-determinism and lack of auditability. LLMs belong in auxiliary tasks (parsing filings, sentiment, code), not in the decision loop — a view validated by the v11.1 results.

---

## Why low frequency

The strategy averages ~3 trades per month. This is deliberate:

- The momentum signal (252/63/21-day lookbacks) develops over weeks and months. It barely changes day-to-day.
- Trading daily would multiply transaction costs ~20× while capturing mostly noise.
- This matches real systematic momentum funds: AQR Managed Futures, Winton, and Man AHL rebalance monthly; Bridgewater All-Weather quarterly. High-frequency rebalancing belongs to a different strategy class (statistical arbitrage, market making).

---

## Known limitations

The strategy does **not**:
- Short, use leverage, or trade options
- Use intraday timing (decisions are at most daily)
- Use news/sentiment/NLP signals
- Apply position-level stop-losses (portfolio-level controls instead)

It may underperform in:
- Sharp V-shaped recoveries (re-entry lag)
- Choppy, prolonged NEUTRAL markets (under-deployment)
- Pure equity bull runs (the defensive sleeve and cash drag on raw return — by design, this is the cost of downside protection)

The strategy is designed to deliver a strong **risk-adjusted** profile, not to beat a pure equity index in raw return during bull markets. Its value shows in drawdown control: backtested max drawdown −17.1% vs SPY's −33.8% (2020).
