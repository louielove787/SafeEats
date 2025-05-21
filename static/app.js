const form = document.getElementById('ingredient-form');
const resultsDiv = document.getElementById('results');
const summaryDiv = document.getElementById('summary');
const safeDiv = document.getElementById('safe');
const cautionDiv = document.getElementById('caution');
const avoidDiv = document.getElementById('avoid');
const disclaimersDiv = document.getElementById('disclaimers');

form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const text = document.getElementById('ingredients').value;
    const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ingredients: text })
    });
    if (response.ok) {
        const data = await response.json();
        summaryDiv.textContent = data.summary;
        safeDiv.textContent = `Safe: ${data.safe.join(', ')}`;
        cautionDiv.textContent = `Caution: ${data.caution.join(', ')}`;
        avoidDiv.textContent = `Avoid: ${data.avoid.join(', ')}`;
        disclaimersDiv.innerHTML = data.disclaimers.map(d => `<p>${d}</p>`).join('');
        resultsDiv.classList.remove('hidden');
    }
});
