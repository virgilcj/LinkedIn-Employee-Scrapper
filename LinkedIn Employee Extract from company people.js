(async () => {
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  const employeeNames = new Set();
  let stopRequested = false;

  // ESC to stop scroll
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      console.warn('🛑 ESC pressed. Stopping...');
      stopRequested = true;
    }
  });

  async function extractNames() {
    const nameDivs = document.querySelectorAll('a.link-without-visited-state > div.t-black');
    nameDivs.forEach(div => {
      const name = div.textContent?.trim();
      if (name) employeeNames.add(name);
    });
  }

  async function clickShowMore() {
    const button = [...document.querySelectorAll('button')].find(b =>
      b.innerText.trim().toLowerCase() === 'show more results'
    );
    if (button) {
      button.scrollIntoView({ behavior: 'smooth', block: 'center' });
      button.click();
      return true;
    }
    return false;
  }

  const maxPages = 30;
  let page = 1;

  while (page <= maxPages && !stopRequested) {
    console.log(`📄 Extracting page ${page}...`);
    await delay(4000);
    await extractNames();
    const more = await clickShowMore();
    if (!more || stopRequested) break;
    page++;
    await delay(5000);
  }

  const result = [...employeeNames];
  console.log(`✅ Done. Found ${result.length} unique employees:\n`, result);

  // 📦 Create and download TXT file
  const blob = new Blob([result.join('\n')], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'linkedin_employees.txt';
  a.click();
  URL.revokeObjectURL(url); // Cleanup

})();
