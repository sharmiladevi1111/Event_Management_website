document.addEventListener("DOMContentLoaded", function () {
  // Mobile nav toggle
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  // Filter dropdowns (Events page)
  var dropdownToggles = document.querySelectorAll(".filter-toggle");
  dropdownToggles.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var menu = btn.nextElementSibling;
      document.querySelectorAll(".filter-menu.open").forEach(function (m) {
        if (m !== menu) m.classList.remove("open");
      });
      menu.classList.toggle("open");
    });
  });

  document.addEventListener("click", function () {
    document.querySelectorAll(".filter-menu.open").forEach(function (m) {
      m.classList.remove("open");
    });
  });

  // Booking form "Call for Instant Booking" quick action
  var callBtn = document.getElementById("callInstantBooking");
  if (callBtn) {
    callBtn.addEventListener("click", function () {
      window.location.href = "tel:" + callBtn.dataset.phone;
    });
  }
});
