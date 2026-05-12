const path = require('path');
const PptxGenJS = require('pptxgenjs');

const outputPath = path.join(
  __dirname,
  '..',
  'slides',
  'week11-progress-2026-05-12.pptx'
);

function addHeader(slide, title, subtitle) {
  slide.addText(title, {
    x: 0.5,
    y: 0.3,
    w: 12.3,
    h: 0.45,
    fontFace: 'Aptos Display',
    fontSize: 24,
    bold: true,
    color: '16324F'
  });

  if (subtitle) {
    slide.addText(subtitle, {
      x: 0.52,
      y: 0.78,
      w: 12,
      h: 0.25,
      fontFace: 'Aptos',
      fontSize: 10,
      color: '4F5D75'
    });
  }

  slide.addShape(pptx.ShapeType.line, {
    x: 0.5,
    y: 1.08,
    w: 12.2,
    h: 0,
    line: { color: 'D9E2EC', pt: 1.2 }
  });
}

function addFooter(slide, index) {
  slide.addText(`Blockchain Consortium Networks SLR | Week 11 | ${index}`, {
    x: 0.5,
    y: 6.95,
    w: 12,
    h: 0.2,
    fontFace: 'Aptos',
    fontSize: 8,
    color: '6B7280',
    align: 'right'
  });
}

function addBullets(slide, items, opts = {}) {
  const runs = [];

  items.forEach((item, idx) => {
    runs.push({
      text: item,
      options: {
        bullet: { indent: 18 },
        breakLine: idx < items.length - 1,
        hanging: 2,
        paraSpaceAfterPt: 10
      }
    });
  });

  slide.addText(runs, {
    x: opts.x ?? 0.8,
    y: opts.y ?? 1.5,
    w: opts.w ?? 5.6,
    h: opts.h ?? 4.8,
    fontFace: 'Aptos',
    fontSize: opts.fontSize ?? 18,
    color: '1F2937',
    valign: 'top',
    margin: 0.05,
    fit: 'shrink'
  });
}

function addCallout(slide, title, body, x, y, w, h, fill) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x,
    y,
    w,
    h,
    rectRadius: 0.08,
    fill: { color: fill },
    line: { color: fill }
  });
  slide.addText(title, {
    x: x + 0.18,
    y: y + 0.14,
    w: w - 0.36,
    h: 0.3,
    fontFace: 'Aptos',
    fontSize: 15,
    bold: true,
    color: '16324F'
  });
  slide.addText(body, {
    x: x + 0.18,
    y: y + 0.48,
    w: w - 0.36,
    h: h - 0.58,
    fontFace: 'Aptos',
    fontSize: 13,
    color: '1F2937',
    margin: 0.02,
    fit: 'shrink'
  });
}

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'GitHub Copilot';
pptx.company = 'Kumoh National Institute of Technology';
pptx.subject = 'Week 11 progress report';
pptx.title = 'Week 11 progress update';
pptx.lang = 'en-US';

async function main() {
  let slide = pptx.addSlide();
  slide.background = { color: 'F8FAFC' };
  slide.addShape(pptx.ShapeType.rect, {
    x: 0,
    y: 0,
    w: 13.333,
    h: 1.4,
    line: { color: '16324F', pt: 0 },
    fill: { color: '16324F' }
  });
  slide.addText('Blockchain Utilization in Institutional Consortium Networks', {
    x: 0.55,
    y: 0.45,
    w: 9.8,
    h: 0.5,
    fontFace: 'Aptos Display',
    fontSize: 26,
    bold: true,
    color: 'FFFFFF'
  });
  slide.addText('Week 11 progress report', {
    x: 0.55,
    y: 1.75,
    w: 4.8,
    h: 0.38,
    fontFace: 'Aptos Display',
    fontSize: 22,
    bold: true,
    color: '16324F'
  });
  slide.addText('Covers work completed since week 9 (2026-04-28 to 2026-05-12)', {
    x: 0.58,
    y: 2.2,
    w: 6.2,
    h: 0.28,
    fontFace: 'Aptos',
    fontSize: 13,
    color: '4F5D75'
  });
  addCallout(
    slide,
    'Why week 11',
    'There was no class in week 10 because of public holidays, so this deck rolls up the full delta since the week 9 presentation.',
    0.58,
    2.75,
    5.7,
    1.2,
    'E8F1FB'
  );
  addCallout(
    slide,
    'Delta at a glance',
    '8 commits\n27 files changed\n5,895 insertions / 1,624 deletions\nNew scripts, synthesis tables, manuscript results, and slides',
    6.55,
    1.75,
    5.8,
    2.2,
    'EEF7E9'
  );
  addBullets(
    slide,
    [
      'Paper builds cleanly after PRISMA LaTeX fix and manuscript consolidation.',
      'Evidence synthesis outputs now quantify RQ1-RQ4 using generated CSV tables.',
      'A real PowerPoint artifact is produced for this week instead of a markdown draft.'
    ],
    { x: 0.75, y: 4.25, w: 11.8, h: 2.2, fontSize: 18 }
  );
  addFooter(slide, 1);

  slide = pptx.addSlide();
  slide.background = { color: 'FFFFFF' };
  addHeader(slide, 'Commit scope since 2026-04-28', 'New work included in the week 11 report');
  slide.addTable(
    [
      [{ text: 'Commit' }, { text: 'Main change' }],
      ['1739130 / 3fb5538 / 4a21b0d / dc0c3f7 / cc08810', 'Consolidated manuscript into paper/paper.tex and removed placeholder or duplicate sources.'],
      ['1e35719', 'Ignored local full-text corpus files to keep the repo lean and avoid accidental full-text commits.'],
      ['2260bc6', 'Fixed PRISMA LaTeX break and refined the manuscript structure.'],
      ['1ff9d13', 'Added automation for full-text recovery, author-email generation, extraction, and synthesis.'],
      ['fbf8f28', 'Added processed synthesis CSVs and markdown evidence reports.'],
      ['021e5cb', 'Expanded the paper with quantified tables, metric ranges, and explicit gaps across RQ1-RQ4.']
    ],
    {
      x: 0.55,
      y: 1.45,
      w: 12.1,
      h: 4.8,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      color: '1F2937',
      fontFace: 'Aptos',
      fontSize: 11,
      rowH: 0.58,
      autoFit: true,
      valign: 'mid',
      margin: 0.05,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  addFooter(slide, 2);

  slide = pptx.addSlide();
  slide.background = { color: 'F8FAFC' };
  addHeader(slide, 'Repository and data pipeline updates', 'Automation and evidence assets added after week 9');
  addCallout(slide, 'New automation scripts', 'download_tierab_fulltexts.py\nrecover_oa_unpaywall.py\nextract_tierab_data.py\ngenerate_author_emails.py\nsynthesize_evidence.py', 0.65, 1.45, 3.8, 2.55, 'E8F1FB');
  addCallout(slide, 'New processed outputs', 'synthesis_rq1_taxonomy.csv\nsynthesis_rq2_tradeoffs.csv\nsynthesis_rq3_interop.csv\nsynthesis_rq4_gaps.csv\nsynthesis_domain_platform.csv', 4.75, 1.45, 3.8, 2.55, 'EEF7E9');
  addCallout(slide, 'New reports', 'synthesis_report.md\nunpaywall_recovery_report.md\nextraction_tierab_report.md\ntierab_download_report.md\ntier_a_paywalled_contacts.md', 8.85, 1.45, 3.8, 2.55, 'FFF3E8');
  addBullets(
    slide,
    [
      '95 tier A/B papers now have recovered or extracted full-text evidence for deeper synthesis.',
      'Tier A paywalled papers are now tracked through a dedicated contacts file for author outreach.',
      'The processed evidence layer is now reproducible from scripts instead of ad hoc manual notes.'
    ],
    { x: 0.72, y: 4.4, w: 11.9, h: 2.1, fontSize: 18 }
  );
  addFooter(slide, 3);

  slide = pptx.addSlide();
  slide.background = { color: 'FFFFFF' };
  addHeader(slide, 'Manuscript changes since week 9', 'The paper moved from draft consolidation to quantified synthesis');
  addBullets(
    slide,
    [
      'Removed legacy main.tex and main.overleaf.tex and centralized the active manuscript in paper/paper.tex.',
      'Fixed the generated PRISMA figure and its generator so escaped underscores no longer break the LaTeX build.',
      'Updated references.bib and removed unverified placeholder citations.',
      'Expanded Results with new tables for network models, privacy mechanisms, metric coverage, interoperability patterns, and artifact availability.'
    ],
    { x: 0.75, y: 1.5, w: 6.1, h: 4.7, fontSize: 19 }
  );
  addCallout(slide, 'Build status', 'paper.tex now compiles successfully with latexmk after the PRISMA fix. The current PDF is 12 pages and includes the new quantified tables.', 7.2, 1.55, 5.2, 1.55, 'E8F1FB');
  addCallout(slide, 'Evidence integration', 'The paper now cites actual extracted ranges instead of generic claims: throughput 3-1700 TPS and latency from 1 ms up to 250+ seconds.', 7.2, 3.35, 5.2, 1.55, 'EEF7E9');
  addCallout(slide, 'Quality framing', 'Study quality distribution is now explicit: Tier A 26, Tier B 122, Tier C 110, Tier D 21.', 7.2, 5.15, 5.2, 0.95, 'FFF3E8');
  addFooter(slide, 4);

  slide = pptx.addSlide();
  slide.background = { color: 'F8FAFC' };
  addHeader(slide, 'New synthesis evidence now in the paper', 'RQ1 and RQ2 highlights extracted from the processed tables');
  slide.addTable(
    [
      [{ text: 'RQ1 taxonomy highlight' }, { text: 'Value' }],
      ['Hyperledger Fabric studies', '80'],
      ['Ethereum studies', '81'],
      ['Consortium network model', '79'],
      ['Top privacy mechanisms', 'ZKP 25, homomorphic encryption 24, private channels 18']
    ],
    {
      x: 0.6,
      y: 1.45,
      w: 5.8,
      h: 2.7,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      fontFace: 'Aptos',
      fontSize: 12,
      margin: 0.04,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  slide.addTable(
    [
      [{ text: 'RQ2 evidence highlight' }, { text: 'Value' }],
      ['Studies reporting throughput', '23 (8 percent of corpus)'],
      ['Studies reporting latency', '33 (11 percent of corpus)'],
      ['Typical Fabric CFT throughput', '50-300 TPS'],
      ['Observed throughput range', '3-1700 TPS'],
      ['Observed latency range', '1 ms to 250+ s']
    ],
    {
      x: 6.75,
      y: 1.45,
      w: 5.95,
      h: 3.05,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      fontFace: 'Aptos',
      fontSize: 12,
      margin: 0.04,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  addBullets(
    slide,
    [
      'Fabric dominates institutional deployment maturity, but Ethereum remains heavily represented in the broader literature.',
      'Only a small minority of studies publish performance numbers, which limits direct comparison across platforms.',
      'The paper now reports ranges rather than single-point claims to reflect institutional workload variability.'
    ],
    { x: 0.72, y: 4.8, w: 12.0, h: 1.7, fontSize: 17 }
  );
  addFooter(slide, 5);

  slide = pptx.addSlide();
  slide.background = { color: 'FFFFFF' };
  addHeader(slide, 'RQ3 and RQ4 findings added this cycle', 'Interoperability and reproducibility now have explicit counts');
  slide.addTable(
    [
      [{ text: 'Interoperability pattern' }, { text: 'Studies' }],
      ['Cross-chain bridge', '25'],
      ['Oracle-mediated', '11'],
      ['Message queue / broker', '7'],
      ['API gateway', '6'],
      ['Relay / notary', '5']
    ],
    {
      x: 0.6,
      y: 1.45,
      w: 5.6,
      h: 2.85,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      fontFace: 'Aptos',
      fontSize: 12,
      margin: 0.04,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  slide.addTable(
    [
      [{ text: 'Artifact availability' }, { text: 'Studies' }],
      ['Code / GitHub', '35'],
      ['Config / deployment files', '18'],
      ['Dataset', '6'],
      ['No reusable artifact', '220']
    ],
    {
      x: 6.55,
      y: 1.45,
      w: 5.7,
      h: 2.5,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      fontFace: 'Aptos',
      fontSize: 12,
      margin: 0.04,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  addBullets(
    slide,
    [
      'Only 48 of 279 included studies describe explicit interoperability patterns; most still assume isolated deployments.',
      'API gateways and oracle-based integrations appear more institution-ready than trust-minimized bridge proposals.',
      'The paper now names five systematic gaps: benchmarking, governance formalization, interoperability specification, privacy-performance quantification, and deployment reproducibility.'
    ],
    { x: 0.72, y: 4.45, w: 12.0, h: 1.9, fontSize: 17 }
  );
  addFooter(slide, 6);

  slide = pptx.addSlide();
  slide.background = { color: 'F8FAFC' };
  addHeader(slide, 'What changed in the repository outputs', 'Concrete artifacts produced between week 9 and week 11');
  addBullets(
    slide,
    [
      'Added 5 synthesis and cross-tab CSVs under data/processed for RQ1-RQ4 evidence.',
      'Added 5 markdown reports under data/reports documenting recovery, extraction, contacts, and synthesis.',
      'Updated data_extraction_includes.csv and fulltext_screening.csv to reflect new extraction and screening state.',
      'Added a new slide deck artifact for week 11 in the expected PPTX format.'
    ],
    { x: 0.78, y: 1.55, w: 7.0, h: 4.5, fontSize: 20 }
  );
  addCallout(slide, 'Processed scope', '279 included studies in synthesis tables\n95 Tier A/B papers with full-text extraction coverage\nTier A paywalled contact list prepared for follow-up', 8.15, 1.75, 4.1, 1.9, 'E8F1FB');
  addCallout(slide, 'Research posture', 'The repo is now set up for reproducible evidence synthesis rather than just a manuscript draft. The next step is author confirmation and quality rescoring.', 8.15, 4.05, 4.1, 1.9, 'EEF7E9');
  addFooter(slide, 7);

  slide = pptx.addSlide();
  slide.background = { color: 'FFFFFF' };
  addHeader(slide, 'Next actions after week 11', 'Immediate follow-up for the next reporting cycle');
  slide.addTable(
    [
      [{ text: 'Task' }, { text: 'Target' }, { text: 'Status' }],
      ['Author-level confirmation of provisional includes', 'Week 12', 'Pending'],
      ['Full-text quality rescoring for Tier A/B paywalled studies', 'Week 12', 'Pending'],
      ['Complete abstract-based extraction for remaining studies', 'Week 12-13', 'Pending'],
      ['Draft Discussion and Limitations section', 'Week 13', 'Not started'],
      ['Journal targeting and submission prep', 'Week 14', 'Not started']
    ],
    {
      x: 0.6,
      y: 1.45,
      w: 12.0,
      h: 3.2,
      border: { type: 'solid', color: 'D9E2EC', pt: 1 },
      fill: 'FFFFFF',
      fontFace: 'Aptos',
      fontSize: 12,
      margin: 0.04,
      bold: true,
      fillHeader: '16324F',
      colorHeader: 'FFFFFF'
    }
  );
  addBullets(
    slide,
    [
      'Use the week-11 tag as the baseline for the next class report.',
      'Compare new work with git diff week-11..HEAD or week-11 to the next weekly tag.',
      'The strongest short-term manuscript gain is a Discussion section that interprets the quantified gaps now added to Results.'
    ],
    { x: 0.78, y: 5.0, w: 11.7, h: 1.35, fontSize: 18 }
  );
  addFooter(slide, 8);

  await pptx.writeFile({ fileName: outputPath });
  console.log(`Wrote ${outputPath}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});