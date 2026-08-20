function mix32(value) {
  value ^= value >>> 16;
  value = Math.imul(value, 0x7feb352d);
  value ^= value >>> 15;
  value = Math.imul(value, 0x846ca68b);
  value ^= value >>> 16;
  return value >>> 0;
}

function scoreCandidates(iterations) {
  let score = 0;
  for (let i = 0; i < iterations; i += 1) {
    const mixed = mix32(i ^ score);
    score = (score + (mixed & 0xffff)) >>> 0;
  }
  return score;
}

function summarise(iterations) {
  const started = performance.now();
  const score = scoreCandidates(iterations);
  const elapsedMs = performance.now() - started;
  return { iterations, score, elapsedMs: Number(elapsedMs.toFixed(3)) };
}

const result = summarise(50_000_000);
console.log(JSON.stringify({ iterations: result.iterations, score: result.score }));
console.error(`elapsed_ms=${result.elapsedMs}`);
