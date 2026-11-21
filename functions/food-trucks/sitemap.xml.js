// nesohq.com/food-trucks/sitemap.xml: every approved truck's page, for search engines.
export async function onRequestGet() {
  let trucks = [];
  try { const r = await fetch("https://hq.nesohq.com/pub/trucks", { cf: { cacheTtl: 300 } }); if (r.ok) trucks = (await r.json()).trucks || []; } catch (e) {}
  const urls = [["https://nesohq.com/food-trucks.html", new Date().toISOString().slice(0, 10)], ["https://nesohq.com/food-trucks/join.html", "2026-11-21"], ["https://nesohq.com/food-trucks/example.html", "2026-11-21"]]
    .concat(trucks.map(t => ["https://nesohq.com/food-trucks/t/" + t.slug, String(t.updated || "").slice(0, 10)]));
  const xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls.map(([u, d]) => `  <url><loc>${u}</loc>${d ? `<lastmod>${d}</lastmod>` : ""}</url>`).join("\n") + "\n</urlset>\n";
  return new Response(xml, { headers: { "content-type": "application/xml; charset=utf-8", "cache-control": "public, max-age=300" } });
}
