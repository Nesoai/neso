/* NESO food truck directory: shared helpers for the directory, a truck's page and the listing form.
   Listings come from NESO HQ's public API. Open now and open today use the visitor's own clock. */
window.FT = (function () {
  var API = "https://hq.nesohq.com/pub/trucks";
  var DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  function hm(t) { var p = String(t || "").split(":"); return (+p[0] || 0) + (+p[1] || 0) / 60; }
  function nice(t) { var p = String(t || "").split(":"), h = +p[0] || 0, m = +p[1] || 0, ap = h >= 12 ? "pm" : "am", x = h % 12 || 12; return x + (m ? ":" + String(m).padStart(2, "0") : "") + ap; }
  function status(t, now) {
    now = now || new Date(); var d = now.getDay(), x = now.getHours() + now.getMinutes() / 60, s = (t.schedule || [])[d];
    if (s && !s.off && x >= hm(s.open) && x < hm(s.close)) return { open: true, today: true, stop: s, text: "Open now until " + nice(s.close) + " at " + s.place };
    if (s && !s.off && x < hm(s.open)) return { open: false, today: true, stop: s, text: "Today " + nice(s.open) + " to " + nice(s.close) + " at " + s.place };
    for (var j = 1; j <= 7; j++) { var n = (t.schedule || [])[(d + j) % 7]; if (n && !n.off) return { open: false, today: false, stop: n, text: "Next: " + (j === 1 ? "tomorrow" : DAYS[n.day]) + " " + nice(n.open) + " at " + n.place }; }
    return { open: false, today: false, stop: null, text: "No stops listed this week" };
  }
  function miles(a, b) {
    var R = 3958.8, r = Math.PI / 180, dLat = (b.lat - a.lat) * r, dLng = (b.lng - a.lng) * r;
    var q = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(a.lat * r) * Math.cos(b.lat * r) * Math.sin(dLng / 2) * Math.sin(dLng / 2);
    return 2 * R * Math.asin(Math.sqrt(q));
  }
  function img(t, i) { return API + "/img/" + t.id + "/" + i; }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function tel(p) { return "tel:" + String(p || "").replace(/[^\d+]/g, ""); }
  return { API: API, DAYS: DAYS, nice: nice, status: status, miles: miles, img: img, esc: esc, tel: tel };
})();
