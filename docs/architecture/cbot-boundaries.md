# cBot Runtime Boundaries

## cBot-enforced controls

- sizing
- stop-loss placement
- max open risk
- trading window checks
- instrument allowlist
- kill switch hooks

## External-only capabilities

- LLM reasoning
- analytics
- journal views
- Discord messaging
- tweet drafting
- approvals
- simulator projections
- tweet publish

## Forbidden behavior

- External services must never directly decide live orders.

## Headless-safe behavior

- No UI APIs.
- No message boxes.
- No chart-shot dependencies.
- No assumption of outbound HTTP from the bot.
