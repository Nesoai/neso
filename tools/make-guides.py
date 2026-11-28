"""Build nesohq.com/guides/: one how-to page per free tool (a principal, 27 Nov 2026), for people who search the question
the tool answers. Each page answers the question in plain words, works one example with real arithmetic, says what to
have ready, then hands off to the tool (?source=guide). No price, no "Pro", no principal's name, no operating state,
no legal, tax or investment advice.
    python3 make.py /home/claude/neso
"""
import html
import json
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1]) / "guides"
DATE = "2026-11-27"


def money(x):
    return f"${x:,.0f}"


# worked numbers (computed, not typed)
R = 0.07 / 12
N = 360
CONST = R / (1 - (1 + R) ** -N) * 12                       # annual debt constant, 7%, 30 years
cap_noi, cap_tdc, cap_eq, cap_grant = 260000, 4000000, 400000, 250000
cap_ds = cap_noi / 1.25
cap_loan = cap_ds / CONST
cap_gap = cap_tdc - cap_loan - cap_eq - cap_grant
pf_units, pf_rent = 12, 1100
pf_gpr = pf_units * pf_rent * 12
pf_vac = pf_gpr * 0.06
pf_egi0 = pf_gpr - pf_vac
pf_oth = pf_egi0 * 0.02
pf_egi = pf_egi0 + pf_oth
pf_opex = pf_egi * 0.40
pf_noi = pf_egi - pf_opex
pf_loan = 1200000
pf_ds = pf_loan * CONST
pf_dscr = pf_noi / pf_ds
pf_maxloan = pf_noi / 1.25 / CONST
mf_hh, mf_freq, mf_spend, mf_rivals, mf_need = 8000, 12, 18, 5, 300000
mf_pie = mf_hh * mf_freq * mf_spend
mf_share = mf_pie / (mf_rivals + 1)
pl_sale, pl_cost, pl_fixed = 60, 0.30, 9000
pl_contrib = pl_sale * (1 - pl_cost)
pl_be = pl_fixed / pl_contrib
ss_w, ss_d, ss_front, ss_rear, ss_side = 60, 140, 25, 20, 5
ss_bw, ss_bd = ss_w - 2 * ss_side, ss_d - ss_front - ss_rear
ss_foot = ss_bw * ss_bd
ms_units, ms_pace = 40, 3
ms_months = -(-ms_units // ms_pace)

G = [
 dict(slug="which-grants-fit", tool="GrantFit", url="https://grantfit.nesohq.com/",
      title="Which grants fit your organization? A 10-minute check",
      desc="How to tell which funding is worth applying for: match the funder to who you are, what the money is for, how much you need and where you are.",
      q="Which grants actually fit my organization?",
      a="The grant that fits is the one whose funder already pays for organizations like yours, for the purpose you have, at the size you need. Most rejected applications fail on fit, not on writing.",
      steps=[("Name what you are", "A nonprofit, a for-profit small business, a town or county, or a tribe. Many grants are open to only one kind, so this alone rules out most of the list."),
             ("Name what the money is for", "Operating costs, equipment, a building, research, training or a specific program. Funders pay for purposes, not for organizations in general."),
             ("Size the ask", "A $5,000 need and a $500,000 need go to different funders. A small foundation rarely funds a building; a federal program rarely bothers with a small equipment buy."),
             ("Be honest about your stage", "A new organization with no audited financials is a long shot for most federal grants and a fair shot for many local foundations."),
             ("Look at place and certifications", "Rural, distressed and Delta areas, and certifications such as minority-, women- or veteran-owned, open set-aside programs.")],
      example=("A two-year-old nonprofit wants $40,000 for a youth job-training program in a rural county.",
               ["Federal grants: possible, but the first federal award usually goes to organizations with audited financials and a track record.",
                "Local and regional foundations: a strong fit. Job training for young people in a rural county is what many community foundations fund.",
                "Corporate giving: a fair fit if a local employer hires the trainees.",
                "SBA and CDFI lending: not a fit. This is program money, not something to borrow against."]),
      ready=["What kind of organization you are and how long you have operated", "The purpose, in one sentence", "The amount", "Your county and state", "Any certifications you hold"],
      tool_line="GrantFit scores seven channels against your answers: federal grants, SBIR, state programs, foundations, corporate giving, SBA and CDFI lending, and crowdfunding. It runs in your browser, and nothing you enter leaves your device.",
      more="GrantFit's results are guidance from general program patterns, not a promise of funding or eligibility. Programs change; check each funder's current notice."),
 dict(slug="capital-stack-financing-gap", tool="CapStack", url="https://capstack.nesohq.com/",
      title="How to build a capital stack and find the financing gap",
      desc="A worked example: size the senior loan from the building's income, layer in equity and grants, and see the gap in dollars.",
      q="How do I find the financing gap on a real estate project?",
      a="Start from what the project costs, subtract what the bank will lend against its income, then subtract every other source you have. What is left is the gap, and naming it in dollars is the first step to closing it.",
      steps=[("Total the development cost", "Land, hard costs, soft costs and reserves: every dollar it takes to finish. This is the height the stack has to reach."),
             ("Size the senior loan from income", "A lender divides the building's net operating income by a coverage ratio (often 1.20 to 1.25) to get the most annual debt service it will accept, then turns that into a loan amount at its rate and term."),
             ("Add equity", "The sponsor's cash, and any investor equity."),
             ("Layer in the rest", "Tax credit equity, grants, soft loans from a city or state, and a deferred developer fee, in the order the deal can get them."),
             ("Name the gap", "Cost minus every source. If it is not zero, the deal needs another source, a lower cost, or more income.")],
      example=(f"A project costs {money(cap_tdc)}. Its stabilized NOI is {money(cap_noi)} a year. The sponsor has {money(cap_eq)} of equity and a {money(cap_grant)} grant.",
               [f"At a 1.25 coverage ratio, the most annual debt service is {money(cap_noi)} ÷ 1.25 = {money(cap_ds)}.",
                f"At 7% over 30 years, each dollar of loan costs about {CONST:.4f} a year, so the loan is {money(cap_ds)} ÷ {CONST:.4f} ≈ {money(cap_loan)}.",
                f"Sources so far: {money(cap_loan)} + {money(cap_eq)} + {money(cap_grant)} = {money(cap_loan + cap_eq + cap_grant)}.",
                f"Gap: {money(cap_tdc)} − {money(cap_loan + cap_eq + cap_grant)} ≈ {money(cap_gap)}. That is the amount to find in tax credits, soft loans or a deferred fee."]),
      ready=["Total development cost", "Stabilized net operating income, if the building earns rent", "Equity you have", "Any grants or soft loans already promised"],
      tool_line="CapStack sizes the senior loan from your NOI, lets you tap in each source (tax credits, grants, soft loans, a deferred developer fee, equity) and shows the gap, the blended cost of capital and how the stack fits together.",
      more="The rate, term and coverage ratio in the example are illustrations. A lender sets its own, and a tax credit's equity depends on the program and the market."),
 dict(slug="does-the-building-pay", tool="ProForma", url="https://proforma.nesohq.com/",
      title="Does the building pay? NOI and DSCR, worked out",
      desc="How to work out a building's net operating income and debt coverage ratio, the two numbers a lender checks first, with a worked 12-unit example.",
      q="How do I know if a rental building pays for its loan?",
      a="Work out the net operating income (rent collected minus the cost of running the building), then divide it by the yearly loan payments. That ratio, the DSCR, is the lender's first question; most want 1.20 to 1.25 or more.",
      steps=[("Gross rent", "Units × average rent × 12."),
             ("Take off vacancy", "Lenders usually assume 5% to 7% of rent is lost to empty units and unpaid rent, even in tight markets."),
             ("Add other income", "Laundry, parking, fees."),
             ("Take off operating costs", "Management, taxes, insurance, utilities, repairs and reserves. For apartments this often runs 35% to 45% of collected income. What is left is the NOI."),
             ("Divide by the loan payments", "NOI ÷ a year of principal and interest = DSCR. Below 1.00, the building does not cover its loan.")],
      example=(f"A {pf_units}-unit building rents at {money(pf_rent)} a unit a month, with 6% vacancy, other income of 2%, operating costs of 40%, and a {money(pf_loan)} loan at 7% over 30 years.",
               [f"Gross rent: {pf_units} × {money(pf_rent)} × 12 = {money(pf_gpr)}. Less 6% vacancy ({money(pf_vac)}) = {money(pf_egi0)}.",
                f"Plus 2% other income ({money(pf_oth)}) = {money(pf_egi)} collected.",
                f"Less 40% operating costs ({money(pf_opex)}) = NOI of {money(pf_noi)}.",
                f"Loan payments: about {money(pf_ds)} a year. DSCR = {money(pf_noi)} ÷ {money(pf_ds)} = {pf_dscr:.2f}.",
                f"At {pf_dscr:.2f} the building does not cover its loan. At a 1.25 ratio, this NOI supports a loan of about {money(pf_maxloan)}, so the deal needs more equity, more rent or lower costs."]),
      ready=["Number of units (or leasable square feet)", "Average rent", "Expected vacancy", "Operating costs, or a share of income", "Loan amount, rate and term"],
      tool_line="ProForma works out NOI, DSCR, yield on cost and cash-on-cash, and lays out a 10-year cash flow. It can pull a rent average from a MarketScope analysis.",
      more="The example's vacancy, costs and loan terms are illustrations; use your own, and a lender's actual terms."),
 dict(slug="lender-ready-market-study", tool="MarketScope", url="https://marketscope.nesohq.com/",
      title="What a lender-ready market study includes",
      desc="The parts an underwriter looks for in a market study, and how to show demand, comparables and absorption so every number can be checked.",
      q="What does a lender-ready market study include?",
      a="A defined trade area, its demographics and growth, where demand comes from, comparable properties with their rents or prices, how fast new space fills (absorption), and a plain conclusion. What makes it lender-ready is that an underwriter can rebuild every number from what is shown.",
      steps=[("Draw the trade area", "The area your tenants or buyers will come from, named on a map, not \"the region\"."),
             ("Show the people", "Population, households, income and growth for that area, from the Census and other public sources, with the source named."),
             ("Say where demand comes from", "Employers, new jobs, people moving in, or a shortage of a kind of space."),
             ("List the comparables", "Similar properties nearby, with rent or price per unit or square foot and occupancy."),
             ("Estimate absorption and conclude", "How many units the market takes a month, how long yours will take to fill, and what could go wrong.")],
      example=(f"A {ms_units}-unit apartment project in a town where comparable buildings have leased about {ms_pace} units a month.",
               [f"At {ms_pace} a month, {ms_units} units take about {ms_months} months to lease up ({ms_units} ÷ {ms_pace}, rounded up).",
                "The study shows the comparables that pace comes from, so the underwriter can check it.",
                "It also names the risks: a competing project in the pipeline, or an employer that might cut jobs."]),
      ready=["Project name, city or county, and type", "Size in units or square feet", "Total development cost", "Two to five comparable properties", "The risks you already see"],
      tool_line="MarketScope turns your inputs into a structured market analysis: trade area, demographics, demand, comparables and absorption. It can fold in a CapStack capital stack.",
      more="A market analysis is context for a decision, not an appraisal or a guarantee of lease-up."),
 dict(slug="lot-to-site-plan", tool="SiteShaper", url="https://siteshaper.nesohq.com/",
      title="From a lot to a site plan: setbacks and buildable area",
      desc="How to work out how much of a lot you can build on after setbacks, with a worked example, before you pay for a survey or a design.",
      q="How much of my lot can I actually build on?",
      a="Take the lot's dimensions, subtract the front, rear and side setbacks your zoning requires, and what is left is the buildable envelope. Height limits, lot coverage and parking rules can shrink it further.",
      steps=[("Measure the lot", "Width along the street and depth back from it, in feet."),
             ("Find the setbacks", "Your zoning code lists the front, rear and side setbacks for the district. Corner lots often have two fronts."),
             ("Subtract them", "Width minus both side setbacks; depth minus front and rear."),
             ("Check the other limits", "Maximum lot coverage, floor area ratio, height and parking can each cap what you build."),
             ("Sketch the building in the envelope", "Footprint, stories and parking, before anyone draws it for real.")],
      example=(f"A {ss_w} × {ss_d} ft lot, with a {ss_front} ft front setback, a {ss_rear} ft rear setback and {ss_side} ft on each side.",
               [f"Buildable width: {ss_w} − {ss_side} − {ss_side} = {ss_bw} ft. Buildable depth: {ss_d} − {ss_front} − {ss_rear} = {ss_bd} ft.",
                f"Buildable footprint: {ss_bw} × {ss_bd} = {ss_foot:,} square feet, out of a {ss_w * ss_d:,} square-foot lot.",
                f"Two stories on that footprint is up to {2 * ss_foot:,} square feet, if lot coverage, floor area and parking rules allow it."]),
      ready=["The lot's width and depth", "The district's setbacks from your zoning code", "What you want to build: homes, a row of units, or a building with a unit mix", "Stories and parking"],
      tool_line="SiteShaper draws the site plan with your setbacks, generates floor plates for the program you give it, and lays out the numbers table, ready to show an architect or a planner.",
      more="SiteShaper is a schematic, not a survey or a zoning determination. Confirm setbacks and limits with your local planning office."),
 dict(slug="housing-project-brief", tool="BuildBrief", url="https://buildbrief.nesohq.com/",
      title="How to explain a housing project to an architect, a contractor or a lender",
      desc="What to put on one page before your first meeting about a housing project, so the people you hire start in the right place.",
      q="What should I bring to a first meeting with an architect or lender about a housing project?",
      a="One page that says what the site is, who the homes are for, how many and what kind, what matters most, the budget range, and what you will not do. With that, a professional can tell you in one meeting whether the idea works and what it takes.",
      steps=[("Describe the site", "Address, lot size and zoning if you know it."),
             ("Say who it is for", "Workforce, seniors, families, students, or the market."),
             ("Give the unit mix", "How many studios, one-, two- and three-bedroom units, and how many stories and parking spaces."),
             ("Rank what matters", "Cost, speed, quality, energy use, design character."),
             ("Set the edges", "A budget range, must-haves and deal-breakers, and the goal in your own words.")],
      example=("A 12-unit workforce-housing building on a half-acre corner lot.",
               ["Who it is for: teachers, nurses and service workers in the town.",
                "Mix: four one-bedroom, six two-bedroom and two three-bedroom units, on three stories, with one parking space per unit.",
                "What matters most: cost and energy use. Deal-breaker: no units without a window in every bedroom.",
                "On one page, an architect can see in minutes whether the lot fits the program and what to study first."]),
      ready=["Site and lot size", "Stage (an idea, a site under contract, or land you own)", "Who the homes are for", "Unit mix, stories and parking", "Budget range, must-haves and deal-breakers"],
      tool_line="BuildBrief turns your answers into a one-page Development Intent Brief: the quick numbers, a massing snapshot, your priorities, and wording a professional reads in two minutes.",
      more="A brief is a starting point for professionals, not a design or a cost estimate."),
 dict(slug="size-the-market-new-location", tool="MarketFit", url="https://marketfit.nesohq.com/",
      title="How to size the market for a new location",
      desc="A bottom-up way to tell whether a town can support your business, with a worked example: households, how often they buy, what they spend, and your fair share.",
      q="How do I know if there is room in a market for a new location?",
      a="Build the market from the bottom up: the households (or businesses) in your trade area, times how often they buy, times what they spend. Divide by the number of competitors plus you for a fair share, and compare it with the revenue the location needs.",
      steps=[("Draw the trade area", "Where your customers will really come from: a 10-minute drive, a neighborhood, a county."),
             ("Count the buyers", "Households, or businesses if you sell to them, from the Census or a county source."),
             ("Estimate how often and how much", "Visits or purchases a year, and the spend each time."),
             ("Divide by the field", "The number of competitors, plus you, gives a fair share before any edge you bring."),
             ("Compare with what you need", "The revenue the location needs to cover its costs. If your fair share falls short, you need a real edge or a different spot.")],
      example=(f"A café looking at a trade area of {mf_hh:,} households, each buying about {mf_freq} times a year at {money(mf_spend)}, with {mf_rivals} cafés already there and {money(mf_need)} a year needed to cover costs.",
               [f"The market: {mf_hh:,} × {mf_freq} × {money(mf_spend)} = {money(mf_pie)} a year.",
                f"A fair share with {mf_rivals} competitors plus you: {money(mf_pie)} ÷ {mf_rivals + 1} = {money(mf_share)}.",
                f"That is {money(mf_need - mf_share)} short of the {money(mf_need)} needed, so the move works only with a clear edge (location, hours, a product no one else has) or lower costs."]),
      ready=["What you sell and who buys it", "The trade area", "A rough count of competitors", "The revenue the move needs"],
      tool_line="MarketFit sizes the market for a first location, a new location, or a new line of business, and gives an honest read: how big the pie is, how crowded it is, and whether your slice works.",
      more="A market size is an estimate for a decision, not a forecast of sales."),
 dict(slug="break-even-and-runway", tool="PlanForge", url="https://planforge.nesohq.com/",
      title="How to find your break-even point and your runway",
      desc="How many sales cover your monthly costs, and how long your cash lasts until then, with a worked example.",
      q="How do I work out my break-even point?",
      a="Divide your monthly fixed costs by what each sale leaves after its direct costs (the contribution margin). The answer is how many sales a month cover the fixed base. Your runway is how many months your cash lasts while you get there.",
      steps=[("Set the average sale", "What a typical sale brings in. For a subscription, the monthly price; for hourly work, the rate times the usual hours."),
             ("Take off the direct cost", "What each sale costs to deliver: materials, ingredients, payment fees. Service businesses often run 5% to 15%; retail and food 25% to 40%."),
             ("Add up fixed costs", "Rent, payroll, insurance, software, loan payments and the owner's pay: what you spend whether you sell or not."),
             ("Divide", "Fixed costs ÷ contribution per sale = sales a month to break even."),
             ("Check the runway", "Starting cash ÷ the monthly shortfall while sales grow = months before the cash runs out.")],
      example=(f"An average sale of {money(pl_sale)}, a direct cost of {pl_cost:.0%}, and fixed costs of {money(pl_fixed)} a month.",
               [f"Each sale leaves {money(pl_sale)} × (1 − {pl_cost:.2f}) = {money(pl_contrib)}.",
                f"Break-even: {money(pl_fixed)} ÷ {money(pl_contrib)} ≈ {pl_be:.0f} sales a month (rounded up to {int(-(-pl_fixed // pl_contrib))}).",
                "A common mistake is counting the owner's pay or a loan payment as a cost of each sale. Both are fixed, and leaving them out makes break-even look closer than it is."]),
      ready=["Your average sale", "Direct cost as a share of each sale", "Monthly fixed costs, including your own pay", "Starting cash", "Expected monthly growth"],
      tool_line="PlanForge turns your pricing, costs and growth into a 12- to 36-month model: revenue, break-even, runway, and the skeleton of the financial section of a business plan.",
      more="A model is a plan to test, not a forecast. Change one input at a time to see what moves the answer."),
]

CSS = """:root{--ink:#16141A;--body:#4C4753;--soft:#6E6878;--plum:#5B2A86;--plum-d:#421D64;--plum-w:#F6F2FA;--gold:#E7B84B;--line:#E9E6EC;--bg:#FFFFFF;--bg-2:#FAF9FB;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:var(--sans);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}
.top{background:var(--plum-d);color:#fff;font-size:14px;padding:10px 0}
.top .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.top a{color:#fff;text-decoration:none;font-weight:600}
header.hero{padding:40px 0 20px}
.kicker{display:inline-block;background:var(--plum-w);color:var(--plum);font-size:13.5px;font-weight:600;padding:6px 13px;border-radius:999px;margin-bottom:16px;text-decoration:none}
h1{font-size:clamp(28px,4.6vw,40px);line-height:1.14;letter-spacing:-.02em}
.lead{font-size:19px;color:var(--body);margin-top:14px}
h2{font-size:22px;letter-spacing:-.01em;margin:34px 0 10px}
p{color:var(--body);margin:0 0 12px}
ol.steps{margin:6px 0 0 0;padding-left:22px;color:var(--body)}
ol.steps li{margin:0 0 10px}
ol.steps b{color:var(--ink)}
.ex{background:var(--bg-2);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:12px;padding:18px 20px;margin-top:8px}
.ex p:first-child{color:var(--ink);font-weight:600}
.ex ul{padding-left:20px;color:var(--body)}
.ex li{margin:6px 0}
ul.ready{padding-left:20px;color:var(--body)}
.cta{background:var(--plum-w);border-radius:14px;padding:22px;margin:34px 0 10px}
.cta p{color:var(--ink)}
.btn{display:inline-block;background:var(--plum);color:#fff;border-radius:10px;padding:12px 20px;font-weight:700;text-decoration:none;margin-top:6px}
.small{font-size:14px;color:var(--soft)}
.more{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-top:8px}
.more a{display:block;border:1px solid var(--line);border-radius:10px;padding:12px 14px;color:var(--ink);text-decoration:none;font-size:15px;line-height:1.35}
.more a:hover,.btn:hover{filter:brightness(.95)}
.cards a b{display:block;font-size:17px;margin-bottom:4px}
footer{border-top:1px solid var(--line);margin-top:40px;padding:22px 0 40px;font-size:14px;color:var(--soft)}
footer a{color:var(--soft)}"""
GTAG = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-8F80E2D56H"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());
if(location.hostname==='nesohq.com'||location.hostname.endsWith('.nesohq.com')){gtag('config','G-8F80E2D56H');}</script>"""
ICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%235B2A86'/%3E%3C/svg%3E"
E = html.escape


def head(title, desc, url, ld):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
{GTAG}
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} · NESO</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="https://nesohq.com/og-hello.png">
<link rel="icon" href="{ICON}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>
<div class="top"><div class="wrap"><a href="https://nesohq.com/?source=guide">NESO HQ LLC</a><span><a href="/guides/">Free guides</a></span></div></div>
<main class="wrap">"""


FOOT = """</main>
<footer><div class="wrap">NESO HQ LLC · <a href="https://nesohq.com/?source=guide">nesohq.com</a> · <a href="https://brief.nesohq.com/?source=guide">The NESO Brief</a> · <a href="/legal/privacy.html">Privacy</a><br>
Educational guidance. Nothing here is legal, tax, engineering or investment advice.</div></footer>
</body></html>
"""


def page(g):
    url = f"https://nesohq.com/guides/{g['slug']}.html"
    go = g["url"] + "?source=guide"
    ld = [{"@context": "https://schema.org", "@type": "HowTo", "name": g["title"], "description": g["desc"],
           "step": [{"@type": "HowToStep", "position": i + 1, "name": n, "text": t} for i, (n, t) in enumerate(g["steps"])],
           "tool": [{"@type": "HowToTool", "name": g["tool"]}]},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": g["q"], "acceptedAnswer": {"@type": "Answer", "text": g["a"]}}]}]
    others = "".join(f'<a href="/guides/{o["slug"]}.html">{E(o["title"])}</a>' for o in G if o is not g)
    steps = "".join(f"<li><b>{E(n)}.</b> {E(t)}</li>" for n, t in g["steps"])
    ex = "".join(f"<li>{E(x)}</li>" for x in g["example"][1])
    ready = "".join(f"<li>{E(x)}</li>" for x in g["ready"])
    return (head(g["title"], g["desc"], url, ld) + f"""
<header class="hero">
  <a class="kicker" href="/guides/">Free guide · {E(g['tool'])}</a>
  <h1>{E(g['title'])}</h1>
  <p class="lead">{E(g['a'])}</p>
</header>
<h2>How to work it out</h2>
<ol class="steps">{steps}</ol>
<h2>A worked example</h2>
<div class="ex"><p>{E(g['example'][0])}</p><ul>{ex}</ul></div>
<h2>What to have ready</h2>
<ul class="ready">{ready}</ul>
<div class="cta"><p><b>Do it in {E(g['tool'])}, free, in your browser.</b> {E(g['tool_line'])}</p>
<a class="btn" href="{go}">Open {E(g['tool'])}</a></div>
<p class="small">{E(g['more'])}</p>
<h2>More free guides</h2>
<div class="more">{others}</div>
""" + FOOT)


def index():
    url = "https://nesohq.com/guides/"
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Free guides from NESO", "url": url,
          "hasPart": [{"@type": "HowTo", "name": g["title"], "url": f"https://nesohq.com/guides/{g['slug']}.html"} for g in G]}
    cards = "".join(f'<a href="/guides/{g["slug"]}.html"><b>{E(g["q"])}</b>{E(g["desc"])}</a>' for g in G)
    return (head("Free guides: grants, capital stacks, pro formas, market size and more",
                 "Plain-language guides to the questions owners, builders and towns ask, each with a worked example and a free tool to do it.",
                 url, ld) + f"""
<header class="hero">
  <span class="kicker">Free guides</span>
  <h1>The questions owners, builders and towns ask</h1>
  <p class="lead">Each guide answers one question in plain words, works one example with real numbers, and hands you a free tool that does it in your browser. No account.</p>
</header>
<div class="more cards">{cards}</div>
""" + FOOT)


OUT.mkdir(parents=True, exist_ok=True)
for g in G:
    (OUT / f"{g['slug']}.html").write_text(page(g))
(OUT / "index.html").write_text(index())
print("\n".join(sorted(p.name for p in OUT.iterdir())))
