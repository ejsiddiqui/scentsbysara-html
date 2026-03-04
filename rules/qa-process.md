# QA Pass Rulebook and Requirements

QA is not to be relegated to an afterthought. It is an integrated, unskippable process layer built directly into implementation velocity tracking.

## 1. The 3-Pass Verification Method

No file can be marked "Completed" in `task.md` without explicitly clearing these three cycles. If a developer says a page is done without proving these passes, the PR is rejected.

### Pass 1: The Literal Audit
- Overlay the built site atop the original `.png` asset (`e.g., home-page.png`).
- Validate font weights, vertical padding block sizes, button dimensions, and left/right alignments.
- **Reporting:** Any variance found must be immediately corrected using CSS architecture tokens, not one-off hardcoded overrides.

### Pass 2: The Responsive Integrity Pass
- Shrink the viewport to `1024px`, `768px`, and `375px`.
- Verify the header collapses correctly.
- Ensure grid columns shift accurately (4 cols -> 3 cols -> 2 cols).
- Ensure horizontal overflow is entirely neutralized.

### Pass 3: The Code Disciplinary Audit
- Run a `Ctrl+F` against the CSS for bad practices:
  - `margin-left: 23px` -> Revert to `var(--space-lg)` or correct the structural grid gap.
  - `#000` or `#fff` -> Revert to `var(--text-primary)` or `var(--bg-primary)`.
  - `border-radius: 5px` -> Ensure all structural blocks are sharp corners.

## 2. Execution Documentation Requirements

When documenting a QA pass for stakeholder review or the final milestone handover:
- State exact pixel deviations if any remain due to browser rendering (e.g., "+1px text aliasing shift on H1").
- Provide screenshot artifacts of the `1440px` and `375px` views for the specific page.

## 3. Blockers and Fix Iteration
You are not allowed to move on to `shop.html` if `index.html` fails `Pass 1`.
Iteration stops until structural fidelity is locked. Pixel Perfection is the absolute metric of success for this rebuild.
