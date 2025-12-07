(async () => {
  const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
  const employeeNames = new Set();
  let stopRequested = false;

  // Listen for ESC key to stop
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      console.warn('🛑 Manual stop requested via ESC key');
      stopRequested = true;
    }
  });

  const maxPages = 10; // ✅ LIMIT how many pages to go through

  async function extractNamesFromPage() {
    const nameElements = document.querySelectorAll('a[data-view-name="search-result-lockup-title"]');
    nameElements.forEach(el => {
      const name = el.textContent.trim();
      if (name) employeeNames.add(name);
    });
  }

  function findNextButton() {
    const xpath = "//button[.//span[text()='Next'] and not(@disabled)]";
    const result = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null);
    return result.singleNodeValue;
  }

  async function goToNextPage() {
    const nextBtn = findNextButton();
    if (nextBtn) {
      nextBtn.scrollIntoView({ behavior: "smooth", block: "center" });
      nextBtn.click();
      return true;
    }
    return false;
  }

  let page = 1;
  while (page <= maxPages && !stopRequested) {
    console.log(`🔍 Extracting page ${page}...`);
    await delay(4000);
    await extractNamesFromPage();

    const hasNext = await goToNextPage();
    if (!hasNext || stopRequested) break;

    page++;
    await delay(5000);
  }

  const nameArray = [...employeeNames];
  console.log(`✅ Done! Found ${nameArray.length} unique employees:`);
  console.log(nameArray);

  // ✅ Create downloadable file
  const blob = new Blob([nameArray.join("\n")], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "linkedin_employees.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  console.log("📁 File downloaded as linkedin_employees.txt");
})();
