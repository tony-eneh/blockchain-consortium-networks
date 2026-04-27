// Week-9 progress deck — same design system as scripts/generate_slides_week8.js
// Run: node scripts/generate_slides_week9.js
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Tony Eneh";
pres.title = "Blockchain Consortium Networks SLR — Week 9 Progress";

// ── Color Palette ──
const C = {
  dark:    "0B1D26",
  primary: "0D4F5C",
  accent:  "14B8A6",
  light:   "E8F5F3",
  white:   "FFFFFF",
  text:    "1E293B",
  muted:   "64748B",
  card:    "F0FDFA",
  warn:    "F59E0B",
  done:    "10B981",
  todo:    "94A3B8",
  red:     "EF4444",
  amber:   "F59E0B",
  blue:    "0EA5E9",
};

const FONT_H = "Cambria";
const FONT_B = "Calibri";
const cardShadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.10 });

// ════════════════════════════════════════════════════════════════
// SLIDE 1 — Title
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });

  s.addText("Blockchain Utilization Strategies\nin Institutional Consortium Networks", {
    x: 0.8, y: 0.8, w: 8.4, h: 2.0,
    fontFace: FONT_H, fontSize: 36, color: C.white, bold: true, lineSpacingMultiple: 1.15,
  });

  s.addText("PRISMA 2020 Systematic Review — Week 9 Progress", {
    x: 0.8, y: 2.9, w: 8.4, h: 0.5,
    fontFace: FONT_B, fontSize: 18, color: C.accent, italic: true,
  });

  s.addText([
    { text: "Tony Eneh", options: { bold: true, breakLine: true } },
    { text: "Networked Systems Laboratory (NSL)", options: { breakLine: true } },
    { text: "Kumoh National Institute of Technology (KIT)", options: { breakLine: true } },
    { text: "April 28, 2026" },
  ], {
    x: 0.8, y: 3.7, w: 8.4, h: 1.2,
    fontFace: FONT_B, fontSize: 13, color: C.muted, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 2 — Recap from last week
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Where We Left Off (Week 8)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  const stats = [
    { num: "863", label: "Full-text candidates", color: C.primary, white: true },
    { num: "279", label: "Included  (32.3%)",    color: C.done },
    { num: "584", label: "Excluded  (67.7%)",    color: C.red },
  ];
  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    const fill = st.white ? C.primary : C.card;
    const numCol = st.white ? C.white : st.color;
    const labCol = st.white ? C.light : C.muted;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 1.5, fill: { color: fill }, shadow: cardShadow() });
    if (!st.white) s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 0.07, fill: { color: st.color } });
    s.addText(st.num, {
      x: xx, y: 1.28, w: 2.8, h: 0.7,
      fontFace: FONT_H, fontSize: 40, color: numCol, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: xx, y: 2.05, w: 2.8, h: 0.35,
      fontFace: FONT_B, fontSize: 13, color: labCol, align: "center", margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.0, w: 8.8, h: 2.1, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Open issues going into Week 9", {
    x: 0.8, y: 3.1, w: 8.4, h: 0.4,
    fontFace: FONT_B, fontSize: 16, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "1.  No quality scores yet — every include is treated as equal weight.", options: { breakLine: true } },
    { text: "2.  Agent decisions over 863 papers had zero human spot-check.", options: { breakLine: true } },
    { text: "3.  data_extraction.csv was a 37-column scaffold with bibliographic fields only — Step 6 unstarted.", options: {} },
  ], {
    x: 0.8, y: 3.55, w: 8.4, h: 1.5,
    fontFace: FONT_B, fontSize: 14, color: C.text, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 3 — Timeline weeks 1-9
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Progress Timeline (Weeks 1–9)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  const timeline = [
    { week: "1–2", label: "RQs + PICOC scope",         status: "done" },
    { week: "3–4", label: "PRISMA protocol + search",   status: "done" },
    { week: "5–6", label: "Search + dedup",             status: "done" },
    { week: "7",   label: "Title/abstract screening",   status: "done" },
    { week: "8",   label: "Agent full-text screening",  status: "done" },
    { week: "9",   label: "Quality + extraction bootstrap", status: "current" },
  ];

  s.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: 1.3, w: 8.4, h: 0.08, fill: { color: C.accent } });

  timeline.forEach((item, i) => {
    const xx = 0.8 + i * (8.4 / (timeline.length - 1));
    const isCurrent = item.status === "current";
    const circleColor = isCurrent ? C.accent : C.done;
    const circleSize = isCurrent ? 0.45 : 0.35;
    const offset = isCurrent ? -0.05 : 0;

    s.addShape(pres.shapes.OVAL, {
      x: xx - circleSize/2, y: 1.34 - circleSize/2 + offset, w: circleSize, h: circleSize,
      fill: { color: circleColor },
    });
    s.addText(item.week, {
      x: xx - 0.9, y: 1.65, w: 1.8, h: 0.3,
      fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, align: "center", margin: 0,
    });
    s.addText(item.label, {
      x: xx - 1.0, y: 1.95, w: 2.0, h: 0.6,
      fontFace: FONT_B, fontSize: 11, color: C.text, align: "center", margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.85, w: 8.8, h: 2.4, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("This Week's Work", {
    x: 0.8, y: 2.95, w: 8.4, h: 0.35,
    fontFace: FONT_B, fontSize: 16, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "1. ", options: { bold: true } },
    { text: "Built a deterministic screening-stage quality rubric (4 dimensions × 0–2) and ran it on the 279 includes.", options: { breakLine: true } },
    { text: "2. ", options: { bold: true } },
    { text: "Generated a stratified spot-check sample (40 rows: 20 includes by tier + 20 excludes by reason) for author audit.", options: { breakLine: true } },
    { text: "3. ", options: { bold: true } },
    { text: "Bootstrapped data_extraction_includes.csv: 279 rows × 37 cols, with abstract-only heuristic seed for 7 fields.", options: { breakLine: true } },
    { text: "4. ", options: { bold: true } },
    { text: "Surfaced first taxonomy signals: 159 IoT/edge, 105 healthcare, 49 Fabric, 32 Ethereum, 12 PBFT.", options: {} },
  ], {
    x: 0.8, y: 3.4, w: 8.4, h: 1.7,
    fontFace: FONT_B, fontSize: 14, color: C.text, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 4 — Quality rubric (this week's headline)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Quality Rubric — Screening-Stage Tiering", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 26, color: C.primary, bold: true, margin: 0,
  });

  // Left: 4 dimensions
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.05, w: 4.6, h: 4.2, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Four PRISMA-protocol dimensions  (0–2 each, total 0–8)", {
    x: 0.8, y: 1.12, w: 4.4, h: 0.4,
    fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "Construct validity", options: { bold: true, color: C.primary, breakLine: true } },
    { text: "Evaluation vocabulary in title/abstract: throughput, latency, benchmark, prototype, …", options: { fontSize: 11, color: C.muted, breakLine: true } },
    { text: " ", options: { fontSize: 4, breakLine: true } },
    { text: "Internal validity", options: { bold: true, color: C.primary, breakLine: true } },
    { text: "Peer-reviewed venue (IEEE/WoS/Scopus/ACM) + comparison/baseline signal.", options: { fontSize: 11, color: C.muted, breakLine: true } },
    { text: " ", options: { fontSize: 4, breakLine: true } },
    { text: "External validity", options: { bold: true, color: C.primary, breakLine: true } },
    { text: "Institutional / cross-organizational markers: consortium, inter-bank, healthcare, supply chain, …", options: { fontSize: 11, color: C.muted, breakLine: true } },
    { text: " ", options: { fontSize: 4, breakLine: true } },
    { text: "Reproducibility", options: { bold: true, color: C.primary, breakLine: true } },
    { text: "Open-source / GitHub / Zenodo / artifact / replication package signals.", options: { fontSize: 11, color: C.muted } },
  ], {
    x: 0.8, y: 1.55, w: 4.4, h: 3.6,
    fontFace: FONT_B, fontSize: 13, color: C.text, lineSpacingMultiple: 1.25,
  });

  // Right: tier distribution as horizontal bars
  s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 1.05, w: 4.0, h: 4.2, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Tier distribution  (n = 279)", {
    x: 5.6, y: 1.12, w: 3.8, h: 0.4,
    fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, margin: 0,
  });

  const tiers = [
    { tier: "A  (≥6)",  n: 26,  color: C.done },
    { tier: "B  (4–5)", n: 122, color: C.accent },
    { tier: "C  (2–3)", n: 110, color: C.amber },
    { tier: "D  (0–1)", n: 21,  color: C.red },
  ];
  const maxN = 122;
  const barAreaW = 2.4;
  const startY = 1.7;
  const rowH = 0.7;
  tiers.forEach((t, i) => {
    const yy = startY + i * rowH;
    s.addText(t.tier, {
      x: 5.55, y: yy, w: 1.0, h: rowH - 0.1,
      fontFace: FONT_B, fontSize: 13, color: C.text, bold: true, valign: "middle", margin: 0,
    });
    const w = Math.max(0.05, (t.n / maxN) * barAreaW);
    s.addShape(pres.shapes.RECTANGLE, { x: 6.55, y: yy + 0.18, w, h: rowH - 0.45, fill: { color: t.color } });
    s.addText(`${t.n}`, {
      x: 6.55 + w + 0.05, y: yy, w: 0.7, h: rowH - 0.1,
      fontFace: FONT_B, fontSize: 13, color: C.text, bold: true, valign: "middle", margin: 0,
    });
  });
  s.addText("148 of 279 (53%) score B or higher → priority queue for full-text rubric pass.", {
    x: 5.6, y: 4.65, w: 3.8, h: 0.5,
    fontFace: FONT_B, fontSize: 11, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 5 — Spot-check sample
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Author Spot-Check — Stratified Sample (n = 40)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 24, color: C.primary, bold: true, margin: 0,
  });

  // Includes table
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 1.05, w: 4.3, h: 4.0, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Includes  (5 per tier  →  20 rows)", {
    x: 0.8, y: 1.1, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.done, bold: true, margin: 0,
  });
  const incRows = [
    ["Tier", "Population", "Sampled"],
    ["A",  "26",  "5"],
    ["B",  "122", "5"],
    ["C",  "110", "5"],
    ["D",  "21",  "5"],
  ];
  incRows.forEach((row, i) => {
    const yy = 1.55 + i * 0.42;
    const isHeader = i === 0;
    if (isHeader) {
      s.addShape(pres.shapes.RECTANGLE, { x: 0.8, y: yy, w: 4.0, h: 0.4, fill: { color: C.primary } });
    }
    row.forEach((cell, j) => {
      const xx = 0.8 + j * (4.0 / row.length);
      s.addText(cell, {
        x: xx, y: yy, w: 4.0 / row.length, h: 0.4,
        fontFace: FONT_B, fontSize: 12,
        color: isHeader ? C.white : C.text,
        bold: isHeader, align: "center", valign: "middle", margin: 0,
      });
    });
  });
  s.addText("Each tier sampled equally → covers strongest and weakest agent decisions.", {
    x: 0.8, y: 4.4, w: 4.0, h: 0.55,
    fontFace: FONT_B, fontSize: 10.5, color: C.muted, italic: true,
  });

  // Excludes table
  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 1.05, w: 4.3, h: 4.0, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Excludes  (4 per top reason  →  20 rows)", {
    x: 5.3, y: 1.1, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.red, bold: true, margin: 0,
  });
  const excRows = [
    ["Reason code",                          "Pop", "Smp"],
    ["insufficient_fulltext_access",         "281", "4"],
    ["no_full_text_access",                  "210", "4"],
    ["second_pass_likely_exclude",           "48",  "4"],
    ["agent_uncertain_full_text",            "32",  "4"],
    ["no_quantitative_or_reproducible_evi…", "7",   "4"],
  ];
  excRows.forEach((row, i) => {
    const yy = 1.55 + i * 0.42;
    const isHeader = i === 0;
    if (isHeader) {
      s.addShape(pres.shapes.RECTANGLE, { x: 5.3, y: yy, w: 4.0, h: 0.4, fill: { color: C.primary } });
    }
    row.forEach((cell, j) => {
      const widths = [2.4, 0.8, 0.8];
      const offsets = [0, 2.4, 3.2];
      s.addText(cell, {
        x: 5.3 + offsets[j], y: yy, w: widths[j], h: 0.4,
        fontFace: FONT_B, fontSize: j === 0 ? 10 : 11,
        color: isHeader ? C.white : C.text,
        bold: isHeader, align: j === 0 ? "left" : "center", valign: "middle", margin: 0,
      });
    });
  });
  s.addText("Deterministic seed = 20260428. Reviewer fills human_decision column.", {
    x: 5.3, y: 4.4, w: 4.0, h: 0.55,
    fontFace: FONT_B, fontSize: 10.5, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 6 — Extraction bootstrap: domains + platforms
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("First Taxonomy Signals  (abstract-only heuristics, n = 279)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 22, color: C.primary, bold: true, margin: 0,
  });

  // Domain bars (left)
  s.addText("Application domain", {
    x: 0.6, y: 0.95, w: 4.4, h: 0.3,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  const domains = [
    { label: "IoT / edge",               n: 159 },
    { label: "Healthcare",               n: 105 },
    { label: "Supply chain",             n: 69  },
    { label: "Government / public",      n: 58  },
    { label: "Finance / banking",        n: 38  },
    { label: "Identity",                 n: 35  },
    { label: "Education",                n: 32  },
    { label: "Energy / utilities",       n: 21  },
  ];
  const dMax = 159;
  const dBarW = 2.0;
  domains.forEach((r, i) => {
    const yy = 1.3 + i * 0.42;
    s.addText(r.label, {
      x: 0.6, y: yy, w: 1.9, h: 0.36,
      fontFace: FONT_B, fontSize: 11, color: C.text, valign: "middle", margin: 0,
    });
    const w = Math.max(0.05, (r.n / dMax) * dBarW);
    s.addShape(pres.shapes.RECTANGLE, { x: 2.5, y: yy + 0.07, w, h: 0.2, fill: { color: C.accent } });
    s.addText(`${r.n}`, {
      x: 2.5 + w + 0.05, y: yy, w: 0.6, h: 0.36,
      fontFace: FONT_B, fontSize: 11, color: C.text, bold: true, valign: "middle", margin: 0,
    });
  });

  // Platform bars (right)
  s.addText("Platform stack", {
    x: 5.4, y: 0.95, w: 4.0, h: 0.3,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  const platforms = [
    { label: "Hyperledger Fabric", n: 49 },
    { label: "Ethereum",           n: 32 },
    { label: "Corda",              n: 5  },
    { label: "Hyperledger Besu",   n: 4  },
    { label: "Quorum",             n: 3  },
    { label: "Cosmos",             n: 1  },
    { label: "Sawtooth",           n: 1  },
  ];
  const pMax = 49;
  const pBarW = 1.9;
  platforms.forEach((r, i) => {
    const yy = 1.3 + i * 0.42;
    s.addText(r.label, {
      x: 5.4, y: yy, w: 1.9, h: 0.36,
      fontFace: FONT_B, fontSize: 11, color: C.text, valign: "middle", margin: 0,
    });
    const w = Math.max(0.05, (r.n / pMax) * pBarW);
    s.addShape(pres.shapes.RECTANGLE, { x: 7.3, y: yy + 0.07, w, h: 0.2, fill: { color: C.blue } });
    s.addText(`${r.n}`, {
      x: 7.3 + w + 0.05, y: yy, w: 0.6, h: 0.36,
      fontFace: FONT_B, fontSize: 11, color: C.text, bold: true, valign: "middle", margin: 0,
    });
  });

  // Footer card
  s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 4.35, w: 4.0, h: 0.85, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Consensus signal (sparse): PBFT 12, RAFT 6, PoS/PoW 5 each, Tendermint/HotStuff/PoA 1 each.\nMost abstracts elide consensus details — full-text pass needed.", {
    x: 5.55, y: 4.4, w: 3.7, h: 0.75,
    fontFace: FONT_B, fontSize: 10.5, color: C.text, lineSpacingMultiple: 1.3,
  });
  s.addText("Heuristic = abstract regex; reviewer must verify against full text.", {
    x: 0.6, y: 5.1, w: 8.8, h: 0.3,
    fontFace: FONT_B, fontSize: 10, color: C.muted, italic: true, align: "center",
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 7 — Extraction sheet field-fill heatbar
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Data Extraction Bootstrap  (data_extraction_includes.csv)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 22, color: C.primary, bold: true, margin: 0,
  });

  // Three big stat cards
  const stats = [
    { num: "279", label: "Studies in extraction sheet", color: C.done },
    { num: "37",  label: "Extraction columns",          color: C.primary, white: true },
    { num: "504", label: "Auto-filled cell hints",      color: C.accent },
  ];
  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    const fill = st.white ? C.primary : C.card;
    const numCol = st.white ? C.white : st.color;
    const labCol = st.white ? C.light : C.muted;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.05, w: 2.8, h: 1.4, fill: { color: fill }, shadow: cardShadow() });
    if (!st.white) s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.05, w: 2.8, h: 0.07, fill: { color: st.color } });
    s.addText(st.num, {
      x: xx, y: 1.18, w: 2.8, h: 0.65,
      fontFace: FONT_H, fontSize: 36, color: numCol, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: xx, y: 1.85, w: 2.8, h: 0.4,
      fontFace: FONT_B, fontSize: 12, color: labCol, align: "center", margin: 0,
    });
  });

  // Per-field fill bars
  s.addText("Heuristic fill counts per field  (max = 279)", {
    x: 0.6, y: 2.7, w: 9, h: 0.3,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  const fields = [
    { label: "domain",                    n: 251 },
    { label: "smart_contract_support",    n: 92  },
    { label: "platform_stack",            n: 79  },
    { label: "privacy_mechanism",         n: 28  },
    { label: "consensus_strategy",        n: 25  },
    { label: "interoperability_strategy", n: 18  },
    { label: "artifact_code_available",   n: 11  },
  ];
  const fMax = 279;
  const fBarW = 5.5;
  fields.forEach((r, i) => {
    const yy = 3.1 + i * 0.32;
    s.addText(r.label, {
      x: 0.6, y: yy, w: 2.4, h: 0.28,
      fontFace: "Consolas", fontSize: 11, color: C.text, valign: "middle", margin: 0,
    });
    const w = Math.max(0.05, (r.n / fMax) * fBarW);
    s.addShape(pres.shapes.RECTANGLE, { x: 3.0, y: yy + 0.06, w, h: 0.16, fill: { color: C.accent } });
    s.addText(`${r.n}  (${(r.n*100/279).toFixed(0)}%)`, {
      x: 3.0 + w + 0.05, y: yy, w: 1.6, h: 0.28,
      fontFace: FONT_B, fontSize: 10.5, color: C.text, valign: "middle", margin: 0,
    });
  });

  s.addText("All bootstrapped values are prefixed [auto] for reviewer audit; remaining 30 fields require full-text reading.", {
    x: 0.6, y: 5.2, w: 8.8, h: 0.3,
    fontFace: FONT_B, fontSize: 10, color: C.muted, italic: true, align: "center",
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 8 — Progress Tracker
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Progress Tracker", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  const steps = [
    { step: "1",  label: "Research questions (PICOC)",       status: "done" },
    { step: "2",  label: "PRISMA protocol",                  status: "done" },
    { step: "3",  label: "Search strings (PRISMA-S)",        status: "done" },
    { step: "4",  label: "Search execution + dedup",         status: "done" },
    { step: "5a", label: "Title/abstract screening",         status: "done" },
    { step: "5b", label: "Full-text screening (agent)",      status: "done" },
    { step: "6",  label: "Data extraction — bootstrap done", status: "current" },
    { step: "7",  label: "Quality assessment — rubric live", status: "current" },
    { step: "8",  label: "Synthesis + taxonomy",             status: "next" },
  ];

  steps.forEach((item, i) => {
    const yy = 1.05 + i * 0.46;
    const isDone = item.status === "done";
    const isCurrent = item.status === "current";
    const isNext = item.status === "next";

    const circleColor = isDone ? C.done : isCurrent ? C.accent : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.OVAL, { x: 0.7, y: yy + 0.04, w: 0.36, h: 0.36, fill: { color: circleColor } });
    s.addText(item.step, {
      x: 0.7, y: yy + 0.04, w: 0.36, h: 0.36,
      fontFace: FONT_B, fontSize: 10, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });

    s.addText(item.label, {
      x: 1.25, y: yy, w: 6.0, h: 0.42,
      fontFace: FONT_B, fontSize: 13, color: isDone ? C.muted : C.text,
      bold: isCurrent || isNext, valign: "middle", margin: 0,
    });

    const badgeText  = isDone ? "Done" : isCurrent ? "In progress" : isNext ? "Next" : "Upcoming";
    const badgeColor = isDone ? C.done : isCurrent ? C.accent : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: yy + 0.05, w: 1.5, h: 0.32, fill: { color: badgeColor } });
    s.addText(badgeText, {
      x: 7.5, y: yy + 0.05, w: 1.5, h: 0.32,
      fontFace: FONT_B, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });
  });

  s.addText("3 new scripts this week: quality_assessment.py, sample_spotcheck.py, bootstrap_extraction.py.", {
    x: 0.6, y: 5.25, w: 8.8, h: 0.3,
    fontFace: FONT_B, fontSize: 11, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 9 — Next Steps (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.565, w: 10, h: 0.06, fill: { color: C.accent } });

  s.addText("Next Steps (Week 10)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.white, bold: true, margin: 0,
  });

  const nextItems = [
    { num: "01", title: "Full-text rubric pass on tier-A/B (148 papers)",
      desc: "Replace abstract-only construct/internal/external/repro scores with full-text scores; identify tier movers." },
    { num: "02", title: "Complete spot-check audit (40 rows)",
      desc: "Reviewer fills human_decision; compute agreement rate vs agent; document discrepancies in audit report." },
    { num: "03", title: "Procure paywalled full-texts (top of priority)",
      desc: "Target 491 OA-gap candidates through institutional access; re-run review_firstpass_fulltexts.py." },
    { num: "04", title: "Extraction deep-fill on tier-A includes (n = 26)",
      desc: "Manually populate the 30 non-bootstrapped extraction fields; first synthesis tables follow." },
  ];

  nextItems.forEach((item, i) => {
    const yy = 1.15 + i * 1.05;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: yy, w: 8.8, h: 0.85, fill: { color: C.primary }, shadow: cardShadow() });
    s.addText(item.num, {
      x: 0.8, y: yy + 0.1, w: 0.6, h: 0.65,
      fontFace: FONT_H, fontSize: 28, color: C.accent, bold: true, valign: "middle", margin: 0,
    });
    s.addText(item.title, {
      x: 1.6, y: yy + 0.08, w: 7.5, h: 0.35,
      fontFace: FONT_B, fontSize: 15, color: C.white, bold: true, margin: 0,
    });
    s.addText(item.desc, {
      x: 1.6, y: yy + 0.42, w: 7.5, h: 0.4,
      fontFace: FONT_B, fontSize: 12, color: C.muted, margin: 0,
    });
  });

  s.addText("Thank you", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontFace: FONT_H, fontSize: 18, color: C.accent, italic: true, align: "center",
  });
}

// ── Write file ──
pres.writeFile({ fileName: "slides/week9-progress-2026-04-28.pptx" })
  .then(() => console.log("Created: slides/week9-progress-2026-04-28.pptx"))
  .catch(err => console.error(err));
