// main.ts — entrypoint for the make.fun bounty "news-image-20261120"
// ("Sum up 20 November's world news in one image").
//
// The entry image is finished artwork that ships inside this repository
// as entry.png, so the program's whole job is to deliver it, untouched,
// to /output/entry.png. Copying a bundled file also guarantees the two
// grading runs produce byte-identical output: no clocks, no randomness,
// no network — the same bytes in, the same bytes out.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const source = join(repoDir, "entry.png");

const outDir = "/output";
const destination = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(source, destination);

console.log(`entry image delivered to ${destination}`);
