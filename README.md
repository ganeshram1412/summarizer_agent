# Summarizer Agent — README

## Overview

The **Summarizer Agent** is the final-stage FSO consumer in your multi‑agent financial planning system. Its purpose is to convert the fully enriched **Financial State Object (FSO)** into a warm, human‑readable, motivational narrative for the client.

## Key Responsibilities

- Read and interpret **all components** of the FSO.
- Produce a **personalized** narrative using the user's name and status.
- Synthesize SMART goal, risk profile, asset allocation, budget analysis, scenario projections, debt plan, and tax insights.
- Provide a **flowing story** (no bullet lists, tables, or JSON).
- Output the result under the key `final_summary`.

## Inputs

- A single JSON object representing the **final FSO** with fields such as:
  - `user_name`
  - `smart_goal_data`
  - `quantification_data`
  - `risk_assessment_data`
  - `budget_analysis_summary`
  - `asset_allocation_data`
  - `debt_management_plan` (optional)
  - `indian_tax_analysis_data`
  - `scenario_projection_data`

## Output

- A **continuous narrative summary**.
- No JSON, tables, or bullet points.
- Must be stored in the output key: `final_summary`.

## Narrative Structure

1. Personalized greeting
2. Goal confirmation
3. Cash‑flow clarity
4. Investment strategy interpretation
5. Debt plan explanation (if applicable)
6. Tax opportunities
7. 3–5 opportunity areas
8. Closing reassurance

## Example (Excerpt)

> “Hi Arun, you've done a fantastic job defining your financial path. Your primary goal of building a ₹50‑lakh education fund over the next 12 years is now fully quantified...”

## Integration Notes

Place this agent at the **very end** of your orchestrator pipeline.  
It expects a _final, complete_ FSO.

## License

Apache 2.0
