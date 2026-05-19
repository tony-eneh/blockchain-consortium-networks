// Week-12 progress deck - Week-9-inspired visual system
// Run: node scripts/generate_week12_presentation.js
const pptxgen = require("pptxgenjs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Tony Eneh";
pres.title = "Blockchain Consortium Networks SLR - Week 12 Progress";
pres.subject = "Week 12 progress report";

const outputPath = path.join(__dirname, "..", "slides", "week12-progress-2026-05-19.pptx");

const C = {
  dark: "0B1D26",
  primary: "0D4F5C",
  accent: "14B8A6",
  light: "E8F5F3",
  white: "FFFFFF",
  text: "1E293B",
  muted: "64748B",
  card: "F0FDFA",
  done: "10B981",
  todo: "94A3B8",
  red: "EF4444",
  amber: "F59E0B",
  blue: "0EA5E9",
};

const FONT_H = "Cambria";
const FONT_B = "Calibri";
const cardShadow = () => ({ type: "outer", color: "000000", blur: 6, offset: 2, angle: 135, opacity: 0.10 });

function addRail(slide) {
  slide.background = { color: C.white };
  slide.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 0.12, h: 5.625, fill: { color: C.accent } });
}

function addTitle(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.6, y: 0.3, w: 9, h: 0.6,
    fontFace: FONT_H, fontSize: title.length > 38 ? 24 : 30,
    color: C.primary, bold: true, margin: 0,
  });
  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.62, y: 0.86, w: 8.8, h: 0.25,
      fontFace: FONT_B, fontSize: 11, color: C.muted, margin: 0,
    });
  }
}

function addFooter(slide, n) {
  slide.addText(`Week 12 Progress | Blockchain Consortium Networks SLR | ${n}`, {
    x: 0.6, y: 5.35, w: 8.8, h: 0.18,
    fontFace: FONT_B, fontSize: 8, color: C.muted, align: "right", margin: 0,
  });
}

function addStatCards(slide, stats, y = 1.12) {
  stats.forEach((st, i) => {
    const xx = 0.6 + i * 3.1;
    const fill = st.white ? C.primary : C.card;
    const numCol = st.white ? C.white : st.color;
    const labCol = st.white ? C.light : C.muted;
    slide.addShape(pres.shapes.RECTANGLE, { x: xx, y, w: 2.8, h: 1.45, fill: { color: fill }, shadow: cardShadow() });
    if (!st.white) slide.addShape(pres.shapes.RECTANGLE, { x: xx, y, w: 2.8, h: 0.07, fill: { color: st.color } });
    slide.addText(st.num, {
      x: xx, y: y + 0.12, w: 2.8, h: 0.68,
      fontFace: FONT_H, fontSize: st.num.length > 6 ? 30 : 39,
      color: numCol, bold: true, align: "center", valign: "middle", margin: 0,
    });
    slide.addText(st.label, {
      x: xx + 0.08, y: y + 0.84, w: 2.64, h: 0.4,
      fontFace: FONT_B, fontSize: 12, color: labCol,
      align: "center", margin: 0, fit: "shrink",
    });
  });
}

function addCard(slide, x, y, w, h, title, body, color = C.card) {
  slide.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color }, shadow: cardShadow() });
  slide.addText(title, {
    x: x + 0.18, y: y + 0.12, w: w - 0.36, h: 0.3,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  slide.addText(body, {
    x: x + 0.18, y: y + 0.52, w: w - 0.36, h: h - 0.62,
    fontFace: FONT_B, fontSize: 12.3, color: C.text,
    lineSpacingMultiple: 1.25, margin: 0.02, fit: "shrink",
  });
}

function addBarList(slide, title, rows, x, y, w, max, color) {
  slide.addText(title, {
    x, y, w, h: 0.28,
    fontFace: FONT_B, fontSize: 14, color: C.primary, bold: true, margin: 0,
  });
  rows.forEach((row, i) => {
    const yy = y + 0.42 + i * 0.42;
    slide.addText(row.label, {
      x, y: yy, w: w * 0.48, h: 0.33,
      fontFace: FONT_B, fontSize: 11, color: C.text, valign: "middle", margin: 0,
      fit: "shrink",
    });
    const barW = Math.max(0.05, (row.n / max) * (w * 0.34));
    slide.addShape(pres.shapes.RECTANGLE, { x: x + w * 0.5, y: yy + 0.08, w: barW, h: 0.18, fill: { color } });
    slide.addText(`${row.n}`, {
      x: x + w * 0.5 + barW + 0.06, y: yy, w: 0.65, h: 0.33,
      fontFace: FONT_B, fontSize: 11, color: C.text, bold: true, valign: "middle", margin: 0,
    });
  });
}

// SLIDE 1 - Title
{
  const s = pres.addSlide();
  s.background = { color: C.dark };
  s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.06, fill: { color: C.accent } });
  s.addText("Blockchain Utilization Strategies\nin Institutional Consortium Networks", {
    x: 0.8, y: 0.78, w: 8.4, h: 2.0,
    fontFace: FONT_H, fontSize: 36, color: C.white, bold: true, lineSpacingMultiple: 1.15,
  });
  s.addText("PRISMA 2020 Systematic Review - Week 12 Progress", {
    x: 0.8, y: 2.9, w: 8.4, h: 0.5,
    fontFace: FONT_B, fontSize: 18, color: C.accent, italic: true,
  });
  s.addText([
    { text: "Tony Eneh", options: { bold: true, breakLine: true } },
    { text: "Networked Systems Laboratory (NSL)", options: { breakLine: true } },
    { text: "Kumoh National Institute of Technology (KIT)", options: { breakLine: true } },
    { text: "May 19, 2026" },
  ], {
    x: 0.8, y: 3.72, w: 8.4, h: 1.2,
    fontFace: FONT_B, fontSize: 13, color: C.muted, lineSpacingMultiple: 1.4,
  });
}

// SLIDE 2 - Where we left off
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Where We Left Off (Week 11)", "The corpus counts stayed stable; this week focused on making the manuscript and tracker more defensible.");
  addStatCards(s, [
    { num: "279", label: "Included studies", color: C.done, white: true },
    { num: "95", label: "Full-text extractions", color: C.accent },
    { num: "184", label: "Abstract-only signals", color: C.amber },
  ]);
  addCard(s, 0.6, 3.05, 8.8, 1.95, "Open issues carried into Week 12", "1.  Agent-assisted screening still needs author-level validation.\n2.  Screening-stage quality tiers must be replaced by full-text scores.\n3.  Throughput / latency captures need unit and workload checks before citation.\n4.  The paper needs clearer limitations around OpenAlex substitution and open-access bias.");
  addFooter(s, 2);
}

// SLIDE 3 - This week's actual work
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "This Week's Work", "Git history over the last 6 days: 2 commits, focused on paper support and project-state correction.");
  addStatCards(s, [
    { num: "2", label: "Commits since May 13", color: C.primary, white: true },
    { num: "+496", label: "Reference lines added", color: C.blue },
    { num: "+33/-19", label: "TODO refresh delta", color: C.accent },
  ]);
  addCard(s, 0.6, 3.05, 4.25, 1.95, "Commit 5e8ee3e", "Added extensive references.\n\npaper/references.bib expanded substantially; paper.tex gained citation support for domain examples, privacy, governance, and interoperability claims.", C.light);
  addCard(s, 5.1, 3.05, 4.3, 1.95, "Commit c043af0", "Updated screening progress.\n\nTODO.md now separates completed artifact generation from remaining publication-validation work.", C.card);
  addFooter(s, 3);
}

// SLIDE 4 - Timeline
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Progress Timeline (Weeks 1-12)", "Week 12 is a manuscript-hardening checkpoint, not a new screening pipeline stage.");
  const timeline = [
    { week: "1-2", label: "RQs + PICOC", status: "done" },
    { week: "3-4", label: "Protocol + search", status: "done" },
    { week: "5-6", label: "Search + dedup", status: "done" },
    { week: "7-8", label: "Screening", status: "done" },
    { week: "9", label: "Quality + extraction", status: "done" },
    { week: "11", label: "Synthesis + paper", status: "done" },
    { week: "12", label: "Manuscript hardening", status: "current" },
  ];
  s.addShape(pres.shapes.RECTANGLE, { x: 0.72, y: 1.42, w: 8.5, h: 0.08, fill: { color: C.accent } });
  timeline.forEach((item, i) => {
    const xx = 0.72 + i * (8.5 / (timeline.length - 1));
    const isCurrent = item.status === "current";
    const size = isCurrent ? 0.46 : 0.34;
    s.addShape(pres.shapes.OVAL, {
      x: xx - size / 2, y: 1.46 - size / 2, w: size, h: size,
      fill: { color: isCurrent ? C.accent : C.done },
    });
    s.addText(item.week, {
      x: xx - 0.72, y: 1.78, w: 1.44, h: 0.25,
      fontFace: FONT_B, fontSize: 12, color: C.primary, bold: true, align: "center", margin: 0,
    });
    s.addText(item.label, {
      x: xx - 0.72, y: 2.05, w: 1.44, h: 0.55,
      fontFace: FONT_B, fontSize: 10.3, color: C.text, align: "center", margin: 0, fit: "shrink",
    });
  });
  addCard(s, 0.6, 3.05, 8.8, 2.0, "Week 12 checkpoint", "The paper is no longer just accumulating material. The work this week clarified what is already artifact-backed and what still needs validation: human spot-checking, Tier A/B full-text rescoring, and metric verification. This makes the next report easier to defend.");
  addFooter(s, 4);
}

// SLIDE 5 - Current review state
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Current Review State", "These are the counts now made explicit in TODO.md.");
  addStatCards(s, [
    { num: "863", label: "Full-text candidates", color: C.primary, white: true },
    { num: "279", label: "Included", color: C.done },
    { num: "584", label: "Excluded", color: C.red },
  ]);
  addBarList(s, "Top exclusion buckets", [
    { label: "insufficient full text", n: 281 },
    { label: "no full text access", n: 210 },
    { label: "second-pass exclude", n: 48 },
    { label: "agent uncertain", n: 32 },
  ], 0.7, 3.0, 4.15, 281, C.red);
  addBarList(s, "Quality tiers (screening-stage)", [
    { label: "Tier A", n: 26 },
    { label: "Tier B", n: 122 },
    { label: "Tier C", n: 110 },
    { label: "Tier D", n: 21 },
  ], 5.15, 3.0, 4.15, 122, C.accent);
  s.addText("Caveat: quality tiers are still title/abstract/source-derived signals, not final full-text scores.", {
    x: 0.7, y: 5.05, w: 8.5, h: 0.3,
    fontFace: FONT_B, fontSize: 10.5, color: C.muted, italic: true, align: "center",
  });
  addFooter(s, 5);
}

// SLIDE 6 - Evidence snapshot
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Evidence Snapshot", "The synthesis numbers did not change this week; the interpretation became stricter.");
  addBarList(s, "Metric and evaluation coverage", [
    { label: "Evaluation setup", n: 80 },
    { label: "Fault tolerance", n: 48 },
    { label: "Latency", n: 33 },
    { label: "Throughput", n: 23 },
  ], 0.7, 1.18, 4.15, 80, C.blue);
  addBarList(s, "Reproducibility signals", [
    { label: "Code artifact", n: 35 },
    { label: "Config/deployment", n: 18 },
    { label: "Dataset", n: 6 },
  ], 5.15, 1.18, 4.15, 35, C.accent);
  addCard(s, 0.65, 3.75, 8.75, 1.15, "How this changes the paper", "The manuscript should present these as evidence-coverage gaps, not as final performance laws. This framing makes the reference implementation motivation much stronger.", C.light);
  addFooter(s, 6);
}

// SLIDE 7 - What improved in the manuscript
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Manuscript Hardening", "The week's biggest visible change is stronger citation coverage.");
  addCard(s, 0.6, 1.15, 4.25, 1.45, "Reference base expanded", "paper/references.bib grew by nearly 500 lines, improving support for the taxonomy, application-domain examples, privacy mechanisms, and interoperability discussion.", C.light);
  addCard(s, 5.1, 1.15, 4.3, 1.45, "Paper claims better anchored", "paper.tex gained targeted reference updates so Results and Discussion are less dependent on generic blockchain survey claims.", C.card);
  addCard(s, 0.6, 3.0, 4.25, 1.45, "Tracker now more honest", "TODO.md now states 95 full-text extractions, 184 abstract-only signals, screening-stage tiers, and the need to verify metric captures.", C.card);
  addCard(s, 5.1, 3.0, 4.3, 1.45, "Remaining risk named", "The plan now calls out OpenAlex substitution, open-access bias, missing human adjudication, and heuristic extraction as limitations to address.", C.light);
  addFooter(s, 7);
}

// SLIDE 8 - Progress tracker
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Progress Tracker", "Updated after the Week 12 TODO refresh.");
  const steps = [
    { step: "1", label: "RQs + PICOC scope", status: "done" },
    { step: "2", label: "Protocol draft", status: "done" },
    { step: "3", label: "Search strings", status: "done" },
    { step: "4", label: "Search + dedup", status: "done" },
    { step: "5", label: "Agent screening complete; human validation pending", status: "current" },
    { step: "6", label: "Extraction bootstrap + partial full text", status: "current" },
    { step: "7", label: "Screening-stage quality rubric", status: "current" },
    { step: "8", label: "Synthesis bootstrapped; verify before publication", status: "current" },
    { step: "9", label: "Reference implementation", status: "next" },
  ];
  steps.forEach((item, i) => {
    const yy = 1.0 + i * 0.45;
    const isDone = item.status === "done";
    const isCurrent = item.status === "current";
    const fill = isDone ? C.done : isCurrent ? C.accent : C.todo;
    s.addShape(pres.shapes.OVAL, { x: 0.75, y: yy + 0.02, w: 0.28, h: 0.28, fill: { color: fill } });
    s.addText(item.step, {
      x: 0.74, y: yy + 0.045, w: 0.3, h: 0.2,
      fontFace: FONT_B, fontSize: 8, color: C.white, bold: true, align: "center", margin: 0,
    });
    s.addShape(pres.shapes.RECTANGLE, { x: 1.15, y: yy, w: 7.7, h: 0.34, fill: { color: isDone ? "ECFDF5" : isCurrent ? C.card : "F1F5F9" } });
    s.addText(item.label, {
      x: 1.28, y: yy + 0.06, w: 7.35, h: 0.22,
      fontFace: FONT_B, fontSize: 12, color: C.text, margin: 0, fit: "shrink",
    });
  });
  addFooter(s, 8);
}

// SLIDE 9 - Next week
{
  const s = pres.addSlide();
  addRail(s);
  addTitle(s, "Next Actions for Week 13", "Move from artifact-backed draft to defensible SLR manuscript.");
  addCard(s, 0.6, 1.08, 8.8, 3.7, "Priority queue", "1.  Complete the 40-row human spot-check and compute agreement.\n2.  Full-text rescore the 148 Tier A/B candidates.\n3.  Verify throughput, latency, and fault-tolerance metric captures.\n4.  Revise Methods and Limitations around OpenAlex, access bias, and agent triage.\n5.  Simplify dense IEEE tables causing overfull boxes.", C.card);
  s.addText("Goal: make the strongest claims traceable to validated evidence, not just generated artifacts.", {
    x: 0.8, y: 4.95, w: 8.4, h: 0.35,
    fontFace: FONT_B, fontSize: 13, color: C.primary, bold: true, align: "center", margin: 0,
  });
  addFooter(s, 9);
}

pres.writeFile({ fileName: outputPath });
console.log(`Wrote ${outputPath}`);
