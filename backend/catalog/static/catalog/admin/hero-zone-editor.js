(function () {
  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  function num(value, fallback) {
    var n = parseFloat(value);
    return Number.isFinite(n) ? n : fallback;
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function round(value) {
    return Math.round(value * 100) / 100;
  }

  ready(function () {
    var host = document.getElementById("hero-zone-editor");
    if (!host) return;

    var group = document.getElementById("zones-group");
    if (!group) return;

    var imageUrl = host.getAttribute("data-image") || "";
    var urlInput = document.getElementById("id_image_url");
    if (!imageUrl && urlInput) imageUrl = urlInput.value;

    host.className = "hero-zone-editor";
    host.innerHTML =
      "<h2>Малювання зон на фото</h2>" +
      "<p>Перетягніть рамку, щоб пересунути зону. Тягніть кут, щоб змінити розмір. " +
      "Клік і протягнення по порожньому місцю створює нову зону. " +
      "Спочатку збережіть сцену з фото, якщо редактор порожній.</p>";

    var stage = document.createElement("div");
    stage.className = "hero-zone-stage";
    var img = document.createElement("img");
    img.alt = "Фото сцени";
    if (imageUrl) img.src = imageUrl;
    var layer = document.createElement("div");
    layer.className = "hero-zone-layer";
    stage.appendChild(img);
    stage.appendChild(layer);
    host.appendChild(stage);

    function rows() {
      return Array.prototype.slice.call(
        group.querySelectorAll("tr.form-row:not(.empty-form)")
      );
    }

    function field(row, name) {
      return row.querySelector('[name$="-' + name + '"]');
    }

    function isEmpty(row) {
      var name = field(row, "name");
      var del = row.querySelector('[name$="-DELETE"]');
      return !name || !name.value.trim() || (del && del.checked);
    }

    function readBox(row) {
      return {
        x: clamp(num(field(row, "x") && field(row, "x").value, 10), 0, 99),
        y: clamp(num(field(row, "y") && field(row, "y").value, 10), 0, 99),
        w: clamp(num(field(row, "width") && field(row, "width").value, 20), 1, 100),
        h: clamp(num(field(row, "height") && field(row, "height").value, 15), 1, 100),
        name: (field(row, "name") && field(row, "name").value) || "Нова зона",
      };
    }

    function writeBox(row, box) {
      var x = field(row, "x");
      var y = field(row, "y");
      var w = field(row, "width");
      var h = field(row, "height");
      if (x) x.value = round(box.x);
      if (y) y.value = round(box.y);
      if (w) w.value = round(box.w);
      if (h) h.value = round(box.h);
    }

    function imageRect() {
      var sr = stage.getBoundingClientRect();
      var ir = img.getBoundingClientRect();
      return {
        left: ir.left - sr.left,
        top: ir.top - sr.top,
        width: ir.width,
        height: ir.height,
      };
    }

    function render() {
      layer.innerHTML = "";
      var rect = imageRect();
      layer.style.left = rect.left + "px";
      layer.style.top = rect.top + "px";
      layer.style.width = rect.width + "px";
      layer.style.height = rect.height + "px";

      rows().forEach(function (row, index) {
        if (isEmpty(row) && !field(row, "x").value) return;
        if (isEmpty(row) && !field(row, "name").value) return;
        var del = row.querySelector('[name$="-DELETE"]');
        if (del && del.checked) return;
        if (!field(row, "name") || !field(row, "name").value.trim()) return;

        var box = readBox(row);
        var el = document.createElement("div");
        el.className = "hero-zone-box";
        el.textContent = box.name;
        el.style.left = box.x + "%";
        el.style.top = box.y + "%";
        el.style.width = box.w + "%";
        el.style.height = box.h + "%";
        var handle = document.createElement("span");
        handle.className = "handle";
        el.appendChild(handle);
        layer.appendChild(el);

        el.addEventListener("mousedown", function (event) {
          if (event.target === handle) return;
          event.preventDefault();
          event.stopPropagation();
          startDrag(row, el, event, "move");
        });
        handle.addEventListener("mousedown", function (event) {
          event.preventDefault();
          event.stopPropagation();
          startDrag(row, el, event, "resize");
        });
        el.addEventListener("click", function () {
          var name = field(row, "name");
          if (name) name.focus();
        });
        el.dataset.index = String(index);
      });
    }

    function startDrag(row, el, event, mode) {
      var start = imageRect();
      var box = readBox(row);
      var sx = event.clientX;
      var sy = event.clientY;

      function move(e) {
        var dx = ((e.clientX - sx) / start.width) * 100;
        var dy = ((e.clientY - sy) / start.height) * 100;
        var next = { x: box.x, y: box.y, w: box.w, h: box.h };
        if (mode === "move") {
          next.x = clamp(box.x + dx, 0, 100 - box.w);
          next.y = clamp(box.y + dy, 0, 100 - box.h);
        } else {
          next.w = clamp(box.w + dx, 3, 100 - box.x);
          next.h = clamp(box.h + dy, 3, 100 - box.y);
        }
        writeBox(row, next);
        el.style.left = next.x + "%";
        el.style.top = next.y + "%";
        el.style.width = next.w + "%";
        el.style.height = next.h + "%";
      }

      function up() {
        document.removeEventListener("mousemove", move);
        document.removeEventListener("mouseup", up);
        render();
      }

      document.addEventListener("mousemove", move);
      document.addEventListener("mouseup", up);
    }

    function addRow() {
      var add = group.querySelector(".add-row a");
      if (add) add.click();
    }

    function emptyRow() {
      var found = rows().find(function (row) {
        return !field(row, "name") || !field(row, "name").value.trim();
      });
      if (found) return found;
      addRow();
      return rows().find(function (row) {
        return !field(row, "name") || !field(row, "name").value.trim();
      });
    }

    stage.addEventListener("mousedown", function (event) {
      if (event.target !== stage && event.target !== img && event.target !== layer) {
        return;
      }
      var rect = imageRect();
      if (!rect.width) return;
      var x = ((event.clientX - stage.getBoundingClientRect().left - rect.left) / rect.width) * 100;
      var y = ((event.clientY - stage.getBoundingClientRect().top - rect.top) / rect.height) * 100;
      if (x < 0 || y < 0 || x > 100 || y > 100) return;

      var row = emptyRow();
      if (!row) return;
      var start = { x: clamp(x, 0, 97), y: clamp(y, 0, 97), w: 3, h: 3 };
      writeBox(row, start);
      var name = field(row, "name");
      if (name && !name.value) name.value = "Нова зона";
      var order = field(row, "order");
      if (order && !order.value) order.value = String(rows().length);

      function move(e) {
        var nx = ((e.clientX - stage.getBoundingClientRect().left - rect.left) / rect.width) * 100;
        var ny = ((e.clientY - stage.getBoundingClientRect().top - rect.top) / rect.height) * 100;
        writeBox(row, {
          x: clamp(Math.min(start.x, nx), 0, 97),
          y: clamp(Math.min(start.y, ny), 0, 97),
          w: clamp(Math.abs(nx - start.x), 3, 100),
          h: clamp(Math.abs(ny - start.y), 3, 100),
        });
        render();
      }

      function up() {
        document.removeEventListener("mousemove", move);
        document.removeEventListener("mouseup", up);
        render();
      }

      document.addEventListener("mousemove", move);
      document.addEventListener("mouseup", up);
    });

    group.addEventListener("input", render);
    group.addEventListener("change", render);
    img.addEventListener("load", render);
    window.addEventListener("resize", render);
    if (urlInput) {
      urlInput.addEventListener("change", function () {
        if (urlInput.value) img.src = urlInput.value;
      });
    }

    setTimeout(render, 200);
  });
})();
