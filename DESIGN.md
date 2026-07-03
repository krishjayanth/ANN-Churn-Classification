---
name: Customer Churn Prediction
description: A calm, precise Streamlit front end for a churn-prediction neural network
colors:
  ledger-navy: "#1e3a8a"
  ledger-navy-deep: "#172f70"
  churn-tint: "#fdeaea"
  churn-ink: "#7f1d1d"
  churn-strong: "#b91c1c"
  stay-tint: "#e5f4ea"
  stay-ink: "#14532d"
  stay-strong: "#15803d"
  borderline-tint: "#fbeecb"
  borderline-ink: "#854d0e"
  borderline-strong: "#b45309"
  surface: "#ffffff"
  ink: "#31333f"
  ink-muted: "#4a4d5c"
  meter-track: "rgba(0,0,0,0.1)"
  placeholder-surface: "#f4f5f7"
  placeholder-border: "#e3e5ea"
typography:
  display:
    fontFamily: "Source Sans Pro, sans-serif"
    fontSize: "3.25rem"
    fontWeight: 700
    lineHeight: 1.1
  title:
    fontFamily: "Source Sans Pro, sans-serif"
    fontSize: "1.3rem"
    fontWeight: 600
    lineHeight: 1.4
  body:
    fontFamily: "Source Sans Pro, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "Source Sans Pro, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.4
rounded:
  sm: "4px"
  md: "8px"
spacing:
  control: "0.7rem 1rem"
  panel: "1.5rem 1.75rem"
components:
  button-primary:
    backgroundColor: "{colors.ledger-navy}"
    textColor: "#ffffff"
    rounded: "{rounded.md}"
    padding: "{spacing.control}"
  button-primary-hover:
    backgroundColor: "{colors.ledger-navy-deep}"
    textColor: "#ffffff"
  result-churn:
    backgroundColor: "{colors.churn-tint}"
    textColor: "{colors.churn-ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.panel}"
  result-stay:
    backgroundColor: "{colors.stay-tint}"
    textColor: "{colors.stay-ink}"
    rounded: "{rounded.md}"
    padding: "{spacing.panel}"
---

# Design System: Customer Churn Prediction

## 1. Overview

**Creative North Star: "The Quiet Ledger"**

This interface is a banking record, not a demo. It collects a customer's profile in calm, orderly sections and delivers one unambiguous verdict: likely to churn, or likely to stay. Every visual decision serves that single output. Surfaces are flat white, type is one well-tuned sans in a few deliberate sizes, and color appears only when it carries meaning — navy for the one action on the page, red or green for the verdict itself.

The system explicitly rejects the generated-UI vocabulary named in PRODUCT.md: purple/blue gradients, glassmorphism, glow effects, gradient text, eyebrow labels, hero-metric templates, nested cards, and emoji decoration. Confidence here comes from clarity and correctness, not ornament. The app is built on Streamlit; native widgets are used as-is and styled only where the defaults fail the register. Custom CSS is a scalpel, not a theme engine.

**Key Characteristics:**
- Flat, white, tint-based; zero shadows anywhere.
- One accent (Ledger Navy) reserved for the single primary action.
- Red/green verdict tints are the only other color on the page, and they always pair with explicit words.
- One typeface (Source Sans Pro, Streamlit's default) at a tight scale; hierarchy by size and weight, never by decoration.
- Refined and restrained components: nothing calls attention until it carries meaning.

## 2. Colors

A restrained palette: white surface, near-black ink, one navy accent, and two semantic verdict pairs.

### Primary
- **Ledger Navy** (#1e3a8a): The single accent. Used exclusively for the primary action — the Predict Churn button. It appears nowhere else: not on headings, not on labels, not on decoration.
- **Ledger Navy Deep** (#172f70): The hover/pressed shade of Ledger Navy. Its only job is button state feedback.

### Secondary
- **Churn Ink** (#7f1d1d) on **Churn Tint** (#fdeaea): The high-risk verdict pair (churn probability > 55%). Dark red text on a pale red panel — full-contrast, never washed out. **Churn Strong** (#b91c1c) fills the probability meter in this state.
- **Stay Ink** (#14532d) on **Stay Tint** (#e5f4ea): The low-risk verdict pair (churn probability < 45%). **Stay Strong** (#15803d) fills the meter.
- **Borderline Ink** (#854d0e) on **Borderline Tint** (#fbeecb): The uncertain verdict pair, for the 45–55% band around the decision boundary. Muted amber is the real-world convention for "caution / uncertain," and it is deliberately neither red nor green — the model isn't committing, so the color doesn't either. **Borderline Strong** (#b45309) fills the meter. Contrast is 5.9:1, well past AA.

### Neutral
- **Surface** (#ffffff): The page and all input areas. Streamlit's default light theme, kept deliberately.
- **Ink** (#31333f): All headings, body text, and labels (Streamlit's default text color).
- **Ink Muted** (#4a4d5c): Secondary text in the resting-state placeholder only — a darker step of ink, never a low-contrast gray (≥7:1 on the placeholder surface).
- **Meter Track** (rgba(0,0,0,0.1)): The unfilled portion of the probability meter — a transparency of ink, not a new gray.
- **Placeholder Surface** (#f4f5f7) / **Placeholder Border** (#e3e5ea): The neutral resting-state slot before a prediction. This is the one bordered, tinted-neutral panel; it deliberately reads as "empty, not a result" so it never competes with the verdict tints.

### Named Rules
**The Verdict Rule.** Color exists only to mean something: navy means "the action", red means "churn risk", green means "retention", amber means "uncertain / near the boundary". Any color that decorates rather than signifies is prohibited.

**The Words-First Rule.** The red/green verdict never stands alone. Every colored state carries its meaning in words ("Likely to churn" / "Likely to stay") so the verdict survives color blindness.

## 3. Typography

**Display Font:** Source Sans Pro (with sans-serif fallback) — Streamlit's default
**Body Font:** Source Sans Pro — same family throughout

**Character:** One humanist sans at a tight product scale. Hierarchy comes from a few well-spaced size steps and weight, never from a second face, uppercase tracking, or color.

### Hierarchy
- **Display** (700, 3.25rem, 1.1): The probability figure inside the verdict panel — the visual climax of the page. It is deliberately the largest element anywhere, larger than the page title, because the prediction is the product.
- **Headline** (700, 2rem, 1.2): The page title "Customer Churn Prediction". Streamlit's default `st.title` is compacted from ~2.75rem to 2rem so it stays a confident header without out-sizing the Display figure. Appears once.
- **Title** (600, 1.3rem, 1.4): The verdict heading ("Likely to churn" / "Likely to stay") and Streamlit `st.subheader` section headings, sentence case.
- **Body** (400, 1rem, 1.6): Descriptions and verdict guidance. Prose stays under 75ch (the centered Streamlit column enforces this).
- **Label** (400, 0.875rem, 1.4): Streamlit's native widget labels. Sentence case, never uppercase, never letter-spaced.

### Named Rules
**The Sentence-Case Rule.** Every heading, label, and button is sentence case. Uppercase tracked labels are the eyebrow tell named in PRODUCT.md and are forbidden.

## 4. Elevation

The system is flat and tint-based. There are no shadows anywhere — not on the button, not on the verdict panel, not on hover. Depth is conveyed exactly two ways: tinted background panels (the verdict result) and Streamlit's native dividers between sections. If a future overlay genuinely needs separation, solve it with a border or a tint before reaching for a shadow.

### Named Rules
**The Flat Ledger Rule.** No `box-shadow`, no glow, no blur, ever. If an element needs to stand apart, give it a tinted background or a 1px border.

## 5. Components

Refined and restrained: quiet defaults, minimal states, nothing calls attention until it carries meaning.

### Buttons
- **Shape:** Gently rounded (8px radius), full column width.
- **Primary:** Ledger Navy (#1e3a8a) background, white text, 600 weight, 0.7rem 1rem padding. There is exactly one primary button per page.
- **Hover:** Background deepens to Ledger Navy Deep (#172f70). No lift, no glow, no transform.
- **Secondary:** Does not exist. The page has one action; a second button style is a design smell.

### Cards / Containers
- **Verdict panel** (the result container): 8px radius, verdict tint background (churn #fdeaea, stay #e5f4ea, or borderline #fbeecb), 1.5rem 1.75rem internal padding, no border, no shadow. Text inside uses the matching ink color at full contrast — never gray on tint. It fades in (opacity + 6px rise, 240ms ease-out) when it arrives, since a result appearing is a state change; the animation is disabled under `prefers-reduced-motion`. The verdict has three zones by churn probability: stay (<45%), borderline (45–55%), churn (>55%) — the borderline band keeps a near-coin-flip from posing as a confident red/green result.
- **Resting-state placeholder:** Before a prediction is run, the same slot holds a neutral placeholder — Placeholder Surface (#f4f5f7) with a 1px Placeholder Border (#e3e5ea), same 8px radius and padding as the verdict panel, plus an empty meter track echoing the result's shape. It reads "your prediction will appear here" so the payoff is signalled before interaction. The border and neutral fill are what distinguish it from a real verdict; results are borderless tinted panels.
- Nested containers are prohibited. Each panel contains text and the meter, nothing boxed.

### Inputs / Fields
- **Style:** Streamlit-native widgets (selectbox, slider, number input, toggle), unmodified. Familiarity is the point; custom form controls are a product ban.
- **Accent:** Native interactive controls (slider fill, toggle-on, focus rings) carry Ledger Navy (#1e3a8a) as their interaction accent, set via `theme.primaryColor`. This is the same "navy = the action" role extended to the controls the user acts through — not decoration.
- **Layout:** Grouped into three labeled sections (profile / financials / relationship) using `st.subheader` and 2–3 column rows. Every input has a visible label and a sensible default.
- **Booleans:** Toggles with plain-language labels ("Has Credit Card"), never 0/1 selectboxes.

### Theme (source of truth)
The light "Quiet Ledger" theme is pinned in `.streamlit/config.toml` (`base="light"`, `backgroundColor="#ffffff"`, `primaryColor="#1e3a8a"`, `textColor="#31333f"`). This is mandatory: without it Streamlit inherits the host's dark-mode preference and renders the whole palette on near-black with a red accent, which breaks the entire system. The config is the theme's source of truth; the CSS block only styles the button and the verdict panel.

### Probability Meter (signature component)
A plain horizontal bar inside the verdict panel: 10px tall, 4px radius, rgba(0,0,0,0.1) track, filled by Churn Strong (#b91c1c) or Stay Strong (#15803d) to the predicted percentage. It restates the displayed number visually — it never replaces it.

## 6. Do's and Don'ts

### Do:
- **Do** reserve Ledger Navy (#1e3a8a) for the primary action and nothing else.
- **Do** pair every colored verdict state with explicit words ("Likely to churn" / "Likely to stay").
- **Do** keep dark ink on tinted panels (#7f1d1d on #fdeaea, #14532d on #e5f4ea) — ≥4.5:1 contrast, always.
- **Do** use Streamlit-native widgets as-is; style with custom CSS only when a default fails the register.
- **Do** keep radii at 8px for containers and buttons, 4px for the meter. Nothing rounder.

### Don't:
- **Don't** use purple/blue gradients, glassmorphism, glow effects, or gradient text — the "generic AI-generated UI" anti-references named in PRODUCT.md.
- **Don't** add uppercase tracked eyebrow labels, hero-metric templates, nested cards, or side-stripe accent borders (`border-left` > 1px as a colored stripe).
- **Don't** use emoji in headings, labels, or buttons — explicitly removed by the owner; keep it that way.
- **Don't** add shadows, lifts, or hover transforms. The Flat Ledger Rule has no exceptions.
- **Don't** animate for decoration. Motion may only convey state (e.g. the spinner during prediction), and anything added must respect `prefers-reduced-motion`.
- **Don't** let any text fall below 4.5:1 contrast, including text on the verdict tints — no gray-on-color, ever.
