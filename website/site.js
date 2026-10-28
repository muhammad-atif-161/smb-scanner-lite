document.querySelectorAll("[data-nav]").forEach((btn) => {
  const links = document.querySelector(".links");
  btn.addEventListener("click", () => {
    const open = links.classList.toggle("open");
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    links.classList.toggle("glass", open);
  });
});
