// Records our loopback-only test harness, never the user's browser session.
const { chromium } = require('playwright');
const fs = require('node:fs/promises');
const path = require('node:path');

(async () => {
  const output = process.argv[2] || '/tmp/trustedrouter-plugin-review';
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 1000 },
    recordVideo: { dir: output, size: { width: 1440, height: 1000 } },
  });
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', (error) => errors.push(error.message));
  try {
    await page.goto('http://127.0.0.1:8176');
    await page.waitForTimeout(2000);
    for (let i = 0; i < 6; i++) {
      await page.locator('nav button').nth(i).click();
      await page.waitForFunction((index) => document.querySelector('#detail').dataset.complete === String(index) || document.querySelector('#detail').dataset.failed === String(index), i, { timeout: 120000 });
      if (await page.locator('#detail').getAttribute('data-failed') === String(i)) throw Error(await page.locator('#detail').innerText());
      await page.screenshot({ path: path.join(output, `case-${i + 1}.png`), fullPage: true });
      await page.waitForTimeout(7000);
    }
    const logs = await page.evaluate(() => window.reviewLogs);
    await fs.writeFile(path.join(output, 'actual-tool-calls.json'), JSON.stringify(logs, null, 2));
    if (errors.length) throw Error(errors.join('\n'));
    console.log(JSON.stringify({ cases: 6, calls: logs.length, screenshots: output, video: await page.video().path() }));
  } finally {
    await context.close();
    await browser.close();
  }
})().catch((error) => { console.error(error); process.exit(1); });
