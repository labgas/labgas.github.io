/* LaBGAS additions to the Minimal Mistakes front-end.
 *
 * Loaded through `after_footer_scripts` in _config.yml, so it runs after the
 * theme's own main.min.js and can react to what that script does rather than
 * replacing any of it.
 */

/* Let the browser's Back button close the search overlay.
 *
 * The theme opens search by toggling classes only — the URL never changes and
 * no history entry is added. Visually the page is replaced, so Back looks like
 * it should return to the page; instead it leaves the site altogether, and the
 * overlay has no visible close control. (Escape does close it, but that is not
 * discoverable.)
 *
 * So: push a history entry when the overlay opens, and close the overlay on
 * popstate instead of navigating. We watch the class on `.search-content`
 * rather than hooking the toggle button, because the theme opens and closes the
 * overlay from two different places — the button's click handler and a
 * document-level Escape handler — and both end up here.
 */
(function () {
  var $ = window.jQuery;
  if (!$ || !window.MutationObserver || !window.history.pushState) {
    return;
  }

  $(function () {
    var content = document.querySelector(".search-content");
    if (!content) {
      return;
    }

    // True while the extra history entry we pushed is the current one.
    var pushed = false;

    function isOpen() {
      return content.classList.contains("is--visible");
    }

    new MutationObserver(function () {
      if (isOpen() && !pushed) {
        window.history.pushState({ labgasSearch: true }, "", window.location.href);
        pushed = true;
      } else if (!isOpen() && pushed) {
        // Closed by the toggle or by Escape. Drop the entry we added, so Back
        // does not need a second press to leave the page.
        pushed = false;
        window.history.back();
      }
    }).observe(content, { attributes: true, attributeFilter: ["class"] });

    $(window).on("popstate", function () {
      if (!isOpen()) {
        return;
      }
      // Clear the flag first: closing fires the observer, which must not then
      // call history.back() and swallow a second entry.
      pushed = false;
      $(".search-content").removeClass("is--visible");
      $(".initial-content").removeClass("is--hidden");
    });
  });
})();
