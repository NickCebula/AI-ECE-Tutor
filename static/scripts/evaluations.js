document.getElementById("username-display").innerText = localStorage.getItem("username") || "Guest";

function generateEvaluation() {
  const now = new Date();
  const entry = document.createElement("p");
  entry.innerText = `${now.toLocaleDateString()} ${now.toLocaleTimeString()} — Evaluation created`;

  const log = document.getElementById("evaluations-log");
  if (log.children[0]?.innerText.includes("No evaluations")) log.innerHTML = "";
  log.appendChild(entry);
}