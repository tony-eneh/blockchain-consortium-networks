// Week-8 progress deck — same design system as scripts/generate_slides_week7.js
// Run: node scripts/generate_slides_week8.js
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Tony Eneh";
pres.title = "Blockchain Consortium Networks SLR — Week 8 Progress";

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

  s.addText("PRISMA 2020 Systematic Review — Week 8 Progress", {
    x: 0.8, y: 2.9, w: 8.4, h: 0.5,
    fontFace: FONT_B, fontSize: 18, color: C.accent, italic: true,
  });

  s.addText([
    { text: "Tony Eneh", options: { bold: true, breakLine: true } },
    { text: "Networked Systems Laboratory (NSL)", options: { breakLine: true } },
    { text: "Kumoh National Institute of Technology (KIT)", options: { breakLine: true } },
    { text: "April 21, 2026" },
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

  s.addText("Where We Left Off (Week 7)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  // Three big stat cards: 571 / 775 / 292
  const screenStats = [
    { num: "571", label: "T/A Included", pct: "34.9%", color: C.done },
    { num: "775", label: "T/A Excluded", pct: "47.3%", color: C.red },
    { num: "292", label: "T/A Uncertain", pct: "17.8%", color: C.amber },
  ];
  screenStats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 1.5, fill: { color: C.card }, shadow: cardShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 0.07, fill: { color: st.color } });
    s.addText(st.num, {
      x: xx, y: 1.28, w: 2.8, h: 0.7,
      fontFace: FONT_H, fontSize: 40, color: st.color, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(`${st.label}  (${st.pct})`, {
      x: xx, y: 2.05, w: 2.8, h: 0.35,
      fontFace: FONT_B, fontSize: 13, color: C.muted, align: "center", margin: 0,
    });
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.0, w: 8.8, h: 2.1, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Open issue going into Week 8", {
    x: 0.8, y: 3.1, w: 8.4, h: 0.4,
    fontFace: FONT_B, fontSize: 16, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "863 candidates", options: { bold: true } },
    { text: " awaiting full-text review (571 first-pass include + 292 uncertain).", options: { breakLine: true } },
    { text: "Manual screening at this scale is not feasible inside the semester window — we needed an agent-driven pipeline.", options: { breakLine: true } },
    { text: "Risk: open-access gap. Many institutional consortium papers are paywalled.", options: {} },
  ], {
    x: 0.8, y: 3.55, w: 8.4, h: 1.5,
    fontFace: FONT_B, fontSize: 14, color: C.text, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 3 — Timeline weeks 1-8
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Progress Timeline (Weeks 1–8)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  const timeline = [
    { week: "1–2", label: "RQs + PICOC scope", status: "done" },
    { week: "3–4", label: "PRISMA protocol + search strings", status: "done" },
    { week: "5–6", label: "Search + deduplication", status: "done" },
    { week: "7",   label: "Title/abstract screening", status: "done" },
    { week: "8",   label: "Agent full-text screening", status: "current" },
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

  // This week box
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.85, w: 8.8, h: 2.4, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("This Week's Work", {
    x: 0.8, y: 2.95, w: 8.4, h: 0.35,
    fontFace: FONT_B, fontSize: 16, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "1. ", options: { bold: true } },
    { text: "Closed the 292-record uncertain queue end-to-end (no manual backlog).", options: { breakLine: true } },
    { text: "2. ", options: { bold: true } },
    { text: "Built and ran an agent full-text reviewer over all 863 candidates.", options: { breakLine: true } },
    { text: "3. ", options: { bold: true } },
    { text: "Auto-generated the PRISMA 2020 flow figure from the screening CSV.", options: { breakLine: true } },
    { text: "4. ", options: { bold: true } },
    { text: "Refreshed paper draft (abstract, Study Selection, Study Characteristics) and TODO.", options: {} },
  ], {
    x: 0.8, y: 3.4, w: 8.4, h: 1.7,
    fontFace: FONT_B, fontSize: 14, color: C.text, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 4 — Agent pipeline architecture
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Agent Full-Text Screening Pipeline", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 28, color: C.primary, bold: true, margin: 0,
  });

  // Pipeline as 5 boxes with arrows
  const stages = [
    { title: "Discover", body: "arXiv abs→pdf, OpenAlex by DOI/title, raw URL probe" },
    { title: "Fetch",    body: "In-memory PDF/HTML download (no on-disk cache)" },
    { title: "Extract",  body: "pypdf per-page text + bs4 HTML fallback" },
    { title: "Score",    body: "Institutional + implementation + evidence keyword baskets" },
    { title: "Finalise", body: "Conservative: needs_human_check → exclude" },
  ];
  const boxW = 1.66, boxH = 1.5;
  const startX = 0.6;
  stages.forEach((st, i) => {
    const xx = startX + i * (boxW + 0.1);
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.2, w: boxW, h: boxH, fill: { color: C.card }, shadow: cardShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.2, w: boxW, h: 0.07, fill: { color: C.accent } });
    s.addText(st.title, {
      x: xx, y: 1.32, w: boxW, h: 0.4,
      fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, align: "center", margin: 0,
    });
    s.addText(st.body, {
      x: xx + 0.05, y: 1.7, w: boxW - 0.1, h: 0.95,
      fontFace: FONT_B, fontSize: 10.5, color: C.text, align: "center", valign: "top", margin: 0, lineSpacingMultiple: 1.2,
    });
    if (i < stages.length - 1) {
      s.addText("›", {
        x: xx + boxW - 0.05, y: 1.75, w: 0.2, h: 0.4,
        fontFace: FONT_B, fontSize: 22, color: C.accent, bold: true, align: "center", margin: 0,
      });
    }
  });

  // Two-column: scripts | guarantees
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.0, w: 4.3, h: 2.3, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Reproducible scripts", {
    x: 0.8, y: 3.05, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "review_firstpass_fulltexts.py  (NEW)", options: { bullet: true, breakLine: true } },
    { text: "review_accessible_fulltexts.py", options: { bullet: true, breakLine: true } },
    { text: "discover_ambiguous_fulltexts.py", options: { bullet: true, breakLine: true } },
    { text: "finalize_uncertain_decisions.py", options: { bullet: true, breakLine: true } },
    { text: "generate_prisma_flow.py  (NEW)", options: { bullet: true } },
  ], {
    x: 0.8, y: 3.4, w: 4.0, h: 1.85,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 3.0, w: 4.3, h: 2.3, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Guarantees", {
    x: 5.3, y: 3.05, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "Deterministic — re-running reproduces 279/584", options: { bullet: true, breakLine: true } },
    { text: "Checkpoint+resume every 25 records", options: { bullet: true, breakLine: true } },
    { text: "Per-page try/except on PDF extraction", options: { bullet: true, breakLine: true } },
    { text: "Single source of truth: fulltext_screening.csv", options: { bullet: true, breakLine: true } },
    { text: "Audit trail in data/reports/*.md", options: { bullet: true } },
  ], {
    x: 5.3, y: 3.4, w: 4.0, h: 1.85,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 5 — Full-Text Screening Results
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Full-Text Screening Results", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  // 3 stat cards
  const stats = [
    { num: "863", label: "Candidates Reviewed", color: C.primary, white: true },
    { num: "279", label: "Included  (32.3%)", color: C.done },
    { num: "584", label: "Excluded  (67.7%)", color: C.red },
  ];
  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    const fillCol = st.white ? C.primary : C.card;
    const numCol = st.white ? C.white : st.color;
    const labCol = st.white ? C.light : C.muted;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 1.5, fill: { color: fillCol }, shadow: cardShadow() });
    if (!st.white) {
      s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 0.07, fill: { color: st.color } });
    }
    s.addText(st.num, {
      x: xx, y: 1.28, w: 2.8, h: 0.7,
      fontFace: FONT_H, fontSize: 40, color: numCol, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: xx, y: 2.05, w: 2.8, h: 0.35,
      fontFace: FONT_B, fontSize: 13, color: labCol, align: "center", margin: 0,
    });
  });

  // Two-column breakdown of where include/exclude came from
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.95, w: 4.3, h: 2.25, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Where the 279 includes came from", {
    x: 0.8, y: 3.0, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.done, bold: true, margin: 0,
  });
  s.addText([
    { text: "First-pass agent review:  136", options: { bullet: true, breakLine: true } },
    { text: "Triage promotions:        123", options: { bullet: true, breakLine: true } },
    { text: "Accessible OA agent:        20", options: { bullet: true, breakLine: true } },
    { text: "Total:                    279", options: { bullet: true, bold: true } },
  ], {
    x: 0.8, y: 3.4, w: 4.0, h: 1.7,
    fontFace: "Consolas", fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.95, w: 4.3, h: 2.25, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Where the 584 exclusions came from", {
    x: 5.3, y: 3.0, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.red, bold: true, margin: 0,
  });
  s.addText([
    { text: "First-pass agent review:  435", options: { bullet: true, breakLine: true } },
    { text: "No / insufficient OA:      68 + …", options: { bullet: true, breakLine: true } },
    { text: "Triage likely-exclude:     48", options: { bullet: true, breakLine: true } },
    { text: "Borderline (conservative): 33", options: { bullet: true, breakLine: true } },
    { text: "Total:                    584", options: { bullet: true, bold: true } },
  ], {
    x: 5.3, y: 3.4, w: 4.0, h: 1.7,
    fontFace: "Consolas", fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 6 — Exclusion reason breakdown
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Why we excluded 584 candidates", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 28, color: C.primary, bold: true, margin: 0,
  });

  const reasons = [
    { label: "Insufficient full-text access",   n: 281 },
    { label: "No open-access full text",         n: 210 },
    { label: "Second-pass likely exclude",       n: 48  },
    { label: "Agent borderline (conservative)",  n: 32  },
    { label: "No reproducible evidence",         n: 7   },
    { label: "Policy / commentary only",         n: 2   },
    { label: "Borderline full-text case",        n: 2   },
    { label: "Not institutional setting",        n: 1   },
    { label: "No implementation detail",         n: 1   },
  ];
  const total = 584;
  const maxN = reasons[0].n;
  const barAreaW = 4.6;
  const rowH = 0.36;
  const startY = 1.15;

  reasons.forEach((r, i) => {
    const yy = startY + i * rowH;
    s.addText(r.label, {
      x: 0.6, y: yy, w: 3.4, h: rowH,
      fontFace: FONT_B, fontSize: 11, color: C.text, valign: "middle", margin: 0,
    });
    const w = Math.max(0.05, (r.n / maxN) * barAreaW);
    s.addShape(pres.shapes.RECTANGLE, { x: 4.0, y: yy + 0.06, w, h: rowH - 0.12, fill: { color: i < 2 ? C.red : (i < 4 ? C.amber : C.todo) } });
    s.addText(`${r.n}  (${(r.n*100/total).toFixed(1)}%)`, {
      x: 4.0 + w + 0.05, y: yy, w: 1.6, h: rowH,
      fontFace: FONT_B, fontSize: 11, color: C.text, valign: "middle", margin: 0,
    });
  });

  // Side panel: top driver + author work
  s.addShape(pres.shapes.RECTANGLE, { x: 6.4, y: 1.15, w: 3.0, h: 4.0, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Top driver", {
    x: 6.55, y: 1.2, w: 2.8, h: 0.3,
    fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, margin: 0,
  });
  s.addText("Open-access gap dominates: 491 of 584 (84%) excluded purely for lack of full text.", {
    x: 6.55, y: 1.5, w: 2.8, h: 1.0,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });
  s.addText("Author follow-up", {
    x: 6.55, y: 2.7, w: 2.8, h: 0.3,
    fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "Procure paywalled full-texts via institutional access; re-run agent.", options: { bullet: true, breakLine: true } },
    { text: "Sample 32 borderline + 48 second-pass excludes.", options: { bullet: true } },
  ], {
    x: 6.55, y: 3.0, w: 2.8, h: 2.0,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 7 — Updated PRISMA flow (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  s.addText("PRISMA 2020 Flow — Updated", {
    x: 0.6, y: 0.15, w: 9, h: 0.5,
    fontFace: FONT_H, fontSize: 26, color: C.white, bold: true, margin: 0,
  });

  // IDENTIFICATION
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 0.7, w: 6.0, h: 0.5, fill: { color: C.primary } });
  s.addText("IDENTIFICATION  —  4 sources: 1,707 records", {
    x: 2.0, y: 0.7, w: 6.0, h: 0.5,
    fontFace: FONT_B, fontSize: 13, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
  });
  s.addText("\u25BC", { x: 4.6, y: 1.2, w: 0.8, h: 0.25, fontFace: FONT_B, fontSize: 16, color: C.accent, align: "center", margin: 0 });

  // Dedup
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 1.43, w: 6.0, h: 0.4, fill: { color: C.primary } });
  s.addText("Duplicates removed: 69  →  1,638 unique", {
    x: 2.0, y: 1.43, w: 6.0, h: 0.4,
    fontFace: FONT_B, fontSize: 12, color: C.white, align: "center", valign: "middle", margin: 0,
  });
  s.addText("\u25BC", { x: 4.6, y: 1.83, w: 0.8, h: 0.22, fontFace: FONT_B, fontSize: 14, color: C.accent, align: "center", margin: 0 });

  // T/A screening
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 2.05, w: 6.0, h: 0.45, fill: { color: C.accent } });
  s.addText("TITLE/ABSTRACT  —  1,638 screened", {
    x: 2.0, y: 2.05, w: 6.0, h: 0.45,
    fontFace: FONT_B, fontSize: 13, color: C.dark, bold: true, align: "center", valign: "middle", margin: 0,
  });

  // T/A branches
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 2.65, w: 2.8, h: 0.7, fill: { color: "3B1C1C" } });
  s.addText([
    { text: "Excluded", options: { bold: true, fontSize: 12, color: C.red, breakLine: true } },
    { text: "775", options: { fontSize: 14, color: C.white } },
  ], { x: 0.3, y: 2.7, w: 2.8, h: 0.6, fontFace: FONT_B, align: "center", valign: "middle" });

  s.addShape(pres.shapes.RECTANGLE, { x: 3.6, y: 2.65, w: 2.8, h: 0.7, fill: { color: "3B2E10" } });
  s.addText([
    { text: "Uncertain → resolved", options: { bold: true, fontSize: 12, color: C.amber, breakLine: true } },
    { text: "292", options: { fontSize: 14, color: C.white } },
  ], { x: 3.6, y: 2.7, w: 2.8, h: 0.6, fontFace: FONT_B, align: "center", valign: "middle" });

  s.addShape(pres.shapes.RECTANGLE, { x: 6.9, y: 2.65, w: 2.8, h: 0.7, fill: { color: "0D3320" } });
  s.addText([
    { text: "Included", options: { bold: true, fontSize: 12, color: C.done, breakLine: true } },
    { text: "571", options: { fontSize: 14, color: C.white } },
  ], { x: 6.9, y: 2.7, w: 2.8, h: 0.6, fontFace: FONT_B, align: "center", valign: "middle" });

  s.addText("\u25BC", { x: 4.6, y: 3.4, w: 0.8, h: 0.22, fontFace: FONT_B, fontSize: 14, color: C.accent, align: "center", margin: 0 });

  // Full-text candidates
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 3.62, w: 6.0, h: 0.45, fill: { color: C.accent } });
  s.addText("FULL-TEXT CANDIDATES  —  863  (571 + 292)", {
    x: 2.0, y: 3.62, w: 6.0, h: 0.45,
    fontFace: FONT_B, fontSize: 13, color: C.dark, bold: true, align: "center", valign: "middle", margin: 0,
  });

  // Full-text branches
  s.addShape(pres.shapes.RECTANGLE, { x: 1.0, y: 4.25, w: 3.5, h: 0.85, fill: { color: "3B1C1C" } });
  s.addText([
    { text: "EXCLUDED", options: { bold: true, fontSize: 13, color: C.red, breakLine: true } },
    { text: "584", options: { fontSize: 22, color: C.white, bold: true, breakLine: true } },
    { text: "OA gap 491 · second-pass 48 · borderline 34 · protocol 11", options: { fontSize: 9.5, color: C.muted } },
  ], { x: 1.0, y: 4.28, w: 3.5, h: 0.8, fontFace: FONT_B, align: "center", valign: "middle" });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.5, y: 4.25, w: 3.5, h: 0.85, fill: { color: "0D3320" } });
  s.addText([
    { text: "INCLUDED IN REVIEW", options: { bold: true, fontSize: 13, color: C.done, breakLine: true } },
    { text: "279", options: { fontSize: 22, color: C.white, bold: true } },
  ], { x: 5.5, y: 4.28, w: 3.5, h: 0.8, fontFace: FONT_B, align: "center", valign: "middle" });

  s.addText("Auto-generated TikZ figure: paper/figures/prisma_flow.tex", {
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
    { step: "1", label: "Research questions (PICOC)", status: "done" },
    { step: "2", label: "PRISMA protocol", status: "done" },
    { step: "3", label: "Search strings (PRISMA-S)", status: "done" },
    { step: "4", label: "Search execution + deduplication", status: "done" },
    { step: "5a", label: "Title/abstract screening", status: "done" },
    { step: "5b", label: "Full-text screening (agent)", status: "done" },
    { step: "6", label: "Data extraction (over 279 includes)", status: "next" },
    { step: "7", label: "Quality assessment", status: "todo" },
    { step: "8", label: "Synthesis + taxonomy", status: "todo" },
  ];

  steps.forEach((item, i) => {
    const yy = 1.05 + i * 0.46;
    const isDone = item.status === "done";
    const isNext = item.status === "next";

    const circleColor = isDone ? C.done : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.OVAL, { x: 0.7, y: yy + 0.04, w: 0.36, h: 0.36, fill: { color: circleColor } });
    s.addText(item.step, {
      x: 0.7, y: yy + 0.04, w: 0.36, h: 0.36,
      fontFace: FONT_B, fontSize: 10, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });

    s.addText(item.label, {
      x: 1.25, y: yy, w: 6.0, h: 0.42,
      fontFace: FONT_B, fontSize: 13, color: isDone ? C.muted : C.text,
      bold: isNext, valign: "middle", margin: 0,
    });

    const badgeText = isDone ? "Done" : isNext ? "Next" : "Upcoming";
    const badgeColor = isDone ? C.done : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: yy + 0.05, w: 1.3, h: 0.32, fill: { color: badgeColor } });
    s.addText(badgeText, {
      x: 7.5, y: yy + 0.05, w: 1.3, h: 0.32,
      fontFace: FONT_B, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });
  });

  s.addText("Branch main is 11 commits ahead of origin/main (4 added this week).", {
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

  s.addText("Next Steps (Week 9)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.white, bold: true, margin: 0,
  });

  const nextItems = [
    { num: "01", title: "Data extraction over 279 includes",
      desc: "Populate data_extraction.csv: network type, consensus, governance, deployment scale, evidence type." },
    { num: "02", title: "Quality assessment rubric",
      desc: "Apply CASP-style scoring; flag low-quality items for sensitivity analysis." },
    { num: "03", title: "Recover paywalled full-texts",
      desc: "Procure 491 paywalled candidates via institutional access; re-run agent reviewer." },
    { num: "04", title: "Snowball + synthesis kickoff",
      desc: "Backward/forward sampling on the 279; begin taxonomy synthesis (Discussion scaffolding)." },
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
pres.writeFile({ fileName: "slides/week8-progress-2026-04-21.pptx" })
  .then(() => console.log("Created: slides/week8-progress-2026-04-21.pptx"))
  .catch(err => console.error(err));
