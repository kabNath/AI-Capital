# Live Tracking — Paper Trading

The strategy was deployed in **live paper trading on QuantConnect on May 1, 2026**, at $1,000,000 simulated capital. The purpose is to validate the backtest out-of-sample, on data the model has never seen, with realistic execution.

> Why paper trading and not real capital? As a PhD student, deploying small real capital would incur transaction-cost drag (2–6% annually on <$25K) that distorts the strategy's true behavior. Paper trading at $1M produces a clean, representative track record that matches the backtest's capital base — far more meaningful for validation than a friction-distorted small live account.

---

## Month 1 — May 2026

| Metric | Value |
|---|---|
| Starting capital | $1,000,000 |
| Ending capital | $1,035,141 |
| Monthly return | +2.84% |
| Total return | +3.51% |
| Max drawdown | −0.2% |
| Regime (end of month) | RISKON |
| Regime changes | 1 (NEUTRAL → RISKON, Apr 30) |
| Rebalances | 2 (warmup + initial) |
| Manual interventions | **0** |

**End-of-month positions:**

| Asset | Weight |
|---|---|
| QQQ | 28.9% |
| IWM | 27.6% |
| DBC | 21.1% |
| Cash | ~22.4% |

---

## Weekly heartbeat progression

The system sends an automated weekly heartbeat. Month 1 progression:

| Date | Capital | Total return | Drawdown | Regime |
|---|---|---|---|---|
| May 1 | $1,007,807 | +0.78% | −0.04% | RISKON |
| May 8 | $1,022,656 | +2.27% | −0.06% | RISKON |
| May 15 | $1,024,990 | +2.50% | −0.78% | RISKON |
| May 22 | $1,031,980 | +3.20% | −0.11% | RISKON |
| May 29 | $1,034,492 | +3.45% | −0.26% | RISKON |

The weekly returns (+1.49%, +0.23%, +0.70%, +0.25%) show a realistic distribution — one strong week followed by normal consolidation — rather than a suspicious monotonic climb.

---

## Honest assessment

**What this month proves:**
- The system runs stably in production (29 days uptime, 0 errors, 0 anomalies)
- Execution matches design (3 trades at deployment, then 0 — as expected for a low-frequency strategy)
- The monitoring infrastructure works (heartbeats, recap, regime tracking)
- Operational discipline held (zero manual intervention)

**What this month does NOT prove:**
- Nothing about long-term performance. One month is statistical noise.
- The +2.84% return is partly favorable timing (deployed into a bull market) and cannot be extrapolated.
- The strategy has not yet experienced a real market stress event live (no CRISIS triggered).

Meaningful validation requires 12–24+ months including at least one significant drawdown. This is month 1 of that process — roughly 8% of the path to a one-year track record.

---

## Monitoring infrastructure

The live deployment includes automated alerting:

- **Rebalance alerts** — full position report on each monthly rebalance
- **CRISIS alerts** — immediate notification if the kill-switch triggers
- **Weekly heartbeat** — confirms the system is alive, reports status
- **Monthly recap** — performance summary vs backtest reference
- **Anomaly detection** — alerts if drawdown exceeds −15% (watch) or −22% (critical, beyond backtest)
- **Regime history tracking** — logs every regime transition

This institutional-style monitoring is part of what the project demonstrates: not just a strategy, but an operated system.
