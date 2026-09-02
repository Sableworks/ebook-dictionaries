(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  var year = document.getElementById("year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  document.querySelectorAll("[data-gallery]").forEach(initGallery);
  bindLatestRelease();

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      var id = link.getAttribute("href");
      if (!id || id === "#") return;
      var target = document.querySelector(id);
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({
        behavior: prefersReducedMotion() ? "auto" : "smooth",
        block: "start",
      });
    });
  });

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function bindLatestRelease() {
    document.querySelectorAll("[data-latest-release]").forEach(function (link) {
      var repo = link.getAttribute("data-latest-release");
      if (!repo) return;
      fetch("https://api.github.com/repos/" + repo + "/releases/latest")
        .then(function (res) {
          return res.ok ? res.json() : null;
        })
        .then(function (rel) {
          if (!rel || !rel.assets) return;
          var zip = rel.assets.find(function (asset) {
            return /\.zip$/i.test(asset.name);
          });
          if (zip && zip.browser_download_url) {
            link.href = zip.browser_download_url;
          }
          var tag = document.querySelector("[data-latest-tag]");
          if (tag && rel.tag_name) {
            tag.textContent = rel.tag_name;
          }
        })
        .catch(function () {});
    });
  }

  function initGallery(root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll(".gallery-slide"));
    if (slides.length < 2) return;

    var index = 0;
    var status = root.querySelector("[data-gallery-status]");
    var prev = root.querySelector("[data-gallery-prev]");
    var next = root.querySelector("[data-gallery-next]");
    var touchX = null;

    function show(nextIndex) {
      index = (nextIndex + slides.length) % slides.length;
      slides.forEach(function (slide, i) {
        slide.classList.toggle("is-active", i === index);
      });
      if (status) {
        status.textContent = index + 1 + " / " + slides.length;
      }
    }

    if (prev) {
      prev.addEventListener("click", function (event) {
        event.stopPropagation();
        show(index - 1);
      });
    }
    if (next) {
      next.addEventListener("click", function (event) {
        event.stopPropagation();
        show(index + 1);
      });
    }

    root.addEventListener("keydown", function (event) {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        show(index - 1);
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        show(index + 1);
      }
    });

    root.addEventListener(
      "touchstart",
      function (event) {
        if (event.changedTouches.length) {
          touchX = event.changedTouches[0].clientX;
        }
      },
      { passive: true }
    );

    root.addEventListener("touchend", function (event) {
      if (touchX === null || !event.changedTouches.length) return;
      var dx = event.changedTouches[0].clientX - touchX;
      touchX = null;
      if (Math.abs(dx) < 40) return;
      show(index + (dx < 0 ? 1 : -1));
    });

    show(0);
  }
})();
