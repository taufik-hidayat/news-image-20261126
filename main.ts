// Entry point: copy entry.png into the output directory and validate it.
// Node 22, standard library only. No network, no randomness, no clock:
// two runs write byte-identical output.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576;
const SOURCE = "entry.png";

// entry.png sits beside this file. Works in ESM (import.meta.url) and in
// CommonJS (__dirname) alike, so the entrypoint runs under either loader.
const HERE =
  typeof __dirname !== "undefined"
    ? __dirname
    : dirname(fileURLToPath(import.meta.url));

function main(): void {
  const sourcePath = join(HERE, SOURCE);
  if (!existsSync(sourcePath)) {
    throw new Error(`missing ${SOURCE} next to main.ts (${sourcePath})`);
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const outPath = join(resolve(outDir), SOURCE);
  copyFileSync(sourcePath, outPath);
  const data = readFileSync(outPath);
  if (data.length > MAX_BYTES) {
    throw new Error(
      `entry.png is ${data.length} bytes, over the ${MAX_BYTES} byte limit`,
    );
  }
  if (!data.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error("entry.png does not start with the PNG signature");
  }
  console.log(`wrote ${outPath} (${data.length} bytes, PNG signature OK)`);
}

main();
