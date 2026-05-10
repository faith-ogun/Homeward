# Homeward — Demo Animations

Remotion compositions for the cutaway animations in the demo video.
Each `<Composition>` produces an MP4 you can drop into iMovie alongside
the screen recording and voice-over.

## What's here

| Composition | Duration | What it shows |
|---|---|---|
| `StatCard1` | 5.0s (150 frames @ 30 fps) | "67%" of surgery is now outpatient or short-stay. AHRQ HCUP, 2017. |
| `StatCard2` | 5.5s (165 frames @ 30 fps) | "3rd" leading cause of death worldwide is post-operative complication. Bar chart. Nepogodiev et al., Lancet 2019. |
| `StatCard3` | 6.0s (180 frames @ 30 fps) | Animated DNA double-helix + "99%" of people carry an actionable PGx variant. PREPARE study, Lancet 2023. |
| `SpectrumCard` | 6.0s (180 frames @ 30 fps) | CYP2D6 spectrum: poor metabolizer (greyed enzyme, no morphine) ↔ ultra-rapid metabolizer (glowing red enzyme, toxicity risk). |
| `PatientInsetCard` | 3.0s (90 frames @ 30 fps) | Top-right corner pill: "Patient 001 · Synthetic FHIR bundle · No PHI". Designed as PIP overlay over the live workspace. |
| `PipelineCutaway` | 5.0s (150 frames @ 30 fps) | Five nodes lighting up in sequence: FHIR Fetch → Discharge → PGx Review → Recovery → Escalation. Ends on AMBER outcome badge. |
| `CompareCard` | 5.0s (150 frames @ 30 fps) | Side-by-side: "Generic recovery agent" (escalates without knowing why) vs "Homeward" (CYP2D6 *4/*4, codeine inert, oxycodone alternative drafted). |
| `SafetyPanel` | 5.0s (150 frames @ 30 fps) | Three guardrails as icon cards: synthetic data only, CPIC-cited evidence, clinician approves. Closes on "HIPAA- and GDPR-compatible by construction." |
| `FinalCard` | 5.0s (150 frames @ 30 fps) | Closing card: Homeward wordmark, "Bringing the post-surgical blind spot under one roof.", standards row (A2A · MCP · FHIR · SHARP), live URL pill. |

Resolution: 1920×1080. Colours match the live landing page palette
(cream / forest ink / accent green).

## Run it

```bash
cd demo
npm install
npm start
```

That opens **Remotion Studio** in your browser at
`http://localhost:3000`. You can scrub the timeline, edit any `.tsx`
file in `src/`, and the preview updates immediately.

## Render to MP4

```bash
npm run render:stat1     # → out/stat-card-1.mp4
npm run render:stat2     # → out/stat-card-2.mp4
npm run render:stat3     # → out/stat-card-3.mp4
npm run render:spectrum  # → out/spectrum.mp4
npm run render:patient   # → out/patient-inset.mp4
npm run render:pipeline  # → out/pipeline.mp4
npm run render:compare   # → out/compare.mp4
npm run render:safety    # → out/safety.mp4
npm run render:final     # → out/final.mp4
npm run render:all       # all nine
```

The first render builds Chromium for off-screen rendering and takes
~30s. Subsequent renders are fast.

## File map

```
demo/
├── package.json            Remotion + React deps
├── tsconfig.json           TS config
├── remotion.config.ts      MP4 output preferences
├── README.md               This file
└── src/
    ├── index.ts            Remotion entry — registers the root
    ├── Root.tsx            Lists every <Composition>
    ├── theme.ts             Colour + font palette (matches landing page)
    ├── StatCard1.tsx        "67%" stat card (outpatient surgery)
    ├── StatCard2.tsx        "3rd leading cause" stat card (post-op deaths)
    ├── StatCard3.tsx        "99%" stat card with animated DNA helix (PGx)
    ├── SpectrumCard.tsx     CYP2D6 spectrum: poor metabolizer ↔ ultra-rapid
    ├── PatientInsetCard.tsx Corner pill: "Patient 001 · Synthetic · No PHI"
    ├── PipelineCutaway.tsx  Five nodes lighting up + AMBER outcome
    ├── CompareCard.tsx      Generic agent vs Homeward, side by side
    ├── SafetyPanel.tsx      Three guardrails: synthetic / CPIC / clinician
    └── FinalCard.tsx        Closing card: wordmark, standards, live URL
```

## Editing

Each stat card is a single React component. Animations use
Remotion's `useCurrentFrame()`, `interpolate()`, and `spring()`.
The "beats" comment block at the top of each component lists what
happens at which frame — change those numbers to retime.

To add a new stat card (e.g. the "99% PGx variant" one), copy
`StatCard1.tsx`, rename the component, and add a `<Composition>` in
`Root.tsx`.

## Why Remotion?

Same reasons you'd reach for it on any other project:
- The animations are code, so they live in git, diff cleanly, and
  re-render the same every time.
- Frame-accurate timing — no nudging keyframes by hand in iMovie.
- Re-skinning is a theme.ts edit, not 8 manual passes.
- Free for individuals (their license terms cover this use case).
