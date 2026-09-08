import { existsSync, mkdirSync, mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { spawnSync } from "node:child_process";

const currentDir = path.dirname(fileURLToPath(import.meta.url));
const chromePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const outputDir = path.join(currentDir, "imgs");
const sourceUrl = pathToFileURL(path.join(currentDir, "card.html")).href;
const outputNames = [
  "01-gpt-6-astra.png",
  "02-gpt-6-astra.png",
  "03-gpt-6-astra.png",
];

mkdirSync(outputDir, { recursive: true });

for (let index = 0; index < outputNames.length; index += 1) {
  const tempProfile = mkdtempSync(path.join(tmpdir(), "gpt6-astra-card-"));
  const outputPath = path.join(outputDir, outputNames[index]);
  const result = spawnSync(
    "/opt/homebrew/bin/timeout",
    [
      "15",
      chromePath,
      "--headless=new",
      "--disable-gpu",
      "--no-sandbox",
      "--hide-scrollbars",
      "--run-all-compositor-stages-before-draw",
      "--no-first-run",
      "--disable-default-apps",
      "--force-device-scale-factor=1",
      "--window-size=900,1200",
      "--virtual-time-budget=800",
      "--user-data-dir=" + tempProfile,
      "--screenshot=" + outputPath,
      sourceUrl + "?card=" + (index + 1),
    ],
    { encoding: "utf8" },
  );

  rmSync(tempProfile, { recursive: true, force: true });

  if (!existsSync(outputPath)) {
    throw new Error(result.stderr || "Chrome rendering failed");
  }

  const resize = spawnSync(
    "sips",
    ["-z", "1440", "1080", outputPath],
    { encoding: "utf8" },
  );

  if (resize.status !== 0) {
    throw new Error(resize.stderr || "Image resizing failed");
  }

  console.log(outputPath);
}
