// ---- Tab switching (paste text vs upload file) ----

const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanels = {
  paste: document.getElementById("tab-paste"),
  upload: document.getElementById("tab-upload"),
};

tabButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    tabButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    Object.values(tabPanels).forEach((p) => p.classList.add("hidden"));
    tabPanels[btn.dataset.tab].classList.remove("hidden");
  });
});

// ---- File chosen: show its name ----

const fileInput = document.getElementById("fileInput");
const dropzoneLabel = document.getElementById("dropzoneLabel");

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    dropzoneLabel.textContent = fileInput.files[0].name;
  }
});

// ---- Generate button ----

const generateBtn = document.getElementById("generateBtn");
const generateBtnText = document.getElementById("generateBtnText");
const errorMsg = document.getElementById("errorMsg");
const loadingOverlay = document.getElementById("loadingOverlay");
const emptyState = document.getElementById("emptyState");
const results = document.getElementById("results");

let lastResult = null;

generateBtn.addEventListener("click", async () => {
  errorMsg.classList.add("hidden");

  const activeTab = document.querySelector(".tab-btn.active").dataset.tab;
  const formData = new FormData();

  if (activeTab === "paste") {
    const text = document.getElementById("studyText").value.trim();
    if (!text) {
      showError("Please paste some text first.");
      return;
    }
    formData.append("text", text);
  } else {
    if (fileInput.files.length === 0) {
      showError("Please choose a file first.");
      return;
    }
    formData.append("file", fileInput.files[0]);
  }

  setLoading(true);

  try {
    const response = await fetch("/generate", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (!response.ok) {
      showError(data.error || "Something went wrong. Please try again.");
      return;
    }

    lastResult = data;
    renderResults(data);
  } catch (err) {
    showError("Could not reach the server. Is app.py running?");
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  generateBtn.disabled = isLoading;
  generateBtnText.textContent = isLoading ? "Generating..." : "Generate study notes";
  loadingOverlay.classList.toggle("hidden", !isLoading);
}

function showError(message) {
  errorMsg.textContent = message;
  errorMsg.classList.remove("hidden");
}

function renderResults(data) {
  emptyState.classList.add("hidden");
  results.classList.remove("hidden");

  document.getElementById("summaryText").textContent = data.summary || "";

  const keyPointsList = document.getElementById("keyPointsList");
  keyPointsList.innerHTML = "";
  (data.key_points || []).forEach((point) => {
    const li = document.createElement("li");
    li.textContent = point;
    keyPointsList.appendChild(li);
  });

  const mcqList = document.getElementById("mcqList");
  mcqList.innerHTML = "";
  (data.mcqs || []).forEach((mcq, i) => {
    const item = document.createElement("div");
    item.className = "mcq-item";

    const q = document.createElement("p");
    q.className = "mcq-question";
    q.textContent = `${i + 1}. ${mcq.question}`;
    item.appendChild(q);

    const ul = document.createElement("ul");
    ul.className = "mcq-options";
    (mcq.options || []).forEach((option) => {
      const li = document.createElement("li");
      li.textContent = option;
      if (
        typeof mcq.answer === "string" &&
        option.trim().toLowerCase().startsWith(mcq.answer.trim().toLowerCase())
      ) {
        li.classList.add("correct");
      }
      ul.appendChild(li);
    });
    item.appendChild(ul);
    mcqList.appendChild(item);
  });

  const vivaList = document.getElementById("vivaList");
  vivaList.innerHTML = "";
  (data.viva_questions || []).forEach((v, i) => {
    const item = document.createElement("div");
    item.className = "viva-item";

    const q = document.createElement("p");
    q.className = "viva-question";
    q.textContent = `${i + 1}. ${v.question}`;
    item.appendChild(q);

    const a = document.createElement("p");
    a.className = "viva-answer";
    a.textContent = v.answer;
    item.appendChild(a);

    vivaList.appendChild(item);
  });
}

// ---- Download as plain text ----

document.getElementById("downloadBtn").addEventListener("click", () => {
  if (!lastResult) return;

  let text = "AI STUDY NOTES\n================\n\n";
  text += "SUMMARY\n-------\n" + lastResult.summary + "\n\n";

  text += "KEY POINTS\n----------\n";
  (lastResult.key_points || []).forEach((p) => (text += "- " + p + "\n"));

  text += "\nMCQs\n----\n";
  (lastResult.mcqs || []).forEach((m, i) => {
    text += `${i + 1}. ${m.question}\n`;
    (m.options || []).forEach((o) => (text += "   " + o + "\n"));
    text += `   Answer: ${m.answer}\n\n`;
  });

  text += "VIVA QUESTIONS\n--------------\n";
  (lastResult.viva_questions || []).forEach((v, i) => {
    text += `${i + 1}. ${v.question}\n   ${v.answer}\n\n`;
  });

  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "study-notes.txt";
  a.click();
  URL.revokeObjectURL(url);
});
