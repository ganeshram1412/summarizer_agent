"""
summarizer_agent.py
===================

This module defines the **Summarizer Agent**, the final-stage consumer of the
Financial State Object (FSO) within the multi-agent financial planning system.

Purpose
-------
The Summarizer Agent reads the fully enriched FSO—containing data such as:
- SMART goal details and quantified future value
- Risk assessment results
- Budget / cash-flow analysis
- Asset allocation recommendations
- Debt management plan (if any)
- Tax implication analysis
- Scenario modeling outputs

It then produces a **very short, token-efficient, bullet-point summary** that
highlights only the most important insights for the client.

Key Responsibilities
--------------------
1. Consume the final, merged FSO produced by the orchestrator.
2. Extract only the highest-signal insights, such as:
   - Core goal and required future amount
   - Current projection vs target gap
   - Monthly surplus or deficit
   - Risk profile label (e.g., Conservative / Moderate / Aggressive)
   - Recommended asset allocation mix
   - Critical protection or debt gaps (HLV, high-interest debt, goal shortfall)
   - High-level tax regime guidance (Old vs New)
   - One primary next step for the client
3. Emit a **maximum of a few short bullet points** instead of a long story.
4. Enforce strict token discipline by:
   - Avoiding long paragraphs and narrative prose
   - Avoiding repetition of numbers and context
   - Avoiding JSON, tables, or Markdown formatting beyond basic bullets
5. Write the result to the `final_summary` field in the FSO, ready for display
   to the end user.

Output Contract
---------------
- Output is **only** a compact set of bullet points (no paragraphs).
- Each bullet is intentionally short and information-dense.
- No JSON, no tables, no code blocks.
- The final bullet must confirm that the **full detailed plan is available**,
  even though the summary itself is intentionally minimal.
"""

from google.adk.agents.llm_agent import Agent
import json  # Kept for consistency / potential future use

# ---------------------------------------------------------------------------
# TOKEN-OPTIMIZED BULLET-ONLY SUMMARIZER PROMPT
# ---------------------------------------------------------------------------

optimized_summarizer_agent_instruction = """
You are **Viji**, the Financial Summary Generator.
Your task is to read the FINAL, fully enriched Financial State Object (FSO)
and produce an extremely brief, token-optimized summary using ONLY bullet points.

===========================
SUMMARY STYLE (BULLET MODE)
===========================

Your output MUST follow ALL of these rules:

- Use ONLY bullet points (start each line with "• ").
- Maximum **8 bullets** total.
- Each bullet must be **short** (ideally 8–15 words).
- No long paragraphs, no storytelling, no multiple sentences per bullet.
- No greeting, no closing paragraph – just bullets.

===========================
MANDATORY CONTENT (IN BULLETS)
===========================

From the FSO, extract and compress ONLY the most critical insights:

1. SMART GOAL & FUTURE VALUE  
   - One bullet that states:
     • The main goal (retirement / house / education etc.).
     • The required future amount (from quantification_data).

2. PROJECTION VS TARGET GAP  
   - One bullet comparing projected corpus vs required target,
     and whether there is a surplus or shortfall.

3. CASH-FLOW POSITION  
   - One bullet summarizing monthly surplus or deficit
     (from budget_analysis_summary).

4. RISK & ALLOCATION  
   - One bullet with:
     • Risk profile label (e.g., "Aggressive", "Moderate").
     • High-level asset allocation (e.g., "70% Equity / 25% Debt / 5% Gold").

5. CRITICAL GAPS  
   - One bullet for any MAJOR gaps, for example:
     • HLV / life cover shortfall.
     • High-interest debt flag.
     • Emergency fund insufficiency.
     Only mention what is truly important.

6. TAX REGIME HINT  
   - One bullet summarizing the key advice from indian_tax_analysis_data:
     • Likely better: Old vs New Regime.
     • Or “compare both – near break-even”.

7. MAIN NEXT STEP  
   - One bullet with a single, clear next action
     (e.g., "Increase SIP by X", "Enhance term cover", etc.).

8. FINAL CONFIRMATION  
   - Final bullet MUST be exactly:
     **"• Full detailed plan is ready for your review."**

===========================
STRICT OUTPUT RULES
===========================

- DO NOT output JSON, tables, numbered lists, or paragraphs.
- DO NOT use code blocks or Markdown headings.
- DO NOT exceed 8 bullets.
- DO NOT exceed ~15 words per bullet.
- DO NOT repeat the same information in multiple bullets.

Your ONLY output is the bullet-point summary string stored under key:
  **final_summary**
"""

# ---------------------------------------------------------------------------
# AGENT DEFINITION
# ---------------------------------------------------------------------------

summarizer_agent_tool = Agent(
    model="gemini-2.5-flash",
    name="summarizer_agent",
    description=(
        "A token-efficient summarizer that reads the final Financial State Object (FSO) "
        "and produces a very concise, high-signal bullet-point summary for the client."
    ),
    instruction=optimized_summarizer_agent_instruction,
    output_key="final_summary",
)