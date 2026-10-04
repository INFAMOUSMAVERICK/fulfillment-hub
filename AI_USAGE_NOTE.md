# AI Usage Note

I used an AI assistant during development as a coding and product-design copilot.

## How I used AI

- Converted the written fulfillment scenario into a small set of operational workflows and states.
- Generated an initial Streamlit application structure and sample fulfillment data.
- Used AI to review edge cases around inventory availability, priority orders, staging, and courier exceptions.
- Used AI to draft the README and demo walkthrough, then edited the content to match the actual prototype.

## Where I changed an AI suggestion

### 1. Avoiding an over-engineered workflow
The initial direction could have become a full warehouse-management system with many screens and fields. I simplified it to a status-driven operations board, inventory verification view, exception inbox, and single-order lookup. This better fits the assignment's request for a simple application and the warehouse team's limited comfort with technology.

### 2. Treating exceptions as first-class workflow items
Rather than leaving problems as free-text notes, I made exceptions a separate queue with an ID, severity, target time, and resolution status. This was a deliberate product decision because the scenario specifically says problems are handled informally and are easy to forget.

AI was therefore used to accelerate implementation and challenge the design, while the final scope and workflow decisions were reviewed and changed by me based on the scenario.
