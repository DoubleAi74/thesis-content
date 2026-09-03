#!/usr/bin/env python3
"""Simulate and draw a continuous-time two-type branching genealogy.

The event tree is exact for the stated birth--death--conversion process with a
global catastrophe hazard. At a birth, one child edge is the parent's
continuation and the other is the newborn lineage. A conversion is a unary
event that changes the edge colour. The catastrophe is a population-level event
of rate δ₁X_t + δ₂Y_t that simultaneously terminates every extant lineage.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.legend_handler import HandlerBase


TYPE_COLOURS = {1: "#0072B2", 2: "#D55E00"}
INK = "#1a1c1f"
SOFT_INK = "#565b62"
GRID = "#e3e6ea"
WHITE = "#ffffff"
CAT = "#9a2820"


@dataclass(frozen=True)
class Rates:
    lambda1: float = 1.0
    mu1: float = 0.55
    nu: float = 0.40
    lambda2: float = 0.90
    mu2: float = 0.50
    delta1: float = 0.05
    delta2: float = 0.08

    def personal(self, kind: int) -> float:
        if kind == 1:
            return self.lambda1 + self.mu1 + self.nu
        return self.lambda2 + self.mu2


@dataclass
class Segment:
    uid: int
    start: float
    end: float
    kind: int
    event: str
    depth: int
    children: list["Segment"] = field(default_factory=list)
    y: float = 0.0


@dataclass
class ActiveLineage:
    start: float
    kind: int
    depth: int
    attach: Callable[[Segment], None]


class SimulationLimit(RuntimeError):
    pass


class Simulator:
    """Population-level Gillespie simulation with optional global catastrophe."""

    def __init__(
        self,
        rates: Rates,
        horizon: float,
        seed: int,
        max_segments: int = 8000,
    ) -> None:
        self.rates = rates
        self.horizon = horizon
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        self.max_segments = max_segments
        self._uid = 0
        self.catastrophe_time: float | None = None

    def _new_uid(self) -> int:
        self._uid += 1
        if self._uid > self.max_segments:
            raise SimulationLimit(
                f"simulation exceeded {self.max_segments} segments; "
                "lower the horizon or choose another seed"
            )
        return self._uid

    def _choose_personal_event(self, kind: int) -> str:
        total = self.rates.personal(kind)
        u = float(self.rng.random()) * total
        if kind == 1:
            if u < self.rates.lambda1:
                return "birth"
            if u < self.rates.lambda1 + self.rates.mu1:
                return "death"
            return "conversion"
        return "birth" if u < self.rates.lambda2 else "death"

    def run(self) -> Segment:
        root_box: list[Segment] = []

        def attach_root(seg: Segment) -> None:
            root_box.append(seg)

        active: list[ActiveLineage] = [
            ActiveLineage(start=0.0, kind=1, depth=0, attach=attach_root)
        ]
        t = 0.0
        self.catastrophe_time = None

        while active:
            rates_personal = [self.rates.personal(a.kind) for a in active]
            r_ind = float(sum(rates_personal))
            n1 = sum(1 for a in active if a.kind == 1)
            n2 = len(active) - n1
            r_cat = self.rates.delta1 * n1 + self.rates.delta2 * n2
            r_tot = r_ind + r_cat
            if r_tot <= 0.0:
                break

            t += float(self.rng.exponential(1.0 / r_tot))
            if t >= self.horizon:
                for lin in active:
                    seg = Segment(
                        self._new_uid(), lin.start, self.horizon,
                        lin.kind, "horizon", lin.depth,
                    )
                    lin.attach(seg)
                active = []
                break

            u = float(self.rng.random()) * r_tot
            if u < r_cat:
                # Global catastrophe: every extant lineage ends at once.
                self.catastrophe_time = t
                for lin in active:
                    seg = Segment(
                        self._new_uid(), lin.start, t,
                        lin.kind, "catastrophe", lin.depth,
                    )
                    lin.attach(seg)
                active = []
                break

            # Choose the acting lineage, weighted by personal rates.
            u -= r_cat
            idx = 0
            for i, rate in enumerate(rates_personal):
                if u < rate:
                    idx = i
                    break
                u -= rate

            lin = active.pop(idx)
            event = self._choose_personal_event(lin.kind)
            seg = Segment(
                self._new_uid(), lin.start, t, lin.kind, event, lin.depth,
            )
            lin.attach(seg)

            if event == "birth":
                def make_attach(parent: Segment) -> Callable[[Segment], None]:
                    def _attach(child: Segment) -> None:
                        parent.children.append(child)
                    return _attach

                attach = make_attach(seg)
                active.append(
                    ActiveLineage(t, lin.kind, lin.depth + 1, attach)
                )
                active.append(
                    ActiveLineage(t, lin.kind, lin.depth + 1, attach)
                )
            elif event == "conversion":
                def make_attach(parent: Segment) -> Callable[[Segment], None]:
                    def _attach(child: Segment) -> None:
                        parent.children.append(child)
                    return _attach

                active.append(
                    ActiveLineage(t, 2, lin.depth + 1, make_attach(seg))
                )
            # death: terminal; nothing further to schedule

        if not root_box:
            raise RuntimeError("simulation produced no root segment")
        return root_box[0]


def walk(root: Segment) -> Iterable[Segment]:
    yield root
    for child in root.children:
        yield from walk(child)


def assign_layout(root: Segment) -> int:
    """Assign equal leaf spacing and centre internal branches on descendants."""

    next_leaf = 0

    def place(node: Segment) -> float:
        nonlocal next_leaf
        if not node.children:
            node.y = float(next_leaf)
            next_leaf += 1
            return node.y
        child_y = [place(child) for child in node.children]
        node.y = 0.5 * (min(child_y) + max(child_y))
        return node.y

    place(root)
    scale = max(next_leaf - 1, 1)
    for node in walk(root):
        node.y = 1.0 - 2.0 * node.y / scale
    return next_leaf


def summarise(root: Segment) -> dict[str, int | float]:
    nodes = list(walk(root))
    leaves = [n for n in nodes if not n.children]
    type1_length = sum(n.end - n.start for n in nodes if n.kind == 1)
    type2_length = sum(n.end - n.start for n in nodes if n.kind == 2)
    return {
        "segments": len(nodes),
        "leaves": len(leaves),
        "births": sum(n.event == "birth" for n in nodes),
        "deaths": sum(n.event == "death" for n in nodes),
        "conversions": sum(n.event == "conversion" for n in nodes),
        "alive_at_horizon": sum(n.event == "horizon" for n in nodes),
        "killed_by_catastrophe": sum(n.event == "catastrophe" for n in nodes),
        "type1_segments": sum(n.kind == 1 for n in nodes),
        "type2_segments": sum(n.kind == 2 for n in nodes),
        "type1_branch_length": round(type1_length, 6),
        "type2_branch_length": round(type2_length, 6),
        "max_depth": max(n.depth for n in nodes),
    }


def validate(root: Segment, horizon: float) -> None:
    """Check topology, chronology, and irreversible type conversion."""

    eps = 1e-10
    cat_times = {
        n.end for n in walk(root) if n.event == "catastrophe"
    }
    if len(cat_times) > 1:
        raise AssertionError("catastrophe times are not simultaneous")

    for node in walk(root):
        if not (node.start - eps <= node.end <= horizon + eps):
            raise AssertionError(f"invalid interval for segment {node.uid}")
        expected_children = {
            "birth": 2,
            "conversion": 1,
            "death": 0,
            "horizon": 0,
            "catastrophe": 0,
        }
        if len(node.children) != expected_children[node.event]:
            raise AssertionError(f"invalid child count for {node.event}")
        for child in node.children:
            if abs(child.start - node.end) > eps:
                raise AssertionError("child does not begin at parent event time")
            if node.event == "birth" and child.kind != node.kind:
                raise AssertionError("birth changed type")
            if node.event == "conversion" and not (node.kind == 1 and child.kind == 2):
                raise AssertionError("conversion is not type 1 -> type 2")
            if node.kind == 2 and child.kind == 1:
                raise AssertionError("type reversal detected")


class ConversionHandle:
    pass


class ConversionLegendHandler(HandlerBase):
    def create_artists(
        self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans
    ):
        x = xdescent + width / 2
        y = ydescent + height / 2
        blue = Line2D(
            [x], [y], marker="o", markersize=6.4, markerfacecolor=WHITE,
            markeredgecolor=TYPE_COLOURS[1], markeredgewidth=1.25,
            linestyle="none", transform=trans,
        )
        orange = Line2D(
            [x], [y], marker="o", markersize=3.2,
            markerfacecolor=TYPE_COLOURS[2], markeredgecolor=WHITE,
            markeredgewidth=0.45, linestyle="none", transform=trans,
        )
        return [blue, orange]


def draw_tree(
    root: Segment,
    horizon: float,
    output_base: Path,
    stats: dict,
    catastrophe_time: float | None,
) -> None:
    assign_layout(root)
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Latin Modern Roman", "Computer Modern Roman", "DejaVu Serif"],
            "mathtext.fontset": "cm",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )

    fig, ax = plt.subplots(figsize=(10.2, 6.8), facecolor=WHITE)
    ax.set_facecolor(WHITE)

    line_width = 1.45
    connector_width = 1.05

    cat_nodes = [n for n in walk(root) if n.event == "catastrophe"]
    # Crop the time axis just past the last event; with catastrophe, leave only
    # enough room on the right for the callout text.
    t_last = max(n.end for n in walk(root))
    if catastrophe_time is not None:
        x_right = catastrophe_time + 1.55
    else:
        x_right = min(horizon, t_last) + 0.22

    # Very light time guides retain chronological readability without axis clutter.
    tick_step = 1.0 if x_right <= 7.0 else 2.0
    ticks = np.arange(0.0, x_right + 0.001, tick_step)
    for tick in ticks[1:]:
        if tick < catastrophe_time if catastrophe_time is not None else tick < x_right - 0.05:
            ax.axvline(tick, color=GRID, lw=0.55, zorder=0, dashes=(1.2, 4.5))

    # Catastrophe wall: soft band + dashed vertical cut through all extant tips.
    if catastrophe_time is not None and cat_nodes:
        ys = [n.y for n in cat_nodes]
        y_lo, y_hi = min(ys) - 0.06, max(ys) + 0.06
        ax.axvspan(
            catastrophe_time - 0.035,
            catastrophe_time + 0.035,
            ymin=0.0,
            ymax=1.0,
            facecolor=CAT,
            alpha=0.05,
            zorder=0.5,
            clip_on=False,
        )
        ax.plot(
            [catastrophe_time, catastrophe_time],
            [y_lo, y_hi],
            color=CAT,
            lw=1.65,
            ls=(0, (5.0, 2.8)),
            alpha=0.90,
            solid_capstyle="round",
            zorder=3.5,
        )

    # Draw event connectors first so horizontal lineage segments remain crisp.
    for node in walk(root):
        if node.event == "birth":
            ys = [child.y for child in node.children]
            ax.plot(
                [node.end, node.end], [min(ys), max(ys)],
                color=TYPE_COLOURS[node.kind], lw=connector_width,
                alpha=0.82, solid_capstyle="round", zorder=1,
            )

    for node in walk(root):
        colour = TYPE_COLOURS[node.kind]
        ax.plot(
            [node.start, node.end], [node.y, node.y], color=colour,
            lw=line_width, solid_capstyle="round", zorder=2,
        )
        if node.event == "birth":
            ax.scatter(
                [node.end], [node.y], s=10.5, c=colour,
                edgecolors=WHITE, linewidths=0.45, zorder=4,
            )
        elif node.event == "conversion":
            ax.scatter(
                [node.end], [node.y], s=31, facecolors=WHITE,
                edgecolors=TYPE_COLOURS[1], linewidths=1.15, zorder=5,
            )
            ax.scatter(
                [node.end], [node.y], s=10, facecolors=TYPE_COLOURS[2],
                edgecolors=WHITE, linewidths=0.35, zorder=6,
            )
        elif node.event == "death":
            ax.scatter(
                [node.end], [node.y], s=13, marker="x", c=SOFT_INK,
                linewidths=0.85, zorder=5,
            )
        elif node.event == "horizon":
            ax.scatter(
                [node.end], [node.y], s=13, facecolors=WHITE,
                edgecolors=colour, linewidths=0.85, zorder=5,
            )
        elif node.event == "catastrophe":
            ax.scatter(
                [node.end], [node.y], s=18, facecolors=CAT,
                edgecolors=WHITE, linewidths=0.55, zorder=6,
            )

    ax.scatter(
        [0.0], [root.y], s=38, facecolors=TYPE_COLOURS[1],
        edgecolors=WHITE, linewidths=0.7, zorder=7,
    )

    ax.set_xlim(-0.12, x_right)
    ax.set_ylim(-1.12, 1.14)
    ax.set_yticks([])
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{int(t)}" for t in ticks], fontsize=9.0, color=SOFT_INK)
    ax.set_xlabel(r"time $t$", fontsize=11.5, color=INK, labelpad=8)
    ax.tick_params(axis="x", length=3.0, width=0.65, color="#aeb4ba", pad=4)
    for side in ("top", "left", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#bfc4c9")
    ax.spines["bottom"].set_linewidth(0.7)

    if catastrophe_time is not None and cat_nodes:
        n_kill = len(cat_nodes)
        n1 = sum(n.kind == 1 for n in cat_nodes)
        n2 = n_kill - n1
        label = (
            rf"catastrophe at $t\approx{catastrophe_time:.2f}$"
            "\n"
            rf"all {n_kill} extant lineages $\to(\mathrm{{R}},\mathrm{{R}})$"
            "\n"
            rf"({n1} type 1, {n2} type 2)"
        )
        # Callout on the right of the wall; x-axis pad is sized for this text only.
        ax.annotate(
            label,
            xy=(catastrophe_time, max(n.y for n in cat_nodes)),
            xytext=(catastrophe_time + 0.18, 0.72),
            textcoords="data",
            fontsize=8.8,
            color=CAT,
            ha="left",
            va="center",
            linespacing=1.3,
            arrowprops=dict(
                arrowstyle="-|>",
                color=CAT,
                lw=1.1,
                connectionstyle="arc3,rad=-0.12",
                shrinkA=0,
                shrinkB=4,
            ),
            zorder=10,
            clip_on=False,
        )

    type1_handle = Line2D([0], [0], color=TYPE_COLOURS[1], lw=2.2)
    type2_handle = Line2D([0], [0], color=TYPE_COLOURS[2], lw=2.2)
    death_handle = Line2D(
        [0], [0], marker="x", color=SOFT_INK, markersize=5.4,
        markeredgewidth=0.9, linestyle="none",
    )
    cat_handle = Line2D(
        [0], [0], marker="o", color=CAT, markersize=5.2,
        markerfacecolor=CAT, markeredgecolor=WHITE, markeredgewidth=0.6,
        linestyle="none",
    )
    horizon_handle = Line2D(
        [0], [0], marker="o", color=SOFT_INK, markersize=4.6,
        markerfacecolor=WHITE, markeredgewidth=0.9, linestyle="none",
    )
    if catastrophe_time is not None:
        handles = [
            type1_handle,
            type2_handle,
            ConversionHandle(),
            death_handle,
            cat_handle,
        ]
        labels = [
            "type 1",
            "type 2",
            "conversion",
            "ordinary death",
            "catastrophe",
        ]
    else:
        handles = [
            type1_handle,
            type2_handle,
            ConversionHandle(),
            death_handle,
            horizon_handle,
        ]
        labels = [
            "type 1",
            "type 2",
            "conversion",
            "ordinary death",
            r"alive at $T$",
        ]
    legend = ax.legend(
        handles,
        labels,
        handler_map={ConversionHandle: ConversionLegendHandler()},
        loc="lower center",
        bbox_to_anchor=(0.5, 1.01),
        ncol=5,
        frameon=False,
        handlelength=1.55,
        columnspacing=1.35,
        handletextpad=0.48,
        fontsize=9.0,
        borderaxespad=0.0,
    )
    for text_item in legend.get_texts():
        text_item.set_color(SOFT_INK)

    fig.subplots_adjust(left=0.035, right=0.985, bottom=0.10, top=0.93)
    output_base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(
        output_base.with_suffix(".png"), dpi=360, facecolor=WHITE,
        bbox_inches="tight", pad_inches=0.12,
    )
    fig.savefig(
        output_base.with_suffix(".pdf"), facecolor=WHITE,
        bbox_inches="tight", pad_inches=0.12,
    )
    plt.close(fig)


def simulate_one(
    seed: int, horizon: float, rates: Rates
) -> tuple[Segment, dict, float | None]:
    simulator = Simulator(rates=rates, horizon=horizon, seed=seed)
    root = simulator.run()
    validate(root, horizon)
    stats = summarise(root)
    stats.update({
        "seed": seed,
        "horizon": horizon,
        "catastrophe_time": (
            None if simulator.catastrophe_time is None
            else round(simulator.catastrophe_time, 6)
        ),
    })
    return root, stats, simulator.catastrophe_time


def scan_seeds(start: int, stop: int, horizon: float, rates: Rates) -> None:
    """Print compact candidate statistics for offline aesthetic selection."""

    rows = []
    for seed in range(start, stop + 1):
        try:
            _, stats, cat_t = simulate_one(seed, horizon, rates)
        except SimulationLimit:
            continue
        # Prefer a readable tree cut by catastrophe with both types at the wall.
        density = abs(stats["segments"] - 180) / 180
        conversion_penalty = 0 if 4 <= stats["conversions"] <= 40 else 1
        cat_count = stats["killed_by_catastrophe"]
        if cat_t is None or cat_count < 8:
            cat_penalty = 2.0
        elif cat_count > 80:
            cat_penalty = 0.8
        else:
            cat_penalty = 0.0
        # Prefer catastrophe mid-horizon so the cut is visually clear.
        if cat_t is None:
            time_penalty = 1.5
        else:
            time_penalty = abs(cat_t - 0.55 * horizon) / horizon
        type1_at_end = 0
        type2_at_end = 0
        # Approximate from segment counts is weak; use killed leaves if possible.
        # Re-simulate is expensive; use type2 segment share as proxy.
        type_balance = 0 if stats["type2_segments"] >= 10 else 1
        both_types_proxy = 0 if (
            stats["type1_segments"] >= 8 and stats["type2_segments"] >= 8
        ) else 0.8
        score = (
            density
            + conversion_penalty
            + cat_penalty
            + time_penalty
            + type_balance
            + both_types_proxy
        )
        rows.append((score, stats, cat_t))
    for score, stats, cat_t in sorted(rows, key=lambda item: item[0])[:20]:
        cat_s = "None" if cat_t is None else f"{cat_t:.3f}"
        print(
            f"score={score:.3f}  cat_t={cat_s}  "
            f"{json.dumps(stats, sort_keys=True)}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed", type=int, default=int(os.environ.get("SEED", "2869")),
        help="random seed (default: SEED environment variable or 2869)",
    )
    parser.add_argument("--horizon", type=float, default=9.0)
    parser.add_argument(
        "--delta1", type=float, default=None,
        help="catastrophe rate weight on type 1 (default: 0.05)",
    )
    parser.add_argument(
        "--delta2", type=float, default=None,
        help="catastrophe rate weight on type 2 (default: 0.08)",
    )
    parser.add_argument(
        "--no-catastrophe", action="store_true",
        help="set δ₁=δ₂=0 (pure genealogy to the horizon)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "fig03",
        help="output path without extension",
    )
    parser.add_argument(
        "--scan", nargs=2, type=int, metavar=("START", "STOP"),
        help="scan an inclusive seed range and print candidate statistics",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.no_catastrophe:
        rates = Rates(delta1=0.0, delta2=0.0)
    else:
        rates = Rates(
            delta1=0.05 if args.delta1 is None else args.delta1,
            delta2=0.08 if args.delta2 is None else args.delta2,
        )
    if args.scan:
        scan_seeds(args.scan[0], args.scan[1], args.horizon, rates)
        return

    root, stats, cat_t = simulate_one(args.seed, args.horizon, rates)
    draw_tree(root, args.horizon, args.output, stats, cat_t)
    metadata = {
        "figure": "fig03_genealogy_tree",
        "process": (
            "continuous-time two-type birth-death-conversion genealogy "
            "with global catastrophe"
        ),
        "parameters": rates.__dict__,
        "statistics": stats,
        "catastrophe_time": stats["catastrophe_time"],
        "software": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": mpl.__version__,
        },
        "validation": {
            "chronology_and_topology": "passed",
            "irreversible_conversion": "passed",
            "simultaneous_catastrophe": "passed",
            "leaf_identity": stats["leaves"] == stats["births"] + 1,
            "terminal_identity": stats["leaves"]
            == (
                stats["deaths"]
                + stats["alive_at_horizon"]
                + stats["killed_by_catastrophe"]
            ),
        },
    }
    metadata_path = args.output.parent / "meta.json"
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
