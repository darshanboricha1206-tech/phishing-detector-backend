async function checkWebsite() {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

  fetch("https://phishing-detector-backend.onrender.com/check", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url: tab.url })
})
  .then(res => res.json())
  .then(data => {
    const result = document.getElementById("result");
    if (data.result === "phishing") {
      result.innerText = `❌ Phishing Website (${data.confidence}%)`;
      result.style.color = "red";
    } else {
      result.innerText = `✅ Safe Website (${data.confidence}%)`;
      result.style.color = "green";
    }
  });
}

document.addEventListener("DOMContentLoaded", checkWebsite);