# Backtest Metrics — v10.6.1

**Period:** January 2010 – 2026 (16 years)
**Starting capital:** $1,000,000
**Benchmark:** SPY
**Source:** QuantConnect / LEAN backtest (figures below are exact platform output)

---

## Headline metrics

| Metric | Value |
|---|---|
| Compounding Annual Return (CAGR) | 12.46% |
| Net Profit | +588.23% |
| End Equity | $6,882,266 |
| Max Drawdown | −17.10% |
| Sharpe Ratio | 0.633 |
| Sortino Ratio | 0.67 |
| Calmar Ratio (CAGR / Max DD) | 0.729 |
| PSR (Probabilistic Sharpe Ratio) | 14.36% |

## Risk metrics

| Metric | Value |
|---|---|
| Beta vs SPY | 0.325 |
| Alpha | 0.042 |
| Annual Standard Deviation | 0.111 |
| Annual Variance | 0.012 |
| Information Ratio | −0.123 |
| Treynor Ratio | 0.217 |
| Tracking Error | 0.14 |

## Trade statistics

| Metric | Value |
|---|---|
| Win Rate | 56% |
| Loss Rate | 44% |
| Profit-Loss Ratio | 2.33 |
| Average Win | 1.89% |
| Average Loss | −0.81% |
| Expectancy | 0.883 |
| Total Orders | 595 (~37/year) |
| Portfolio Turnover | 2.42% |
| Total Fees | $595 (~0.05%/year) |
| Drawdown Recovery | 1281 days |
| Buying-power errors | 0 |

---

## Comparison vs SPY (buy & hold)

| Metric | AI Capital v10.6.1 | SPY |
|---|---|---|
| CAGR | 12.46% | ~13.5% |
| Max Drawdown | **−17.1%** | −33.8% (2020) |
| Volatility | **11.1%** | ~17% |
| Sharpe | **0.633** | ~0.55 |
| Beta | **0.325** | 1.00 |

**Interpretation:** AI Capital does not beat SPY in raw return. It delivers a comparable CAGR with roughly **half the drawdown, two-thirds the volatility, and a beta of just 0.325** — a markedly superior risk-adjusted profile. This is the intended outcome of a capital-management strategy: stability and downside protection over raw return maximization.

---

## Robustness

- **0 parameters flagged as overfit** (QuantConnect overfitting detection: "Likely Not Overfit")
- **0 buying-power errors** across 16 years
- Tested across four distinct market regimes: 2008 aftermath, 2017 boom, 2020 COVID crash, 2022 inflation/rate shock
- Selected as best risk-adjusted version (Calmar 0.729) among 6+ tested variants — see [methodology](../docs/methodology.md)
