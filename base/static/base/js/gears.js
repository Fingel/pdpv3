let gear = document.getElementById("gear1");
window.scrollStopped = function (callback) {
  let previousScroll = 0;
  window.addEventListener("scroll", function () {
    let currentScroll =
      document.documentElement.scrollTop || document.body.scrollTop;
    if (currentScroll > previousScroll) {
      gear.classList = "go-counter-clockwise";
    } else {
      gear.classList = "go-clockwise";
    }
    previousScroll = currentScroll;

    if (gear.getAttribute("scrollTimeout")) {
      clearTimeout(gear.getAttribute("scrollTimeout"));
    }
    gear.setAttribute("scrollTimeout", setTimeout(callback, 150, self));
  });
};

window.scrollStopped(function () {
  gear.classList = "";
});
