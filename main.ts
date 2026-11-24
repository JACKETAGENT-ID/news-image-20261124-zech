// main.ts — validates entry.png and copies it to the output directory.
// Node standard library only. No network. Deterministic: the same input
// file always produces the same output bytes.
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const MAX_BYTES = 1024 * 1024; // 1 MiB
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function main(): void {
  const data = readFileSync(join(process.cwd(), "entry.png"));

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
