document.addEventListener("DOMContentLoaded", function () {
  const currentTheme = localStorage.getItem("admin-theme") || "dark";
  document.documentElement.setAttribute("data-theme", currentTheme);

  const toggle = document.getElementById("theme-toggle");
  if (toggle) {
    toggle.textContent = currentTheme === "dark" ? "Light mode" : "Dark mode";

    toggle.addEventListener("click", function () {
      const newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", newTheme);
      localStorage.setItem("admin-theme", newTheme);
      toggle.textContent = newTheme === "dark" ? "Light mode" : "Dark mode";
    });
  }
});
