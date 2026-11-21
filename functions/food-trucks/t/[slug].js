// A truck's own page in NESO's food truck directory: nesohq.com/food-trucks/t/<slug>.
// Rendered here from NESO HQ's public listing so search engines see the whole page, with
// schema.org FoodEstablishment data. Open now is worked out in the visitor's browser.
const API = "https://hq.nesohq.com/pub/trucks";
const DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const nice = t => { const [h, m] = String(t || "0:0").split(":").map(Number); return ((h % 12) || 12) + (m ? ":" + String(m).padStart(2, "0") : "") + (h >= 12 ? "pm" : "am"); };
const telOf = p => "tel:" + String(p || "").replace(/[^\d+]/g, "");

export async function onRequestGet({ params }) {
  const slug = String(params.slug || "").toLowerCase();
  if (!/^[a-z0-9-]{1,80}$/.test(slug)) return notFound();
  let t;
  try { const r = await fetch(API + "/" + slug, { cf: { cacheTtl: 60 } }); if (!r.ok) return notFound(); t = (await r.json()).truck; } catch (e) { return notFound(); }
  if (!t) return notFound();
  const url = "https://nesohq.com/food-trucks/t/" + t.slug;
  const img = i => API + "/img/" + t.id + "/" + i;
  const ld = { "@context": "https://schema.org", "@type": "FoodEstablishment", name: t.name, url, servesCuisine: t.cuisines,
    address: { "@type": "PostalAddress", addressLocality: t.city, addressRegion: t.state, postalCode: t.zip || undefined, addressCountry: "US" },
    telephone: t.phone || undefined, image: t.photos ? Array.from({ length: t.photos }, (_, i) => img(i)) : undefined, description: t.blurb || undefined,
    sameAs: [t.instagram, t.facebook, t.website].filter(Boolean),
    openingHoursSpecification: t.schedule.filter(s => !s.off).map(s => ({ "@type": "OpeningHoursSpecification", dayOfWeek: DAYS[s.day], opens: s.open, closes: s.close })),
    hasMenu: t.menu.length ? { "@type": "Menu", hasMenuSection: { "@type": "MenuSection", name: "Menu", hasMenuItem: t.menu.map(m => ({ "@type": "MenuItem", name: m.name, description: m.desc || undefined })) } } : undefined };
  const week = t.schedule.map(s => `<div class="day${s.off ? " off" : ""}" data-day="${s.day}"><div class="d">${DAYS[s.day]}</div>${s.off ? "<div class='w'>Not out</div>" :
    `<div class="w">${esc(s.place)}</div><div class="h">${nice(s.open)} to ${nice(s.close)}</div>${s.lat != null ? `<a class="dir" href="https://www.google.com/maps/dir/?api=1&destination=${s.lat},${s.lng}" rel="noopener">Directions</a>` : s.address ? `<div class="h">${esc(s.address)}</div>` : ""}`}</div>`).join("");
  const menu = t.menu.map(m => `<div class="item"><div class="row"><b>${esc(m.name)}</b>${m.price ? `<span class="price">${esc(m.price)}</span>` : ""}</div>${m.desc ? `<p>${esc(m.desc)}</p>` : ""}</div>`).join("");
  const photos = t.photos ? `<div class="photos">${Array.from({ length: t.photos }, (_, i) => `<img src="${img(i)}" alt="${esc(t.name)}, photo ${i + 1}" loading="${i ? "lazy" : "eager"}">`).join("")}</div>` : "";
  const links = [[t.instagram, "Instagram"], [t.facebook, "Facebook"], [t.website, "Website"], [t.order, "Order online"]].filter(x => x[0]).map(([u, n]) => `<a href="${esc(u)}" rel="noopener nofollow">${n}</a>`).join(" · ");
  const desc = `${t.name}: ${t.cuisines.join(", ")} food truck in ${t.city}, ${t.state}. Where it is each day, hours, menu and photos.`;
  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(t.name)}: ${esc(t.cuisines[0] || "food")} truck in ${esc(t.city)}, ${esc(t.state)} | NESO Food Trucks</title>
<meta name="description" content="${esc(desc)}"><link rel="canonical" href="${url}">
<meta property="og:title" content="${esc(t.name)} | NESO Food Trucks"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${url}">${t.photos ? `<meta property="og:image" content="${img(0)}">` : ""}
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<script type="application/ld+json">${JSON.stringify(ld).replace(/</g, "\\u003c")}</script>
<style>
:root{--char:#1c1613;--ember:#e2552b;--ember2:#f08a3a;--cream:#fbf3e6;--paper:#fffaf2;--ink:#221a15;--muted:#6f6259;--line:#eadfce;--neso:#5b2a86}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 Inter,Arial,sans-serif}a{color:inherit}img{max-width:100%;display:block}
.wrap{max-width:960px;margin:0 auto;padding:0 16px}.disp{font-family:"Bebas Neue",Impact,sans-serif;font-weight:400;letter-spacing:.02em}
header.top{background:var(--char);color:var(--cream)}header.top .wrap{display:flex;align-items:center;justify-content:space-between;height:58px;gap:10px}
.brand{text-decoration:none;color:var(--cream);font-size:26px}.brand span{color:var(--ember2)}header.top a.b{color:var(--cream);font-size:14px}
h1{font-size:clamp(48px,9vw,84px);line-height:.92;margin:26px 0 6px}.cu{color:var(--muted);margin:0 0 12px;font-weight:600}
.status{display:inline-flex;gap:9px;align-items:center;background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-weight:600}
.dot{width:10px;height:10px;border-radius:50%;background:#c9813a}.dot.on{background:#2fb35a;box-shadow:0 0 0 4px rgba(47,179,90,.25)}
.btns{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}.btn{display:inline-block;text-decoration:none;font-weight:800;padding:12px 18px;border-radius:10px}.btn.fire{background:var(--ember);color:#fff}.btn.ghost{background:var(--cream)}
.photos{display:grid;grid-template-columns:2fr 1fr 1fr;gap:8px;margin:16px 0}.photos img{width:100%;height:260px;object-fit:cover;border-radius:14px}.photos img:first-child{grid-row:span 2;height:528px}
section{padding:22px 0}h2{font-size:40px;line-height:1;margin:0 0 12px}
.week{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}.day{background:#fff;border:1px solid var(--line);border-radius:14px;padding:12px}.day.today{background:var(--char);color:var(--cream)}.day.off{opacity:.55}
.day .d{font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}.day.today .d{color:var(--ember2)}.day .w{font-weight:800;margin:3px 0}.day .h{font-size:14px;color:var(--muted)}.day.today .h{color:#d9cbbb}.dir{font-size:13px;font-weight:700}
.menu{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px}.item{background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 14px}.item .row{display:flex;justify-content:space-between;gap:10px}.item p{margin:4px 0 0;color:var(--muted);font-size:14px}.price{color:var(--ember);font-weight:800}
.special{background:var(--char);color:var(--cream);border-radius:14px;padding:14px 16px;margin-bottom:12px}.special b{color:var(--ember2)}
.own{background:#f3ecf9;border-radius:14px;padding:16px;margin:10px 0 30px}.own a{color:var(--neso);font-weight:800}
footer{padding:22px 0;color:#6e6878;font-size:13.5px}footer a{color:var(--neso)}
@media(max-width:700px){.photos{grid-template-columns:1fr 1fr}.photos img,.photos img:first-child{height:180px;grid-row:auto}.photos img:first-child{grid-column:span 2;height:260px}}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand disp" href="https://nesohq.com/food-trucks.html">Food <span>Trucks</span></a><a class="b" href="https://nesohq.com/food-trucks.html">All trucks</a></div></header>
<main class="wrap">
<h1 class="disp">${esc(t.name)}</h1><p class="cu">${esc(t.cuisines.join(" · "))} · ${esc(t.city)}, ${esc(t.state)}${t.catering ? " · catering and events" : ""}</p>
<span class="status"><i class="dot" id="dot"></i><span id="st">See this week's stops below</span></span>
${t.blurb ? `<p style="font-size:18px;max-width:680px">${esc(t.blurb)}</p>` : ""}
<div class="btns">${t.phone ? `<a class="btn fire" href="${telOf(t.phone)}">Call ${esc(t.phone)}</a>` : ""}${t.order ? `<a class="btn ghost" href="${esc(t.order)}" rel="noopener nofollow">Order online</a>` : ""}${t.email ? `<a class="btn ghost" href="mailto:${esc(t.email)}">Email${t.catering ? " about catering" : ""}</a>` : ""}</div>
${photos}
<section><h2 class="disp">Where we'll be</h2><div class="week">${week}</div></section>
${menu || t.special ? `<section><h2 class="disp">Menu</h2>${t.special ? `<div class="special"><b>This week's special:</b> ${esc(t.special)}</div>` : ""}<div class="menu">${menu}</div></section>` : ""}
${links ? `<p>${links}</p>` : ""}
<div class="own">Own this truck? Change your stops, hours and menu with the private link you saved when you listed it. Lost it? Write to <a href="mailto:hello@nesohq.com">hello@nesohq.com</a>. Want your own website too? <a href="https://nesohq.com/food-trucks/example.html">See the example truck site</a>.</div>
</main>
<footer><div class="wrap">Listed by the truck's owner in <a href="https://nesohq.com/food-trucks.html">NESO's free food truck directory</a>. Stops and hours are as the owner last set them; open now uses your device's clock. Something wrong here? <a href="mailto:hello@nesohq.com?subject=${encodeURIComponent("Food truck listing: " + t.name)}">Tell NESO</a>. · <a href="https://nesohq.com/legal/privacy.html">Privacy</a></div></footer>
<script>(function(){var S=${JSON.stringify(t.schedule.map(s => ({ day: s.day, off: s.off, place: s.place, open: s.open, close: s.close }))).replace(/</g, "\\u003c")};
function hm(x){var p=String(x||"0:0").split(":");return(+p[0]||0)+(+p[1]||0)/60}function nice(x){var p=String(x||"0:0").split(":"),h=+p[0]||0,m=+p[1]||0;return((h%12)||12)+(m?":"+String(m).padStart(2,"0"):"")+(h>=12?"pm":"am")}
var D=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],n=new Date(),d=n.getDay(),x=n.getHours()+n.getMinutes()/60,s=S[d],el=document.getElementById("st");
var c=document.querySelector('.day[data-day="'+d+'"]');if(c)c.classList.add("today");
if(s&&!s.off&&x>=hm(s.open)&&x<hm(s.close)){el.textContent="Open now until "+nice(s.close)+" at "+s.place;document.getElementById("dot").className="dot on"}
else if(s&&!s.off&&x<hm(s.open)){el.textContent="Today "+nice(s.open)+" to "+nice(s.close)+" at "+s.place}
else{for(var j=1;j<=7;j++){var q=S[(d+j)%7];if(q&&!q.off){el.textContent="Next: "+(j===1?"tomorrow":D[q.day])+" "+nice(q.open)+" at "+q.place;break}}}})();</script>
</body></html>`;
  return new Response(html, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "public, max-age=60" } });
}
function notFound() {
  return new Response(`<!DOCTYPE html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Truck not found | NESO</title><body style="font:16px/1.6 Arial,sans-serif;max-width:640px;margin:40px auto;padding:0 16px"><h1>That truck isn't listed.</h1><p>It may have moved or not been approved yet. <a href="https://nesohq.com/food-trucks.html">See every truck in the directory</a>.</p></body>`, { status: 404, headers: { "content-type": "text/html; charset=utf-8" } });
}
