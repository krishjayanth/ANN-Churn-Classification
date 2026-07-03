# Product

## Register

product

## Users

Recruiters and portfolio viewers skimming this project to judge the author's ML and engineering skills. They arrive cold, spend a minute or two, and should immediately understand what the model does, feed it a customer profile, and see a credible prediction. Secondary: the author and learning peers revisiting the project.

## Product Purpose

An interactive front end for a Keras neural network that predicts bank-customer churn. The app collects a customer profile (demographics, financials, relationship with the bank), runs it through the trained pipeline (encoders → scaler → model), and returns a churn probability with a clear likely-to-churn / likely-to-stay verdict. Success: a first-time visitor gets from landing to a prediction they understand in under a minute, and the app reads as a finished tool rather than a class exercise.

## Brand Personality

Trustworthy, calm, precise. The register of a quiet internal banking tool: restrained color, clear numbers, generous whitespace, nothing performative. Confidence comes from clarity and correctness, not visual noise.

## Anti-references

- Generic AI-generated UI: purple/blue gradients on everything, glassmorphism, glow effects, gradient text, bouncing/wiggling animation.
- Uppercase tracked eyebrow labels above every section; hero-metric templates; nested cards; side-stripe accent borders.
- Emoji as decoration in headings, labels, or buttons (explicitly removed by the owner; keep it that way).
- Hackathon-demo energy in general — anything that makes a viewer think "template" instead of "tool".

## Design Principles

1. **The prediction is the product.** The probability and verdict are the visual climax of the page; everything else supports getting there.
2. **One glance to understand.** A cold visitor should know what the app does and how to use it without instructions.
3. **Legible before beautiful.** Contrast, readable sizes, and clear labels are never traded for style.
4. **Color means something.** Color is reserved for meaning — the risk verdict and the primary action — never decoration.
5. **Restraint signals competence.** Fewer, better-considered elements; whitespace and hierarchy over ornament.

## Accessibility & Inclusion

WCAG AA as the working target: ≥4.5:1 contrast for body text (≥3:1 for large text), visible focus states, labels on every input, and respect for `prefers-reduced-motion`. Verdict states must not rely on color alone (red/green pairs with explicit "Likely to churn" / "Likely to stay" wording).
