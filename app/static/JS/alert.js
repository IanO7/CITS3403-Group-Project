function showOzfoodyNotification(message, type = "success", duration = 2500) {
  const notif = document.getElementById("ozfoody-notification");
  if (!notif) return;
  notif.innerHTML = message; // <-- Use innerHTML instead of textContent
  notif.className = `ozfoody-notification show ${type}`;
  notif.style.display = "block";
  setTimeout(() => {
    notif.classList.remove("show");
    setTimeout(() => { notif.style.display = "none"; }, 300);
  }, duration);
}
window.showOzfoodyNotification = showOzfoodyNotification;