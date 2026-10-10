
const Sim = (function () {
'use strict';

let GRID_N = 256;
let CELLS_N = GRID_N * GRID_N;
let SHIFT = 8;
let MASK = GRID_N - 1;

const EMPTY = 0xffffffff;
const CHUNK = 256;
const CHUNK_MAX = 4096;
const SAMPLE_CAP = 128;
const HUE_STEP = 7;
const GRAPH_TIME_PER_SAMPLE = 2;
const BURST_LOG = 512;

// A Moore neighbourhood on a torus, throughout.
const DI = [1, 1, 1, 0, -1, -1, -1, 0];
const DJ = [1, 0, -1, -1, -1, 0, 1, 1];

const MUT_CONST = 0;
const MUT_ALPHA = 1;
const CHILD_RESET = 0;
const CHILD_EQUAL = 1;
const CHILD_AREA = 2;
const HUE_REDRAW = 0;
const HUE_THERMO = 1;
const HUE_SPREAD = 2;
const HUE_JITTER = 3;
const HEAT_X_REF = 8;
const DEG2RAD = Math.PI / 180;
const SUBSTEP_MAX = 64;
const EM_SAFETY = 0.24;
const TII_TIE = 0;
const TII_BIAS = 1;
const SUP_OFF = 0;
const SUP_ON = 1;

const EMPTY_RGB = [11, 13, 17];

let mutMode = MUT_ALPHA;
let childMode = CHILD_RESET;
let typeIIMode = TII_BIAS;
let supportMode = SUP_ON;
let hueMode = HUE_JITTER;

let dRaw = 0.9;
let paramE = Math.pow(10, -1.5);      // 0.0316
let paramBeta = Math.pow(10, -0.54);  // 0.288
let paramM = Math.pow(10, -4.05);     // 8.9e-5
let paramDelta = Math.pow(10, -2.15); // 7.1e-3
let alpha0 = 0.01;
let paramLambda = 1.14;
let paramTheta = 3;

// A burst gives its fragments a finite morph: the noise ramps linearly down to
// nothing over paramSettle sweeps and then stops dead, so a settled species
// holds its colour exactly until it fragments in turn. D is the design dial —
// the total displacement delivered inside that window.
let paramDispersal = 90;
let paramSettle = 2;

// Settling proper: a drift -alpha*sin(k*theta) toward k stable hues, so a
// fragment does not merely stop diffusing but is gathered into a definite
// colour and held there. alpha = 0 leaves the walk to stop where it lies.
let paramDrift = 2;
let paramWells = 12;
let paramSpread = 2;
let paramJitter = 47;

// (n+1)^theta for the nine possible Moore counts, rebuilt when theta moves.
const supportW = new Float64Array(9);

let cells;
let pixels;
let occupied;
let occupiedN = 0;

let subs = [];
let deadSubs = [];
let aliveSubs = [];
let speciesList = [];
let deadSpecies = [];
let aliveSpecies = [];

// A species record is recycled once it is dead, so speciesList stops at the
// high-water mark of concurrent species instead of growing for the life of the
// run. The slot is what sub.sp indexes; the tag is a serial number that is
// never reused, so a graph trace or a label cannot jump from a dead species to
// the live one that inherited its slot.
let speciesTag = 0;

let simTime = 0;
let totalEvents = 0;
let expansions = 0;
let innerContests = 0;
let contests = 0;
let mutations = 0;
let bursts = 0;
let subsEver = 0;
let alphaMax = 1;
let mutDebt = 1;
let paintDirty = false;

let nextGraphTime = GRAPH_TIME_PER_SAMPLE;
const graphSamples = [];
const burstTimes = [];

let rngCtx = 0;
let hueRngCtx = 0;

function allocate() {
    cells = new Uint32Array(CELLS_N);
    pixels = new Uint8ClampedArray(CELLS_N * 4);
    occupied = new Uint32Array(CELLS_N);
}

function srand(seed) {
    rngCtx = seed >>> 0;
    // Hue noise runs on its own stream, so switching the thermostat on leaves
    // the spatial trajectory for a given seed untouched, cell for cell.
    hueRngCtx = ((seed ^ 0x9e3779b9) >>> 0) || 1;
}

function rand() {
    if (rngCtx === 0) rngCtx = 123459876;
    const hi = (rngCtx / 127773) | 0;
    const lo = rngCtx % 127773;
    let value = 16807 * lo - 2836 * hi;
    if (value < 0) value += 0x7fffffff;
    rngCtx = value;
    return value;
}

function randomUnit() {
    return rand() / 0x7fffffff;
}

function hueRand() {
    if (hueRngCtx === 0) hueRngCtx = 123459876;
    const hi = (hueRngCtx / 127773) | 0;
    const lo = hueRngCtx % 127773;
    let value = 16807 * lo - 2836 * hi;
    if (value < 0) value += 0x7fffffff;
    hueRngCtx = value;
    return value;
}

// Box-Muller, uncached: two draws in, one normal out, no state to carry.
function hueNormal() {
    const u = (hueRand() / 0x7fffffff) || 1e-12;
    const v = hueRand() / 0x7fffffff;
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// Total variance a fragment of multiplicity X should accumulate, in deg^2.
function morphVariance(count) {
    return paramDispersal * paramDispersal * count / HEAT_X_REF;
}

function exponential() {
    return -Math.log(randomUnit() || 1e-12);
}

// Hue is the whole of the taxonomy: saturation and brightness are held fixed.
function hsbToRgb(hue, saturation, brightness) {
    const hp = ((hue % 360) + 360) % 360 / 60;
    const c = brightness * saturation;
    const x = c * (1 - Math.abs(hp % 2 - 1));
    let r = 0;
    let g = 0;
    let b = 0;

    if (hp < 1) { r = c; g = x; }
    else if (hp < 2) { r = x; g = c; }
    else if (hp < 3) { g = c; b = x; }
    else if (hp < 4) { g = x; b = c; }
    else if (hp < 5) { r = x; b = c; }
    else { r = c; b = x; }

    const m = brightness - c;
    return [
        Math.round((r + m) * 255),
        Math.round((g + m) * 255),
        Math.round((b + m) * 255)
    ];
}

function paintRgb(record, hue) {
    const rgb = hsbToRgb(hue, 0.72, 0.95);
    record.r = rgb[0];
    record.g = rgb[1];
    record.b = rgb[2];
}

function paintRecord(record, hue) {
    paintRgb(record, hue);
    record.css = 'rgb(' + record.r + ', ' + record.g + ', ' + record.b + ')';
}

function makeSpecies(hue) {
    let sp;

    if (deadSpecies.length > 0) {
        sp = speciesList[deadSpecies.pop()];
        sp.alpha = 0;
        sp.cells = 0;
        sp.subsAlive = 0;
        sp.subsEver = 0;
        sp.heat = 0;
        sp.cool = 0;
        sp.hue = hue;
        sp.alive = true;
        sp.subList.length = 0;
    } else {
        sp = {
            id: speciesList.length,
            tag: 0,
            alpha: 0,
            cells: 0,
            subsAlive: 0,
            subsEver: 0,
            heat: 0,
            cool: 0,
            hue: hue,
            alive: true,
            slot: -1,
            subList: [],
            r: 0,
            g: 0,
            b: 0,
            css: ''
        };
        speciesList.push(sp);
    }

    sp.tag = speciesTag++;
    paintRecord(sp, hue);
    sp.slot = aliveSpecies.length;
    aliveSpecies.push(sp);
    return sp;
}

function killSpecies(sp) {
    if (!sp.alive) return;
    sp.alive = false;
    const last = aliveSpecies.pop();
    if (last !== sp) {
        aliveSpecies[sp.slot] = last;
        last.slot = sp.slot;
    }
    sp.slot = -1;
    // Its sub-species were killed first, so nothing indexes this slot now.
    deadSpecies.push(sp.id);
}

function makeSub(sp, hue) {
    let sub;
    if (deadSubs.length > 0) {
        sub = subs[deadSubs.pop()];
    } else {
        sub = {
            id: subs.length,
            sp: 0,
            hue: 0,
            count: 0,
            slot: -1,
            aliveSlot: -1,
            r: 0,
            g: 0,
            b: 0
        };
        subs.push(sub);
    }
    sub.sp = sp.id;
    sub.hue = hue;
    sub.count = 0;
    sub.slot = sp.subList.length;
    sp.subList.push(sub.id);
    sub.aliveSlot = aliveSubs.length;
    aliveSubs.push(sub.id);
    sp.subsAlive++;
    sp.subsEver++;
    subsEver++;
    paintRgb(sub, hue);
    return sub;
}

function killSub(sub, sp) {
    const list = sp.subList;
    const last = list.pop();
    if (last !== sub.id) {
        list[sub.slot] = last;
        subs[last].slot = sub.slot;
    }
    sub.slot = -1;

    const aliveLast = aliveSubs.pop();
    if (aliveLast !== sub.id) {
        aliveSubs[sub.aliveSlot] = aliveLast;
        subs[aliveLast].aliveSlot = sub.aliveSlot;
    }
    sub.aliveSlot = -1;

    sp.subsAlive--;
    deadSubs.push(sub.id);
}

function updatePixel(index) {
    const sub = cells[index];
    const offset = index * 4;
    if (sub === EMPTY) {
        pixels[offset] = EMPTY_RGB[0];
        pixels[offset + 1] = EMPTY_RGB[1];
        pixels[offset + 2] = EMPTY_RGB[2];
    } else {
        const record = subs[sub];
        pixels[offset] = record.r;
        pixels[offset + 1] = record.g;
        pixels[offset + 2] = record.b;
    }
    pixels[offset + 3] = 255;
}

function repaintAll() {
    for (let index = 0; index < CELLS_N; index++) updatePixel(index);
}

// Increment before decrement, so a species never looks momentarily extinct.
function changeCell(index, subId) {
    const previous = cells[index];
    if (previous === subId) return;

    const next = subs[subId];
    next.count++;
    speciesList[next.sp].cells++;

    if (previous === EMPTY) {
        occupied[occupiedN++] = index;
    } else {
        const old = subs[previous];
        const oldSp = speciesList[old.sp];
        old.count--;
        oldSp.cells--;
        if (old.count === 0) killSub(old, oldSp);
        if (oldSp.cells === 0) killSpecies(oldSp);
    }

    cells[index] = subId;
    updatePixel(index);
}

function chooseNeighbour(index) {
    const direction = rand() % 8;
    const row = ((index >> SHIFT) + DI[direction]) & MASK;
    const column = ((index & MASK) + DJ[direction]) & MASK;
    return (row << SHIFT) | column;
}

function rebuildSupport() {
    for (let n = 0; n <= 8; n++) supportW[n] = Math.pow(n + 1, paramTheta);
}

// Identity is read at the level of the contest: the sub-species label in a
// Type II event, the species label in a Type III one.
function sameNeighbours(index, identity, speciesLevel) {
    const row = index >> SHIFT;
    const column = index & MASK;
    let count = 0;

    for (let direction = 0; direction < 8; direction++) {
        const r = (row + DI[direction]) & MASK;
        const c = (column + DJ[direction]) & MASK;

        const occupant = cells[(r << SHIFT) | c];
        if (occupant === EMPTY) continue;
        if (speciesLevel ? subs[occupant].sp === identity : occupant === identity) count++;
    }

    return count;
}

// Type I: empty ground is a rival of fixed strength d, and never invades. A
// cell takes empty ground with probability 1 - d, whatever its energy.
function expandProbability() {
    return 1 - dRaw;
}

function xOf(sp) {
    return sp.subsAlive;
}

function competition(events) {
    for (let event = 0; event < events; event++) {
        const index = rand() % CELLS_N;
        const other = chooseNeighbour(index);
        if (other < 0) continue;

        const here = cells[index];
        const there = cells[other];
        if (here === there) continue;

        if (here === EMPTY || there === EMPTY) {
            const occupier = here === EMPTY ? there : here;
            const target = here === EMPTY ? index : other;
            if (randomUnit() < expandProbability()) {
                changeCell(target, occupier);
                expansions++;
            }
            continue;
        }

        const spHere = subs[here].sp;
        const spThere = subs[there].sp;

        let pHere;
        if (spHere === spThere) {
            innerContests++;
            const biased = typeIIMode === TII_BIAS && paramLambda > 0;

            if (supportMode === SUP_ON || biased) {
                // Two Bradley-Terry factors on a shared parent alpha, which
                // cancels: local support (n+1)^theta, and a global rare
                // advantage e^(-lambda K/kappa). Either factor is 1 when its
                // toggle is off. Written against sub-species a's strength so
                // only the area difference is exponentiated, which cannot
                // overflow harmfully: e^z -> inf gives P = 0, e^z -> 0 gives 1.
                const hHere = supportMode === SUP_ON
                    ? supportW[sameNeighbours(index, here, false)] : 1;
                const hThere = supportMode === SUP_ON
                    ? supportW[sameNeighbours(other, there, false)] : 1;
                let bias = 1;

                if (biased) {
                    const sp = speciesList[spHere];
                    const kappa = sp.cells / sp.subsAlive;
                    bias = Math.exp(paramLambda * (subs[here].count - subs[there].count) / kappa);
                }

                pHere = hHere / (hHere + hThere * bias);
            } else {
                pHere = 0.5;
            }
        } else {
            contests++;
            let alphaHere = speciesList[spHere].alpha;
            let alphaThere = speciesList[spThere].alpha;

            // Energy stays the species-level bias; support modulates it by
            // local compactness. Occupancy does not reach this contest.
            if (supportMode === SUP_ON) {
                alphaHere *= supportW[sameNeighbours(index, spHere, true)];
                alphaThere *= supportW[sameNeighbours(other, spThere, true)];
            }

            const total = alphaHere + alphaThere;
            pHere = total > 0 ? alphaHere / total : 0.5;
        }

        if (randomUnit() < pHere) changeCell(other, here);
        else changeCell(index, there);
    }
}

function fireMutation() {
    const index = occupied[rand() % occupiedN];
    const parent = subs[cells[index]];
    const sp = speciesList[parent.sp];

    // Thinning: the per-cell rate m*alpha is sampled against the largest alpha.
    if (mutMode === MUT_ALPHA) {
        if (alphaMax <= 0 || randomUnit() >= sp.alpha / alphaMax) return;
    }

    const child = makeSub(sp, parent.hue + HUE_STEP * (randomUnit() * 2 - 1));
    changeCell(index, child.id);
    mutations++;
}

function mutationPass(dtChunk) {
    if (paramM <= 0 || occupiedN === 0) return;
    const rate = mutMode === MUT_ALPHA
        ? paramM * alphaMax * occupiedN
        : paramM * occupiedN;
    if (!(rate > 0)) return;

    mutDebt -= rate * dtChunk;
    while (mutDebt <= 0) {
        fireMutation();
        mutDebt += exponential();
    }
}

// Every sub-species breaks away at once; the domains do not move, only the law
// by which they interact, which switches from Type II to Type III.
function fragment(sp) {
    // energyPass collects the bursting species before it fragments any of
    // them; refuse a record that has since died, so a recycled slot can never
    // be fragmented a second time.
    if (!sp.alive) return;

    const children = sp.subList.slice();
    if (children.length < 2) return;

    const parentAlpha = Math.max(0, sp.alpha);
    const parentCells = sp.cells;

    // Read the family's centre hue before anything is reassigned, so every
    // fragment is measured against the same parent average.
    const meanHue = hueMode === HUE_SPREAD ? circularMean(children, sp.hue) : 0;

    for (let i = 0; i < children.length; i++) {
        const sub = subs[children[i]];

        // A sub-species holds its hue for as long as it is one. Under the
        // redraw rule it then draws a fresh hue from the circle and fixes
        // there; under the thermostat it keeps the hue it has and inherits the
        // heat that the parent's multiplicity paid for, walking away from its
        // siblings as that heat decays.
        // The draw happens either way, used only under the redraw rule, so the
        // contest stream stays aligned and switching the thermostat on cannot
        // move a single cell.
        const fresh = randomUnit() * 360;
        if (hueMode === HUE_REDRAW) {
            sub.hue = fresh;
            paintRgb(sub, sub.hue);
        } else if (hueMode === HUE_JITTER) {
            // Each fragment steps off its own hue by a normal draw: the family
            // stays recognisable, the siblings separate. Drawn on the hue
            // stream, so the contest stream is undisturbed.
            sub.hue = ((sub.hue + paramJitter * hueNormal()) % 360 + 360) % 360;
            paintRgb(sub, sub.hue);
        } else if (hueMode === HUE_SPREAD) {
            // Push each fragment g times its own offset from the family mean,
            // in the direction it already lay: the siblings fan apart along the
            // lines their mutations had started.
            const offset = hueDelta(sub.hue, meanHue);
            sub.hue = ((meanHue + paramSpread * offset) % 360 + 360) % 360;
            paintRgb(sub, sub.hue);
        }

        const child = makeSpecies(sub.hue);

        if (hueMode === HUE_THERMO && paramSettle > 0) {
            // Variance rate falls linearly from peak to zero across the window,
            // so the integral over it is exactly the variance we want and the
            // motion eases to a stop rather than being cut off.
            const peak = 2 * morphVariance(children.length) / paramSettle;
            child.heat = peak;
            child.cool = peak / paramSettle;
        }

        if (childMode === CHILD_RESET) {
            child.alpha = alpha0;
        } else if (childMode === CHILD_EQUAL) {
            child.alpha = parentAlpha / children.length;
        } else {
            child.alpha = parentCells > 0 ? parentAlpha * sub.count / parentCells : 0;
        }

        child.cells = sub.count;
        child.subsAlive = 1;
        child.subsEver = 1;
        // Mutate the list rather than replacing it: a recycled record keeps its
        // array, so a burst allocates nothing per child.
        child.subList.length = 0;
        child.subList.push(sub.id);
        sub.sp = child.id;
        sub.slot = 0;
    }

    sp.subList.length = 0;
    sp.subsAlive = 0;
    sp.cells = 0;
    killSpecies(sp);

    paintDirty = true;
    bursts++;
    burstTimes.push(simTime);
    if (burstTimes.length > BURST_LOG) burstTimes.shift();
}

// The variance rate is linear in time, so its integral over a chunk is exact:
// heat*dt - cool*dt^2/2, clipped at the moment the window closes. Total
// dispersal is therefore D*sqrt(X/8) whatever the chunk size, and a species
// whose window has closed is frozen — heat is exactly zero, not merely small.
// Hue is a circle, so the centre of a set of hues is the direction of their
// resultant, not their arithmetic mean: 350 and 10 average to 0, not to 180.
function circularMean(ids, fallback) {
    let x = 0;
    let y = 0;

    for (let i = 0; i < ids.length; i++) {
        const radians = subs[ids[i]].hue * DEG2RAD;
        x += Math.cos(radians);
        y += Math.sin(radians);
    }

    // A perfectly balanced ring has no mean direction; keep the parent's hue.
    if (Math.abs(x) < 1e-12 && Math.abs(y) < 1e-12) return fallback;
    return ((Math.atan2(y, x) / DEG2RAD) % 360 + 360) % 360;
}

// Signed separation of two hues, in (-180, 180].
function hueDelta(hue, from) {
    return ((hue - from + 540) % 360) - 180;
}

function nearestWell(hue) {
    const spacing = 360 / paramWells;
    return Math.round(hue / spacing) * spacing;
}

// Euler-Maruyama on the hue circle: a noise pulse that ramps to nothing across
// the settling window, against a drift that gathers the hue into one of the
// wells. The variance rate is linear in time so its integral over a substep is
// exact; the substep itself is bounded by the solver's stability limit, since
// the drift stiffens with alpha*k. When the window closes the hue is placed on
// its well and frozen: heat is exactly zero, and a settled species holds its
// colour until it fragments in turn.
function huePass(dtChunk) {
    if (hueMode !== HUE_THERMO) return;

    const stiffness = paramDrift * paramWells * DEG2RAD;
    const limit = EM_SAFETY / (stiffness + 1);
    let steps = 1;

    if (paramDrift > 0 && dtChunk > limit) {
        steps = Math.ceil(dtChunk / limit);
        if (steps > SUBSTEP_MAX) steps = SUBSTEP_MAX;
    }

    const ds = dtChunk / steps;
    let touched = false;

    for (let i = 0; i < aliveSpecies.length; i++) {
        const sp = aliveSpecies[i];

        if (sp.heat <= 0) continue;

        let hue = sp.hue;
        let closed = false;

        for (let n = 0; n < steps; n++) {
            let variance = 0;

            if (sp.heat > 0) {
                const left = sp.cool > 0 ? sp.heat / sp.cool : ds;
                const span = ds < left ? ds : left;

                variance += sp.heat * span - 0.5 * sp.cool * span * span;
                sp.heat -= sp.cool * span;

                if (sp.heat <= 0 || span >= left) {
                    sp.heat = 0;
                    sp.cool = 0;
                    closed = true;
                }
            }

            if (paramDrift > 0) {
                hue -= paramDrift * Math.sin(paramWells * hue * DEG2RAD) * ds;
            }
            if (variance > 0) hue += Math.sqrt(variance) * hueNormal();
        }

        if (closed && paramDrift > 0) hue = nearestWell(hue);

        // One increment for the whole species: the band moves as a body, so the
        // +/-HUE_STEP structure mutation builds inside it survives the walk.
        const move = hue - sp.hue;
        sp.hue = ((hue % 360) + 360) % 360;
        paintRecord(sp, sp.hue);

        for (let k = 0; k < sp.subList.length; k++) {
            const sub = subs[sp.subList[k]];
            sub.hue = ((sub.hue + move) % 360 + 360) % 360;
            paintRgb(sub, sub.hue);
        }

        touched = true;
    }

    if (touched) paintDirty = true;
}

function energyPass(dtChunk) {
    let pending = null;
    let maxAlpha = 0;

    for (let i = 0; i < aliveSpecies.length; i++) {
        const sp = aliveSpecies[i];
        const x = xOf(sp);
        const next = sp.alpha + dtChunk * (sp.cells * paramE - paramBeta * x);
        let burst = false;

        if (next <= 0) {
            burst = true;
        } else if (x > 0) {
            const rate = paramDelta * x / next;
            if (randomUnit() < -Math.expm1(-rate * dtChunk)) burst = true;
        }

        sp.alpha = next > 0 ? next : 0;
        if (sp.alpha > maxAlpha) maxAlpha = sp.alpha;

        if (burst && sp.subList.length >= 2) {
            if (pending === null) pending = [];
            pending.push(sp);
        }
    }

    alphaMax = maxAlpha > 0 ? maxAlpha : alpha0;
    if (pending === null) return;

    for (let i = 0; i < pending.length; i++) fragment(pending[i]);
}

// A sample keeps only the largest species, which is all the graph ever draws.
function sampleState() {
    // Always copy before sorting: aliveSpecies carries the slot index of every
    // live record, and reordering it in place would invalidate every slot.
    let chosen = aliveSpecies.slice();
    if (chosen.length > SAMPLE_CAP) {
        chosen.sort(function (a, b) { return b.cells - a.cells; });
        chosen = chosen.slice(0, SAMPLE_CAP);
    }

    // A sample is keyed by tag, not by slot: slots are recycled, so a trace
    // keyed by slot could jump from a dead species to the live one that took
    // its place. Held in tag order for the graph's binary search.
    chosen.sort(function (a, b) { return a.tag - b.tag; });

    const count = chosen.length;
    const ids = new Int32Array(count);
    const area = new Float32Array(count);
    const energy = new Float32Array(count);
    const diversity = new Float32Array(count);
    // The colour travels with the sample. A dead species' record is recycled, so
    // by the time its trace is drawn the slot may hold another species entirely,
    // and speciesList can no longer say what colour the line was.
    const rgb = new Uint8Array(count * 3);
    for (let i = 0; i < count; i++) {
        const sp = chosen[i];
        ids[i] = sp.tag;
        area[i] = sp.cells;
        energy[i] = sp.alpha;
        diversity[i] = xOf(sp);
        rgb[i * 3] = sp.r;
        rgb[i * 3 + 1] = sp.g;
        rgb[i * 3 + 2] = sp.b;
    }

    return {
        time: simTime,
        empty: CELLS_N - occupiedN,
        ids: ids,
        area: area,
        energy: energy,
        diversity: diversity,
        rgb: rgb
    };
}

function captureGraphSample() {
    graphSamples.push(sampleState());
}

function resetSimulation() {
    cells.fill(EMPTY);
    occupiedN = 0;
    subs = [];
    deadSubs = [];
    aliveSubs = [];
    speciesList = [];
    deadSpecies = [];
    aliveSpecies = [];
    speciesTag = 0;

    simTime = 0;
    totalEvents = 0;
    expansions = 0;
    innerContests = 0;
    contests = 0;
    mutations = 0;
    bursts = 0;
    subsEver = 0;
    alphaMax = alpha0;
    mutDebt = exponential();
    nextGraphTime = GRAPH_TIME_PER_SAMPLE;
    graphSamples.length = 0;
    burstTimes.length = 0;
    paintDirty = false;

    const founder = makeSpecies(randomUnit() * 360);
    founder.alpha = alpha0;
    const seed = makeSub(founder, founder.hue);
    repaintAll();
    changeCell((GRID_N >> 1) * GRID_N + (GRID_N >> 1), seed.id);
}

function chunkFor() {
    const wanted = aliveSpecies.length * 4;
    if (wanted <= CHUNK) return CHUNK;
    return wanted > CHUNK_MAX ? CHUNK_MAX : wanted;
}

function step(events) {
    let left = events;
    while (left > 0) {
        const chunk = chunkFor();
        const size = left < chunk ? left : chunk;
        const dtChunk = size / CELLS_N;

        competition(size);
        simTime += dtChunk;
        totalEvents += size;
        mutationPass(dtChunk);
        energyPass(dtChunk);
        huePass(dtChunk);
        left -= size;

        while (simTime >= nextGraphTime) {
            captureGraphSample();
            nextGraphTime += GRAPH_TIME_PER_SAMPLE;
        }
    }

    // Once per call rather than once per chunk: hues move continuously under
    // the thermostat, and a full repaint per chunk would be a hundred passes
    // over the buffer per frame.
    if (paintDirty) {
        repaintAll();
        paintDirty = false;
    }
}

function drainGraphSamples() {
    if (graphSamples.length === 0) return [];
    return graphSamples.splice(0);
}

function setGridSize(size) {
    if (size < 2 || (size & (size - 1)) !== 0) return;
    GRID_N = size;
    CELLS_N = size * size;
    SHIFT = Math.round(Math.log2(size));
    MASK = size - 1;
    allocate();
    resetSimulation();
}

function clampPositive(value, fallback) {
    return Number.isFinite(value) && value >= 0 ? value : fallback;
}

allocate();
rebuildSupport();

return {
    EMPTY: EMPTY,
    HUE_STEP: HUE_STEP,
    GRAPH_TIME_PER_SAMPLE: GRAPH_TIME_PER_SAMPLE,
    MUT_CONST: MUT_CONST,
    MUT_ALPHA: MUT_ALPHA,
    HUE_REDRAW: HUE_REDRAW,
    HUE_THERMO: HUE_THERMO,
    HUE_SPREAD: HUE_SPREAD,
    HUE_JITTER: HUE_JITTER,
    HEAT_X_REF: HEAT_X_REF,
    TII_TIE: TII_TIE,
    TII_BIAS: TII_BIAS,
    SUP_OFF: SUP_OFF,
    SUP_ON: SUP_ON,
    CHILD_RESET: CHILD_RESET,
    CHILD_EQUAL: CHILD_EQUAL,
    CHILD_AREA: CHILD_AREA,

    get GRID_N() { return GRID_N; },
    get CELLS_N() { return CELLS_N; },
    get pixels() { return pixels; },
    get cells() { return cells; },
    get species() { return speciesList; },
    // speciesList is now a recycled pool, so its length is the high-water mark
    // of concurrent species, not the number ever created. The tag counter is.
    get speciesEver() { return speciesTag; },
    get speciesPool() { return speciesList.length; },
    get aliveSpecies() { return aliveSpecies; },
    get subs() { return subs; },
    get aliveSubs() { return aliveSubs; },
    get occupiedN() { return occupiedN; },
    get emptyN() { return CELLS_N - occupiedN; },
    get simTime() { return simTime; },
    get totalEvents() { return totalEvents; },
    get expansions() { return expansions; },
    get contests() { return contests; },
    get innerContests() { return innerContests; },
    get mutations() { return mutations; },
    get bursts() { return bursts; },
    get subsEver() { return subsEver; },
    get burstTimes() { return burstTimes; },

    get mutMode() { return mutMode; },
    get childMode() { return childMode; },
    get typeIIMode() { return typeIIMode; },
    get supportMode() { return supportMode; },
    get hueMode() { return hueMode; },
    get dRaw() { return dRaw; },
    get dValue() { return expandProbability(); },
    get E() { return paramE; },
    get beta() { return paramBeta; },
    get m() { return paramM; },
    get delta() { return paramDelta; },
    get alpha0() { return alpha0; },
    get lambda() { return paramLambda; },
    get theta() { return paramTheta; },
    get dispersal() { return paramDispersal; },
    get settle() { return paramSettle; },
    get drift() { return paramDrift; },
    get wells() { return paramWells; },
    get spread() { return paramSpread; },
    get jitter() { return paramJitter; },

    setMutMode: function (mode) { mutMode = mode === MUT_CONST ? MUT_CONST : MUT_ALPHA; },
    setChildMode: function (mode) {
        childMode = mode === CHILD_EQUAL || mode === CHILD_AREA ? mode : CHILD_RESET;
    },
    setTypeIIMode: function (mode) { typeIIMode = mode === TII_BIAS ? TII_BIAS : TII_TIE; },
    setSupportMode: function (mode) { supportMode = mode === SUP_ON ? SUP_ON : SUP_OFF; },
    setHueMode: function (mode) {
        hueMode = mode === HUE_THERMO || mode === HUE_SPREAD || mode === HUE_JITTER
            ? mode
            : HUE_REDRAW;
    },
    setDispersal: function (value) { paramDispersal = clampPositive(value, paramDispersal); },
    setSettle: function (value) { paramSettle = clampPositive(value, paramSettle) || paramSettle; },
    setDrift: function (value) { paramDrift = clampPositive(value, paramDrift); },
    setSpread: function (value) { paramSpread = clampPositive(value, paramSpread); },
    setJitter: function (value) { paramJitter = clampPositive(value, paramJitter); },
    setWells: function (value) {
        const k = Math.round(clampPositive(value, paramWells));
        paramWells = k >= 2 ? k : 2;
    },
    setLambda: function (value) { paramLambda = clampPositive(value, paramLambda); },
    setTheta: function (value) {
        paramTheta = clampPositive(value, paramTheta);
        rebuildSupport();
    },
    setD: function (value) { dRaw = Math.min(1, Math.max(0, clampPositive(value, dRaw))); },
    setE: function (value) { paramE = clampPositive(value, paramE); },
    setBeta: function (value) { paramBeta = clampPositive(value, paramBeta); },
    setM: function (value) { paramM = clampPositive(value, paramM); },
    setDelta: function (value) { paramDelta = clampPositive(value, paramDelta); },
    setAlpha0: function (value) { alpha0 = clampPositive(value, alpha0); },

    srand: srand,
    reset: resetSimulation,
    step: step,
    setGridSize: setGridSize,
    xOf: xOf,
    expandProbability: expandProbability,
    circularMean: circularMean,
    hueDelta: hueDelta,
    sameNeighbours: sameNeighbours,
    repaintAll: repaintAll,
    snapshot: sampleState,
    drainGraphSamples: drainGraphSamples,
    _state: function () {
        return { cells: cells, occupied: occupied, occupiedN: occupiedN };
    }
};
})();

if (typeof module !== 'undefined' && module.exports) module.exports = Sim;
