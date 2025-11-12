const uploadForm = document.getElementById("uploadForm");
const askForm = document.getElementById("askForm");
const statusDiv = document.getElementById("status");
const responseDiv = document.getElementById("response");

uploadForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);
  statusDiv.innerHTML = "📘 Procesando y entrenando...";
  const res = await fetch("/upload/", { method: "POST", body: formData });
  const data = await res.json();
  statusDiv.innerHTML = "✅ " + data.status;
});

askForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(askForm);
  responseDiv.innerHTML = "⌛ Pensando...";
  const res = await fetch("/ask/", { method: "POST", body: formData });
  const data = await res.json();
  responseDiv.innerHTML = "🧠 <b>Respuesta:</b><br>" + data.response;
});
