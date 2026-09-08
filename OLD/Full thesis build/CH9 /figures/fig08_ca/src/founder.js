const Sim = require('./sim.js');

const SEED = 20260903;
const FRAME = 80000;          // the page's own default speed, per the CA doc
const E = Sim.E, BETA = Sim.beta;

Sim.setGridSize(256);
Sim.srand(SEED);
Sim.reset();

const rows = [];
let burstT = null, peakA = 0, peakT = 0, maxX = 0, areaAtBurst = 0, alphaAtBurst = 0;
let lastSeen = null;

for (let frame = 0; frame < 4000 && burstT === null; frame++) {
    Sim.step(FRAME);
    const samples = Sim.drainGraphSamples();
    for (const s of samples) {
        // founder is tag 0
        let idx = -1;
        for (let i = 0; i < s.ids.length; i++) if (s.ids[i] === 0) { idx = i; break; }
        if (idx === -1) { if (burstT === null) burstT = s.time; break; }
        const N = s.area[idx], a = s.energy[idx], X = s.diversity[idx];
        rows.push([s.time, a, X, N, N * E / BETA]);
        if (a > peakA) { peakA = a; peakT = s.time; }
        if (X > maxX) maxX = X;
        lastSeen = [s.time, a, X, N];
    }
}
if (lastSeen) { alphaAtBurst = lastSeen[1]; areaAtBurst = lastSeen[3]; }

console.error(`E=${E.toFixed(4)} beta=${BETA.toFixed(4)} beta/E=${(BETA/E).toFixed(2)}`);
console.error(`burst at t=${burstT===null?'n/a':burstT.toFixed(1)}  peak alpha=${peakA.toFixed(0)} at t=${peakT.toFixed(0)}`);
console.error(`at last sample: alpha=${alphaAtBurst.toFixed(0)} X=${maxX} area=${areaAtBurst}`);
console.error(`rows=${rows.length}`);

let out = 't alpha X N balance\n';
for (const r of rows) out += r.map(v => (+v).toFixed(4)).join(' ') + '\n';
require('fs').writeFileSync(process.argv[2] || 'founder.dat', out);
