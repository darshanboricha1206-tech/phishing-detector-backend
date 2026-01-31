chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url) {

    if (
      tab.url.startsWith("chrome://") ||
      tab.url.startsWith("edge://")
    ) return;

    fetch("https://phishing-detector-backend.onrender.com/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: tab.url })
    })
    .then(res => res.json())
    .then(data => {
      console.log("Scan result:", data);

      if (data.result === "phishing") {
        chrome.notifications.create({
          type: "basic",
          iconUrl: "icon.png",
          title: "⚠️ Phishing Website Detected!",
          message: `This website is unsafe!\nConfidence: ${data.confidence}%`
        });
      }
    })
    .catch(err => {
      console.error("Fetch error:",err);
    });
  }
});