# Operator Lifecycle Guide

This guide is for a non-technical operator who wants to create, review, backtest, evaluate, and promote strategies without working directly in the repo architecture.

## Create

Start in the operator app.

Enter two kinds of information:

1. a plain-English strategy brief
2. a safe config form

The strategy brief should explain:

- what the strategy is trying to do
- what signals it looks for
- how trades should exit
- how risk should be handled

The safe config form should capture the operator-controlled settings such as symbol, timeframe, session filter, risk per trade, and promotion target.

At this stage, the operator does not need to edit manifests, runtime files, or orchestration modules.

## Review

After the brief and safe config are submitted, the system generates a strategy draft.

The operator reviews:

- a plain-English summary of the strategy
- the generated draft code only if needed
- a structured checklist that confirms the strategy is understood

The checklist is the guardrail. The operator must confirm the entry rule, exit rule, symbol, timeframe, session, risk, stop/take-profit, overtrading risk, and backtest readiness before anything can move forward.

If any checklist item is incomplete, the backtest step stays blocked.

## Backtest

Once review is complete, the app prepares the backtest request for the operator.

The operator should see:

- a human-readable message that the backtest is ready
- the generated command needed for the backtest pipeline
- the manifest path used by the system

The operator should not need to author the manifest by hand.

This stage is intended to hide Docker and repo internals as much as possible while still giving a traceable run request.

## Evaluate

After a run is available, the operator uses the evaluation stage to understand what happened.

The system should summarize:

- the run identifier
- journal-style explanation of the run
- core metrics such as Sharpe ratio and drawdown
- whether prop-style limits were breached
- the current promotion status

This stage is for human understanding, not raw artifact inspection.

## Promote

Promotion remains approval-gated.

The operator can see whether a strategy is blocked, awaiting approval, paper-eligible, or live-eligible, but promotion should not bypass the repo’s approval rules.

The intended order remains:

1. compile success
2. backtest success
3. simulator pass
4. paper approval
5. live approval

The first release of this operator workflow is meant to guide the lifecycle, not to automate live deployment.

## Related technical references

Technical users can still refer to:

- `README.md`
- `docs/runbooks/ctrader-cli-environment.md`
- `docs/runbooks/ctrader-backtest-smoke.md`
- `docs/runbooks/promotion-gates.md`

The operator should not need those documents for normal use of the guided workflow.
