const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Tony Eneh";
pres.title = "Blockchain Consortium Networks SLR — Weekly Progress";

// ── Color Palette: Deep Teal + Slate (blockchain/institutional feel) ──
const C = {
  dark:    "0B1D26",   // near-black teal
  primary: "0D4F5C",   // deep teal
  accent:  "14B8A6",   // bright teal/mint
  light:   "E8F5F3",   // ice mint
  white:   "FFFFFF",
  text:    "1E293B",   // slate-900
  muted:   "64748B",   // slate-500
  card:    "F0FDFA",   // teal-50
  warn:    "F59E0B",   // amber
  done:    "10B981",   // emerald
  todo:    "94A3B8",   // slate-400
};

const FONT_H = "Cambria";
const FONT_B = "Calibri";

// Helper: fresh shadow object (pptxgenjs mutates in-place)
const cardShadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.10 });

// ════════════════════════════════════════════════════════════════
// SLIDE 1 — Title (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  // Top accent bar
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });

  s.addText("Blockchain Utilization Strategies\nin Institutional Consortium Networks", {
    x: 0.8, y: 1.0, w: 8.4, h: 2.0,
    fontFace: FONT_H, fontSize: 36, color: C.white, bold: true, lineSpacingMultiple: 1.15,
  });

  s.addText("PRISMA 2020 Systematic Review — Weekly Progress", {
    x: 0.8, y: 3.1, w: 8.4, h: 0.5,
    fontFace: FONT_B, fontSize: 18, color: C.accent, italic: true,
  });

  s.addText([
    { text: "Tony Eneh", options: { bold: true, breakLine: true } },
    { text: "Networked Systems Laboratory (NSL)", options: { breakLine: true } },
    { text: "Kumoh National Institute of Technology (KIT)", options: { breakLine: true } },
    { text: "April 14, 2026" },
  ], {
    x: 0.8, y: 4.0, w: 8.4, h: 1.2,
    fontFace: FONT_B, fontSize: 13, color: C.muted, lineSpacingMultiple: 1.4,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 2 — Review Objective (light)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };

  // Left accent stripe
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Review Objective", {
    x: 0.6, y: 0.4, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  // Goal card
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 1.3, w: 8.8, h: 1.2,
    fill: { color: C.card }, shadow: cardShadow(),
  });
  s.addText("Synthesize technical evidence on how institutions design and deploy consortium blockchain strategies, and derive an experimentally testable reference architecture.", {
    x: 0.9, y: 1.4, w: 8.2, h: 1.0,
    fontFace: FONT_B, fontSize: 16, color: C.text, lineSpacingMultiple: 1.3,
  });

  // Two info boxes side by side
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 2.9, w: 4.2, h: 1.1, fill: { color: C.light }, shadow: cardShadow() });
  s.addText([
    { text: "Standard", options: { bold: true, fontSize: 13, color: C.muted, breakLine: true } },
    { text: "PRISMA 2020 + PRISMA-S", options: { fontSize: 16, color: C.text } },
  ], { x: 0.8, y: 3.0, w: 3.8, h: 0.9, fontFace: FONT_B });

  s.addShape(pres.shapes.RECTANGLE, { x: 5.2, y: 2.9, w: 4.2, h: 1.1, fill: { color: C.light }, shadow: cardShadow() });
  s.addText([
    { text: "Scope", options: { bold: true, fontSize: 13, color: C.muted, breakLine: true } },
    { text: "Regulated multi-party settings — inter-bank, inter-agency, enterprise consortia", options: { fontSize: 14, color: C.text } },
  ], { x: 5.4, y: 3.0, w: 3.8, h: 0.9, fontFace: FONT_B });

  // Bottom note
  s.addText("Technical-first review paired with a reference implementation phase.", {
    x: 0.6, y: 4.4, w: 8.8, h: 0.5,
    fontFace: FONT_B, fontSize: 13, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 3 — Research Questions (2x2 grid cards)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Research Questions", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  const rqs = [
    { tag: "RQ1 · Taxonomy", body: "Which blockchain utilization strategies are reported for institutional consortium workflows? Taxonomize across architecture, governance, consensus, privacy." },
    { tag: "RQ2 · Trade-offs", body: "What empirical evidence exists on trade-offs among performance, resilience, privacy, and operational complexity?" },
    { tag: "RQ3 · Interoperability", body: "Which interoperability patterns (cross-chain, API-mediated, bridge/oracle, messaging) are most effective under institutional constraints?" },
    { tag: "RQ4 · Gaps & Implementation", body: "What design gaps and reproducibility weaknesses remain? How should a reference implementation be structured?" },
  ];

  const positions = [
    { x: 0.6, y: 1.15 }, { x: 5.2, y: 1.15 },
    { x: 0.6, y: 3.25 }, { x: 5.2, y: 3.25 },
  ];

  rqs.forEach((rq, i) => {
    const p = positions[i];
    s.addShape(pres.shapes.RECTANGLE, { x: p.x, y: p.y, w: 4.2, h: 1.8, fill: { color: C.card }, shadow: cardShadow() });
    // Accent left edge
    s.addShape(pres.shapes.RECTANGLE, { x: p.x, y: p.y, w: 0.07, h: 1.8, fill: { color: C.accent } });
    s.addText(rq.tag, {
      x: p.x + 0.25, y: p.y + 0.12, w: 3.7, h: 0.35,
      fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
    });
    s.addText(rq.body, {
      x: p.x + 0.25, y: p.y + 0.5, w: 3.75, h: 1.2,
      fontFace: FONT_B, fontSize: 12, color: C.text, lineSpacingMultiple: 1.25, margin: 0,
    });
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 4 — Search Strategy (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.primary };

  s.addText("Search Strategy", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.white, bold: true, margin: 0,
  });

  const blocks = [
    { label: "B1  Technology", terms: '"consortium blockchain" OR "permissioned blockchain" OR "enterprise blockchain" OR "distributed ledger"' },
    { label: "B2  Institutional Setting", terms: 'institution* OR "inter-organizational" OR "cross-organizational" OR interbank OR "multi-party"' },
    { label: "B3  Strategy Dimensions", terms: "governance OR consensus OR privacy OR confidentiality OR interoperability OR cross-chain" },
    { label: "B4  Technical Evidence", terms: "implement* OR prototype OR benchmark OR evaluation OR experiment*" },
  ];

  blocks.forEach((b, i) => {
    const yy = 1.15 + i * 0.95;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: yy, w: 8.8, h: 0.8, fill: { color: C.dark }, shadow: cardShadow() });
    s.addText(b.label, {
      x: 0.8, y: yy + 0.08, w: 2.6, h: 0.3,
      fontFace: FONT_B, fontSize: 13, color: C.accent, bold: true, margin: 0,
    });
    s.addText(b.terms, {
      x: 0.8, y: yy + 0.38, w: 8.4, h: 0.35,
      fontFace: FONT_B, fontSize: 11, color: C.white, margin: 0,
    });
  });

  s.addText("Combined with AND  ·  Date range: 2021 – present  ·  4 sources queried", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontFace: FONT_B, fontSize: 13, color: C.accent, italic: true, align: "center",
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 5 — Information Sources (light)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Information Sources", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  // Table
  const headerOpts = { fill: { color: C.primary }, color: C.white, bold: true, fontFace: FONT_B, fontSize: 13, align: "left", valign: "middle" };
  const cellOpts   = { fill: { color: C.white }, color: C.text, fontFace: FONT_B, fontSize: 12, align: "left", valign: "middle" };
  const altOpts    = { fill: { color: C.light }, color: C.text, fontFace: FONT_B, fontSize: 12, align: "left", valign: "middle" };

  const rows = [
    [
      { text: "Source", options: headerOpts },
      { text: "Method", options: headerOpts },
      { text: "Notes", options: headerOpts },
    ],
    [
      { text: "IEEE Xplore", options: cellOpts },
      { text: "Manual search + CSV export", options: cellOpts },
      { text: "Full Boolean query on All Metadata", options: cellOpts },
    ],
    [
      { text: "Web of Science", options: altOpts },
      { text: "Manual search + CSV export", options: altOpts },
      { text: "TS= Topic field tag", options: altOpts },
    ],
    [
      { text: "arXiv", options: cellOpts },
      { text: "Python script (Atom API)", options: cellOpts },
      { text: "15 focused sub-queries", options: cellOpts },
    ],
    [
      { text: "OpenAlex", options: altOpts },
      { text: "Python script (Works API)", options: altOpts },
      { text: "Replaces ACM DL + Scopus", options: altOpts },
    ],
  ];

  s.addTable(rows, {
    x: 0.6, y: 1.2, w: 8.8,
    colW: [2.2, 3.0, 3.6],
    border: { pt: 0.5, color: "CBD5E1" },
    rowH: [0.45, 0.45, 0.45, 0.45, 0.45],
  });

  // Explanation card
  s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: 3.7, w: 8.8, h: 1.3, fill: { color: C.card }, shadow: cardShadow() });
  s.addText([
    { text: "Why OpenAlex?  ", options: { bold: true, color: C.primary, fontSize: 14 } },
    { text: "ACM Digital Library requires a premium subscription to export CSV. Scopus requires an institutional subscription to search. Semantic Scholar API was attempted but rate-limited without an API key. OpenAlex is free, open, and indexes ~250M works including ACM and Elsevier/Scopus venues.", options: { fontSize: 13, color: C.text } },
  ], { x: 0.9, y: 3.8, w: 8.2, h: 1.1, fontFace: FONT_B, lineSpacingMultiple: 1.3 });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 6 — Search Results (stat callouts + table)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.white };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });

  s.addText("Search Results", {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 32, color: C.primary, bold: true, margin: 0,
  });

  // Big stat callouts
  const stats = [
    { num: "1,707", label: "Total Identified" },
    { num: "69", label: "Duplicates Removed" },
    { num: "1,638", label: "Unique Records" },
  ];

  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    s.addShape(pres.shapes.RECTANGLE, { x: xx, y: 1.15, w: 2.8, h: 1.4, fill: { color: i === 2 ? C.primary : C.card }, shadow: cardShadow() });
    s.addText(st.num, {
      x: xx, y: 1.2, w: 2.8, h: 0.8,
      fontFace: FONT_H, fontSize: 44, color: i === 2 ? C.white : C.primary, bold: true, align: "center", valign: "middle", margin: 0,
    });
    s.addText(st.label, {
      x: xx, y: 2.0, w: 2.8, h: 0.4,
      fontFace: FONT_B, fontSize: 12, color: i === 2 ? C.light : C.muted, align: "center", valign: "middle", margin: 0,
    });
  });

  // Per-source breakdown table
  const hdr = { fill: { color: C.primary }, color: C.white, bold: true, fontFace: FONT_B, fontSize: 12, align: "left", valign: "middle" };
  const hdrR = { ...hdr, align: "right" };
  const cl  = { fill: { color: C.white }, color: C.text, fontFace: FONT_B, fontSize: 12, valign: "middle" };
  const clR = { ...cl, align: "right" };
  const al  = { fill: { color: C.light }, color: C.text, fontFace: FONT_B, fontSize: 12, valign: "middle" };
  const alR = { ...al, align: "right" };

  s.addTable([
    [{ text: "Source", options: hdr }, { text: "Records", options: hdrR }],
    [{ text: "IEEE Xplore", options: cl }, { text: "386", options: clR }],
    [{ text: "Web of Science", options: al }, { text: "50", options: alR }],
    [{ text: "arXiv (API)", options: cl }, { text: "49", options: clR }],
    [{ text: "OpenAlex (API)", options: al }, { text: "1,222", options: alR }],
  ], {
    x: 0.6, y: 2.9, w: 5.0,
    colW: [3.2, 1.8],
    border: { pt: 0.5, color: "CBD5E1" },
    rowH: [0.38, 0.38, 0.38, 0.38, 0.38],
  });

  // Dedup method note
  s.addText("Dedup: DOI match (40) + title+year match (29)", {
    x: 5.8, y: 3.5, w: 3.6, h: 0.5,
    fontFace: FONT_B, fontSize: 12, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 7 — PRISMA Flow (dark)
// ════════════════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: C.dark };

  s.addText("PRISMA Flow — Identification Phase", {
    x: 0.6, y: 0.25, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: 28, color: C.white, bold: true, margin: 0,
  });

  // Identification box
  s.addShape(pres.shapes.RECTANGLE, { x: 1.5, y: 1.0, w: 7.0, h: 2.7, fill: { color: C.primary }, shadow: cardShadow() });
  s.addText("IDENTIFICATION", {
    x: 1.5, y: 1.05, w: 7.0, h: 0.4,
    fontFace: FONT_B, fontSize: 14, color: C.accent, bold: true, align: "center", margin: 0,
  });

  const sources = [
    { name: "IEEE Xplore", count: "386", xx: 1.8 },
    { name: "Web of Science", count: "50", xx: 3.6 },
    { name: "arXiv", count: "49", xx: 5.4 },
    { name: "OpenAlex", count: "1,222", xx: 7.0 },
  ];

  sources.forEach((src) => {
    s.addShape(pres.shapes.RECTANGLE, { x: src.xx, y: 1.55, w: 1.4, h: 0.9, fill: { color: C.dark } });
    s.addText(src.count, {
      x: src.xx, y: 1.55, w: 1.4, h: 0.55,
      fontFace: FONT_H, fontSize: 22, color: C.accent, bold: true, align: "center", margin: 0,
    });
    s.addText(src.name, {
      x: src.xx, y: 2.1, w: 1.4, h: 0.3,
      fontFace: FONT_B, fontSize: 10, color: C.muted, align: "center", margin: 0,
    });
  });

  s.addText("Total records identified: 1,707", {
    x: 1.5, y: 2.6, w: 7.0, h: 0.4,
    fontFace: FONT_B, fontSize: 16, color: C.white, bold: true, align: "center", margin: 0,
  });

  // Arrow down
  s.addText("\u25BC", {
    x: 4.5, y: 3.7, w: 1.0, h: 0.4,
    fontFace: FONT_B, fontSize: 24, color: C.accent, align: "center", margin: 0,
  });

  // Dedup box
  s.addShape(pres.shapes.RECTANGLE, { x: 2.5, y: 3.95, w: 5.0, h: 0.55, fill: { color: C.primary }, shadow: cardShadow() });
  s.addText("Duplicates removed: 69  (DOI: 40  |  Title+Year: 29)", {
    x: 2.5, y: 3.95, w: 5.0, h: 0.55,
    fontFace: FONT_B, fontSize: 13, color: C.white, align: "center", valign: "middle", margin: 0,
  });

  // Arrow down
  s.addText("\u25BC", {
    x: 4.5, y: 4.5, w: 1.0, h: 0.35,
    fontFace: FONT_B, fontSize: 24, color: C.accent, align: "center", margin: 0,
  });

  // Records to screen
  s.addShape(pres.shapes.RECTANGLE, { x: 2.5, y: 4.75, w: 5.0, h: 0.6, fill: { color: C.accent } });
  s.addText("Records to screen: 1,638", {
    x: 2.5, y: 4.75, w: 5.0, h: 0.6,
    fontFace: FONT_B, fontSize: 18, color: C.dark, bold: true, align: "center", valign: "middle", margin: 0,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 8 — Progress Tracker (light)
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
    { step: "4", label: "Search execution + deduplication", status: "current" },
    { step: "5", label: "Title/abstract screening", status: "next" },
    { step: "6-8", label: "Extraction, quality assessment, synthesis", status: "todo" },
    { step: "9-12", label: "Reference implementation + experiments", status: "todo" },
  ];

  steps.forEach((item, i) => {
    const yy = 1.15 + i * 0.58;
    const isDone = item.status === "done";
    const isCurrent = item.status === "current";
    const isNext = item.status === "next";

    // Step number circle
    const circleColor = isDone ? C.done : isCurrent ? C.accent : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.OVAL, { x: 0.7, y: yy + 0.05, w: 0.4, h: 0.4, fill: { color: circleColor } });
    s.addText(item.step, {
      x: 0.7, y: yy + 0.05, w: 0.4, h: 0.4,
      fontFace: FONT_B, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });

    // Label
    s.addText(item.label, {
      x: 1.3, y: yy, w: 5.5, h: 0.48,
      fontFace: FONT_B, fontSize: 15, color: isDone ? C.muted : C.text,
      bold: isCurrent, valign: "middle", margin: 0,
    });

    // Status badge
    const badgeText = isDone ? "Done" : isCurrent ? "This week" : isNext ? "Next" : "Upcoming";
    const badgeColor = isDone ? C.done : isCurrent ? C.accent : isNext ? C.warn : C.todo;
    s.addShape(pres.shapes.RECTANGLE, { x: 7.5, y: yy + 0.08, w: 1.4, h: 0.34, fill: { color: badgeColor } });
    s.addText(badgeText, {
      x: 7.5, y: yy + 0.08, w: 1.4, h: 0.34,
      fontFace: FONT_B, fontSize: 11, color: C.white, bold: true, align: "center", valign: "middle", margin: 0,
    });
  });

  s.addText("All artifacts version-controlled in Git.", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontFace: FONT_B, fontSize: 12, color: C.muted, italic: true,
  });
}

// ════════════════════════════════════════════════════════════════
// SLIDE 9 — Next Steps (dark)
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
    { num: "01", title: "Title / abstract screening", desc: "Apply inclusion/exclusion criteria to 1,638 records. Two-reviewer independent screening." },
    { num: "02", title: "Full-text screening", desc: "Retrieve and assess shortlisted papers against full eligibility criteria." },
    { num: "03", title: "Record exclusion reasons", desc: "Document reasons per PRISMA flow. Complete the flow diagram." },
    { num: "04", title: "Data extraction template", desc: "Design extraction form: platform, consensus, governance, privacy, interoperability, metrics." },
  ];

  nextItems.forEach((item, i) => {
    const yy = 1.15 + i * 1.05;
    s.addShape(pres.shapes.RECTANGLE, { x: 0.6, y: yy, w: 8.8, h: 0.85, fill: { color: C.primary }, shadow: cardShadow() });
    // Number
    s.addText(item.num, {
      x: 0.8, y: yy + 0.1, w: 0.6, h: 0.65,
      fontFace: FONT_H, fontSize: 28, color: C.accent, bold: true, valign: "middle", margin: 0,
    });
    // Title
    s.addText(item.title, {
      x: 1.6, y: yy + 0.08, w: 7.5, h: 0.35,
      fontFace: FONT_B, fontSize: 15, color: C.white, bold: true, margin: 0,
    });
    // Description
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
pres.writeFile({ fileName: "slides/weekly-progress-2026-04-14.pptx" })
  .then(() => console.log("Created: slides/weekly-progress-2026-04-14.pptx"))
  .catch(err => console.error(err));
