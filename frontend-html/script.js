const form = document.getElementById('uploadForm');
const fileInput = document.getElementById('fileInput');
const resultBox = document.getElementById('result');
const imagePreview = document.getElementById('imagePreview');

fileInput.addEventListener('change', () => {
  const file = fileInput.files[0];
  if (file) {
    imagePreview.src = URL.createObjectURL(file);
    imagePreview.style.display = 'block';
    resultBox.style.display = 'none';
  }
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  resultBox.textContent = "Diagnosing... Please wait ⏳";
  resultBox.style.display = 'block';

  try {
    const response = await fetch("http://localhost:8001/predict", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    resultBox.innerHTML = `✅ <strong>${data.class}</strong><br/>🎯 Confidence: ${(data.confidence * 100).toFixed(2)}%`;
  } catch (err) {
    console.error(err);
    resultBox.textContent = "❌ Error connecting to the prediction server.";
  }
});
