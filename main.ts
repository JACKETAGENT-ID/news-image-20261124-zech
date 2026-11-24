// main.ts — validates entry.png and copies it to the output directory.
// Node standard library only. No network. Deterministic: the same input
// file always produces the same output bytes.
//
// The image is resolved relative to this script's own directory
// (dirname(fileURLToPath(import.meta.url))), NOT relative to the current
// working directory: the grader runs `node /bot/main.ts` from an arbitrary
// working directory, so a cwd-based lookup fails with ENOENT.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024; // 1 MiB
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function main(): void {
  const scriptDir = dirname(fileURLToPath(import.meta.url));
  const data = readFileSync(join(scriptDir, "entry.png"));

  if (data.length > MAX_BYTES) {
    throw new Error(`entry.png is ${data.length} bytes, over the 1 MiB cap`);
  }
  if (data.length < 24 || !data.subarray(0, 8).equals(PNG_SIG)) {
    throw new Error("entry.png does not start with the PNG signature");
  }
  // IHDR chunk: width and height are big-endian uint32 at offsets 16 and 20.
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width > 1024 || height > 1024) {
    throw new Error(`entry.png is ${width}x${height}, over 1024x1024`);
  }

  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, "entry.png"), data);
  console.log(`entry.png: ${width}x${height}, ${data.length} bytes -> ${outDir}/entry.png`);
}

main();
