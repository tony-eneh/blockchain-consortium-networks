const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Tony Eneh";
pres.title = "Blockchain Consortium Networks SLR — Week 7 Progress";

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

  s.addText("PRISMA 2020 Systematic Review — Week 7 Progress", {
    x: 0.8, y: 2.9, w: 8.4, h: 0.5,
    fontFace: FONT_B, fontSize: 18, color: C.accent, italic: true,
  });

  s.addText([
    { text: "Tony Eneh", options: { bold: true, breakLine: true } },
    { text: "Networked Systems Laboratory (NSL)", options: { breakLine: true } },
    { text: "Kumoh National Institute of Technology (KIT)", options: { breakLine: true } },
    { text: "April 14, 2026" },
  ], {
    x: 0.8, y: 3.7, w: 8.4, h: 1.2,
    fontFace: FONT_B, fontSize: 13, color: C.muted, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 2 — Review Recap (condensed)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Review Recap", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  const rqs = [
    { tag: "RQ1", body: "Taxonomy of blockchain strategies (architecture, governance, consensus, privacy)" },
    { tag: "RQ2", body: "Empirical trade-offs: performance, resilience, privacy, complexity" },
    { tag: "RQ3", body: "Interoperability patterns in institutional settings" },
    { tag: "RQ4", body: "Design gaps and reference implementation requirements" },
  ];

  rqs.forEach((rq, i) => {
    const yy = 1.15 + i * 0.65;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: yy, w: 8.8, h: 0.52, fill: { color: C.card }, shadow: cardShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: yy, w: 0.07, h: 0.52, fill: { color: C.accent } });
    s.addText(rq.tag, {
      x: 0.85, y: yy + 0.06, w: 0.7, h: 0.4,
      fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
    });
    s.addText(rq.body, {
      x: 1.6, y: yy + 0.06, w: 7.6, h: 0.4,
      fontFace: FONT_B, fontSize: 14, color: C.text, margin: 0,
    });
  });

  // Scope + standard
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.9, w: 4.2, h: 0.9, fill: { color: C.light }, shadow: cardShadow() });
  s.addText([
    { text: "Standard", options: { bold: true, fontSize: 12, color: C.muted, breakLine: true } },
    { text: "PRISMA 2020 + PRISMA-S", options: { fontSize: 15, color: C.text } },
  ], { x: 0.8, y: 3.95, w: 3.8, h: 0.8, fontFace: FONT_B });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 3.9, w: 4.2, h: 0.9, fill: { color: C.light }, shadow: cardShadow() });
  s.addText([
    { text: "Scope", options: { bold: true, fontSize: 12, color: C.muted, breakLine: true } },
    { text: "Inter-bank, inter-agency, B2B enterprise consortia", options: { fontSize: 15, color: C.text } },
  ], { x: 5.4, y: 3.95, w: 3.8, h: 0.8, fontFace: FONT_B });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 3 — What was done (weeks 1-7 timeline)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Progress Timeline (Weeks 1–7)", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  const timeline = [
    { week: "1–2", label: "Research questions + PICOC scope", status: "done" },
    { week: "3–4", label: "PRISMA protocol + search strings", status: "done" },
    { week: "5–6", label: "Search execution + deduplication", status: "done" },
    { week: "7",   label: "Title/abstract screening", status: "current" },
  ];

  // Horizontal timeline bar
  s.addShape(pres.shapes.RECTANGLE, { x: 1.0, y: 1.3, w: 8.0, h: 0.08, fill: { color: C.accent } });

  timeline.forEach((item, i) => {
    const xx = 1.0 + i * 2.4;
    const isCurrent = item.status === "current";
    const circleColor = isCurrent ? C.accent : C.done;
    const circleSize = isCurrent ? 0.45 : 0.35;
    const offset = isCurrent ? -0.05 : 0;

    s.addShape(pres.shapes.OVAL, {
      x: xx + 0.6 - circleSize/2, y: 1.34 - circleSize/2 + offset, w: circleSize, h: circleSize,
      fill: { color: circleColor },
    });

    s.addText(item.week, {
      x: xx, y: 1.65, w: 1.2, h: 0.3,
      fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, align: "center", margin: 0,
    });
    s.addText(item.label, {
      x: xx - 0.3, y: 1.95, w: 1.8, h: 0.6,
      fontFace: FONT_B, fontSize: 11, color: C.text, align: "center", margin: 0,
    });
  });

  // This week's highlight box
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.9, w: 8.8, h: 1.8, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("This Week's Work", {
    x: 0.8, y: 3.0, w: 8.4, h: 0.35,
    fontFace: FONT_B, fontSize: 16, color: C.primary, bold: true, margin: 0,
  });
  s.addText([
    { text: "1. ", options: { bold: true } },
    { text: "Executed database searches across 4 sources (IEEE, WoS, arXiv API, OpenAlex API)", options: { breakLine: true } },
    { text: "2. ", options: { bold: true } },
    { text: "Normalized exports and deduplicated records (1,707 \u2192 1,638 unique)", options: { breakLine: true } },
    { text: "3. ", options: { bold: true } },
    { text: "Title/abstract screening using inclusion/exclusion criteria", options: {} },
  ], {
    x: 0.8, y: 3.4, w: 8.4, h: 1.2,
    fontFace: FONT_B, fontSize: 14, color: C.text, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 4 — Search Results (kept from previous)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Search Results", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  const stats = [
    { num: "1,707", label: "Total Identified" },
    { num: "69", label: "Duplicates Removed" },
    { num: "1,638", label: "Unique Records" },
  ];

  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.1, w: 2.8, h: 1.3, fill: { color: i === 2 ? C.primary : C.card }, shadow: cardShadow() });
    s.addText(st.num, {
      x: xx, y: 1.15, w: 2.8, h: 0.75,
      fontFace: FONT_H, fontSize: 42, color: i === 2 ? C.white : C.primary, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: xx, y: 1.9, w: 2.8, h: 0.35,
      fontFace: FONT_B, fontSize: 12, color: i === 2 ? C.light : C.muted, align: "center", valign: "middle", margin: 0,
    });
  });

  const hdr = { fill: { color: C.primary }, color: C.white, bold: true, fontFace: FONT_B, fontSize: 12, align: "left", valign: "middle" };
  const hdrR = { fill: { color: C.primary }, color: C.white, bold: true, fontFace: FONT_B, fontSize: 12, align: "right", valign: "middle" };
  const cl  = { fill: { color: C.white }, color: C.text, fontFace: FONT_B, fontSize: 12, valign: "middle" };
  const clR = { fill: { color: C.white }, color: C.text, fontFace: FONT_B, fontSize: 12, align: "right", valign: "middle" };
  const al  = { fill: { color: C.light }, color: C.text, fontFace: FONT_B, fontSize: 12, valign: "middle" };
  const alR = { fill: { color: C.light }, color: C.text, fontFace: FONT_B, fontSize: 12, align: "right", valign: "middle" };

  s.addTable([
    [{ text: "Source", options: hdr }, { text: "Method", options: hdr }, { text: "Records", options: hdrR }],
    [{ text: "IEEE Xplore", options: cl }, { text: "Manual export", options: cl }, { text: "386", options: clR }],
    [{ text: "Web of Science", options: al }, { text: "Manual export", options: al }, { text: "50", options: alR }],
    [{ text: "arXiv", options: cl }, { text: "API (15 sub-queries)", options: cl }, { text: "49", options: clR }],
    [{ text: "OpenAlex", options: al }, { text: "API (replaces ACM+Scopus)", options: al }, { text: "1,222", options: alR }],
  ], {
    x: 0.6, y: 2.7, w: 8.8,
    colW: [2.2, 4.0, 2.6],
    border: { pt: 0.5, color: "CBD5E1" },
    rowH: [0.4, 0.4, 0.4, 0.4, 0.4],
  });

  s.addText("Dedup: DOI match (40) + title+year match (29) = 69 removed", {
    x: 0.6, y: 4.85, w: 8.8, h: 0.35,
    fontFace: FONT_B, fontSize: 12, color: C.muted, italic: true, align: "center",
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 5 — Screening Results (NEW)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Title/Abstract Screening Results", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 30, color: C.primary, bold: true, margin: 0,
  });

  // Three big stat cards
  const screenStats = [
    { num: "571", label: "Included", pct: "34.9%", color: C.done },
    { num: "775", label: "Excluded", pct: "47.3%", color: C.red },
    { num: "292", label: "Uncertain", pct: "17.8%", color: C.amber },
  ];

  screenStats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.1, w: 2.8, h: 1.5, fill: { color: C.card }, shadow: cardShadow() });
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.1, w: 2.8, h: 0.07, fill: { color: st.color } });
    s.addText(st.num, {
      x: xx, y: 1.25, w: 2.8, h: 0.7,
      fontFace: FONT_H, fontSize: 40, color: st.color, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(`${st.label} (${st.pct})`, {
      x: xx, y: 2.05, w: 2.8, h: 0.35,
      fontFace: FONT_B, fontSize: 13, color: C.muted, align: "center", margin: 0,
    });
  });

  // Screening criteria summary
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.95, w: 4.3, h: 2.2, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Inclusion Criteria", {
    x: 0.8, y: 3.0, w: 4.0, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.done, bold: true, margin: 0,
  });
  s.addText([
    { text: "Blockchain technology term present", options: { bullet: true, breakLine: true } },
    { text: "Institutional / consortium setting", options: { bullet: true, breakLine: true } },
    { text: "Strategy details (consensus, governance, privacy, interop)", options: { bullet: true, breakLine: true } },
    { text: "Evidence of implementation or evaluation", options: { bullet: true } },
  ], {
    x: 0.8, y: 3.35, w: 3.9, h: 1.6,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 2.95, w: 4.2, h: 2.2, fill: { color: C.card }, shadow: cardShadow() });
  s.addText("Top Exclusion Reasons", {
    x: 5.4, y: 3.0, w: 3.8, h: 0.35,
    fontFace: FONT_B, fontSize: 14, color: C.red, bold: true, margin: 0,
  });
  s.addText([
    { text: "Insufficient relevance signals (607)", options: { bullet: true, breakLine: true } },
    { text: "No abstract + irrelevant title (127)", options: { bullet: true, breakLine: true } },
    { text: "No blockchain technology term (31)", options: { bullet: true, breakLine: true } },
    { text: "Non-technical commentary (5)", options: { bullet: true, breakLine: true } },
    { text: "Crypto-market / single-org (5)", options: { bullet: true } },
  ], {
    x: 5.4, y: 3.35, w: 3.8, h: 1.6,
    fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.3,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 6 — PRISMA Flow (dark, updated with screening)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  s.addText("PRISMA Flow Diagram", {
    x: 0.6, y: 0.15, w: 9, h: 0.5,
    fontFace: FONT_H, fontSize: 28, color: C.white, bold: true, margin: 0,
  });

  // Row 1: Identification
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 0.75, w: 6.0, h: 0.55, fill: { color: C.primary } });
  s.addText("IDENTIFICATION  —  Records from 4 databases: 1,707", {
    x: 2.0, y: 0.75, w: 6.0, h: 0.55,
    fontFace: FONT_B, fontSize: 14, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
  });

  // Arrow
  s.addText("\u25BC", { x: 4.6, y: 1.3, w: 0.8, h: 0.3, fontFace: FONT_B, fontSize: 18, color: C.accent, align: "center", margin: 0 });

  // Row 2: Dedup
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 1.55, w: 6.0, h: 0.5, fill: { color: C.primary } });
  s.addText("Duplicates removed: 69  \u2192  1,638 unique records", {
    x: 2.0, y: 1.55, w: 6.0, h: 0.5,
    fontFace: FONT_B, fontSize: 13, color: C.white, align: "center", valign: "middle", margin: 0,
  });

  // Arrow
  s.addText("\u25BC", { x: 4.6, y: 2.05, w: 0.8, h: 0.3, fontFace: FONT_B, fontSize: 18, color: C.accent, align: "center", margin: 0 });

  // Row 3: Screening
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 2.3, w: 6.0, h: 0.55, fill: { color: C.accent } });
  s.addText("SCREENING  —  Title/abstract screened: 1,638", {
    x: 2.0, y: 2.3, w: 6.0, h: 0.55,
    fontFace: FONT_B, fontSize: 14, color: C.dark, bold: true, align: "center", valign: "middle", margin: 0,
  });

  // Branch: excluded
  s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 3.05, w: 2.8, h: 0.85, fill: { color: "3B1C1C" } });
  s.addText([
    { text: "Excluded", options: { bold: true, fontSize: 13, color: C.red, breakLine: true } },
    { text: "775 records", options: { fontSize: 16, color: C.white } },
  ], { x: 0.3, y: 3.1, w: 2.8, h: 0.75, fontFace: FONT_B, align: "center", valign: "middle" });

  // Branch: uncertain
  s.addShape(pres.shapes.RECTANGLE, { x: 3.6, y: 3.05, w: 2.8, h: 0.85, fill: { color: "3B2E10" } });
  s.addText([
    { text: "Uncertain", options: { bold: true, fontSize: 13, color: C.amber, breakLine: true } },
    { text: "292 records", options: { fontSize: 16, color: C.white } },
  ], { x: 3.6, y: 3.1, w: 2.8, h: 0.75, fontFace: FONT_B, align: "center", valign: "middle" });

  // Branch: included
  s.addShape(pres.shapes.RECTANGLE, { x: 6.9, y: 3.05, w: 2.8, h: 0.85, fill: { color: "0D3320" } });
  s.addText([
    { text: "Included", options: { bold: true, fontSize: 13, color: C.done, breakLine: true } },
    { text: "571 records", options: { fontSize: 16, color: C.white } },
  ], { x: 6.9, y: 3.1, w: 2.8, h: 0.75, fontFace: FONT_B, align: "center", valign: "middle" });

  // Arrow to next phase
  s.addText("\u25BC", { x: 4.6, y: 4.0, w: 0.8, h: 0.3, fontFace: FONT_B, fontSize: 18, color: C.accent, align: "center", margin: 0 });

  // Full-text phase (upcoming)
  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 4.25, w: 6.0, h: 0.55, fill: { color: C.primary }, shadow: cardShadow() });
  s.addText("FULL-TEXT REVIEW  —  Candidates: 863  (571 + 292 uncertain)", {
    x: 2.0, y: 4.25, w: 6.0, h: 0.55,
    fontFace: FONT_B, fontSize: 13, color: C.muted, align: "center", valign: "middle", margin: 0,
  });

  // Arrow
  s.addText("\u25BC", { x: 4.6, y: 4.8, w: 0.8, h: 0.3, fontFace: FONT_B, fontSize: 18, color: C.muted, align: "center", margin: 0 });

  s.addShape(pres.shapes.RECTANGLE, { x: 2.0, y: 5.0, w: 6.0, h: 0.45, fill: { color: C.primary } });
  s.addText("INCLUDED IN REVIEW  —  ???  (after full-text screening)", {
    x: 2.0, y: 5.0, w: 6.0, h: 0.45,
    fontFace: FONT_B, fontSize: 12, color: C.muted, align: "center", valign: "middle", margin: 0,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 7 — Progress Tracker
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
    { step: "5b", label: "Full-text screening", status: "next" },
    { step: "6", label: "Data extraction", status: "todo" },
    { step: "7-8", label: "Quality assessment + synthesis", status: "todo" },
  ];

  steps.forEach((item, i) => {
    const yy = 1.05 + i * 0.54;
    const isDone = item.status === "done";
    const isNext = item.status === "next";

    const circleColor = isDone ? C.done : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.OVAL, { x: 0.7, y: yy + 0.05, w: 0.38, h: 0.38, fill: { color: circleColor } });
    s.addText(item.step, {
      x: 0.7, y: yy + 0.05, w: 0.38, h: 0.38,
      fontFace: FONT_B, fontSize: 10, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });

    s.addText(item.label, {
      x: 1.3, y: yy, w: 5.5, h: 0.45,
      fontFace: FONT_B, fontSize: 14, color: isDone ? C.muted : C.text,
      bold: isNext, valign: "middle", margin: 0,
    });

    const badgeText = isDone ? "Done" : isNext ? "Next" : "Upcoming";
    const badgeColor = isDone ? C.done : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: yy + 0.07, w: 1.3, h: 0.32, fill: { color: badgeColor } });
    s.addText(badgeText, {
      x: 7.5, y: yy + 0.07, w: 1.3, h: 0.32,
      fontFace: FONT_B, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });
  });

  s.addText("All artifacts version-controlled in Git.", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontFace: FONT_B, fontSize: 12, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 8 — Next Steps (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.565, w: 10, h: 0.06, fill: { color: C.accent } });

  s.addText("Next Steps", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.white, bold: true, margin: 0,
  });

  const nextItems = [
    { num: "01", title: "Manual review of 292 uncertain papers", desc: "Resolve borderline cases — reclassify as include or exclude." },
    { num: "02", title: "Full-text screening of 863 candidates", desc: "Retrieve PDFs and assess against full eligibility criteria." },
    { num: "03", title: "Record exclusion reasons", desc: "Code each exclusion for PRISMA flow diagram completion." },
    { num: "04", title: "Design data extraction form", desc: "Fields: platform, consensus, governance, privacy, interoperability, metrics, artifacts." },
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
      x: 1.6, y: yy + 0.42, w: 7.5, h: 0.35,
      fontFace: FONT_B, fontSize: 12, color: C.muted, margin: 0,
    });
  });

  s.addText("Thank you", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontFace: FONT_H, fontSize: 18, color: C.accent, italic: true, align: "center",
  });
}

// ── Write file ──
pres.writeFile({ fileName: "slides/week7-progress-2026-04-14.pptx" })
  .then(() => console.log("Created: slides/week7-progress-2026-04-14.pptx"))
  .catch(err => console.error(err));
