// Client-side search over every digest. The index is fetched the first time
// someone types, so the archive page stays light.
(function () {
  var input = document.getElementById("search");
  var results = document.getElementById("results");
  var status = document.getElementById("search-status");
  var archive = document.getElementById("archive");
  var index = null;
  var loading = null;

  function load() {
    if (!loading) {
      loading = fetch(window.SEARCH_INDEX)
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var txt = document.createElement("textarea");
          index = data.map(function (d) {
            txt.innerHTML = d.text; // strip_html leaves entities such as &amp;
            d.text = txt.value;
            d.hay = (d.title + " " + d.text).toLowerCase();
            return d;
          });
        });
    }
    return loading;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function snippet(text, term) {
    var i = text.toLowerCase().indexOf(term);
    var start = Math.max(0, i - 70);
    var s = (start > 0 ? "…" : "") + text.slice(start, i + term.length + 110) + "…";
    var safe = escapeHtml(s);
    var re = new RegExp("(" + term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig");
    return safe.replace(re, "<mark>$1</mark>");
  }

  function run() {
    var q = input.value.trim().toLowerCase();
    if (!q) {
      results.hidden = true;
      status.hidden = true;
      archive.hidden = false;
      return;
    }
    var terms = q.split(/\s+/);
    var hits = index.filter(function (d) {
      return terms.every(function (t) { return d.hay.indexOf(t) !== -1; });
    });
    archive.hidden = true;
    status.hidden = false;
    status.textContent = hits.length + (hits.length === 1 ? " digest" : " digests") + " mention " + q;
    results.innerHTML = hits.map(function (d) {
      return '<li><a href="' + d.url + '"><time>' + escapeHtml(d.date) +
        '</time><span class="excerpt">' + snippet(d.text, terms[0]) + "</span></a></li>";
    }).join("");
    results.hidden = hits.length === 0;
  }

  var timer;
  input.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { load().then(run); }, 150);
  });
})();
