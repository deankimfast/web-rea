#!/usr/bin/env python3
"""Validate frozen-inventory aggregate scores and render Markdown; no network I/O."""
import argparse
import json
import sys
from pathlib import Path

LABELS = ("correct", "partly_right", "wrong", "missed")


def count(value, field):
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")
    return value


def validate(data):
    if not isinstance(data, dict):
        raise ValueError("input must be an object")
    version = data.get("inventory_version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("inventory_version must be a nonempty string")
    if not isinstance(data.get("scope"), str) or not data["scope"].strip():
        raise ValueError("scope must be a nonempty string")
    areas = data.get("areas")
    if not isinstance(areas, dict) or not areas:
        raise ValueError("areas must be a nonempty map of fixed denominators")
    for area, size in areas.items():
        if not isinstance(area, str) or not area.strip():
            raise ValueError("area names must be nonempty strings")
        count(size, f"denominator for {area}")
    rounds = data.get("rounds")
    if not isinstance(rounds, list) or not rounds:
        raise ValueError("rounds must be a nonempty list")
    previous = 0
    for row in rounds:
        if not isinstance(row, dict):
            raise ValueError("each round must be an object")
        number = count(row.get("round"), "round")
        if number <= previous:
            raise ValueError("round numbers must be positive and strictly increasing")
        previous = number
        if row.get("inventory_version") != version:
            raise ValueError(f"round {number}: mixed inventory versions")
        groups = row.get("areas")
        if not isinstance(groups, dict) or set(groups) != set(areas):
            raise ValueError(f"round {number}: areas differ from frozen baseline")
        for area, size in areas.items():
            values = groups[area]
            if not isinstance(values, dict) or set(values) != set(LABELS):
                raise ValueError(f"round {number}/{area}: require exactly C/P/W/M fields")
            total = sum(count(values[key], f"{number}/{area}/{key}") for key in LABELS)
            if total != size:
                raise ValueError(f"round {number}/{area}: C+P+W+M={total}, expected {size}")
        count(row.get("unmapped_wrong_claims", 0), "unmapped_wrong_claims")
    return data


def percent(numerator, denominator):
    return f"{100 * numerator / denominator:.1f}%" if denominator else "N/A"


def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")


def render(data):
    validate(data)
    lines = [f"Inventory: {cell(data['inventory_version'])}; scope: {cell(data['scope'])}.",
             "", "Coverage is (C+P)/N; fully correct is C/N. Wrong remains in N.", "",
             "| Round | Area | Correct | Partly right | Wrong | Missed | N | Coverage | Fully correct |",
             "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for row in data["rounds"]:
        totals = {key: sum(group[key] for group in row["areas"].values()) for key in LABELS}
        entries = [(area, row["areas"][area]) for area in data["areas"]] + [("**Total**", totals)]
        for area, values in entries:
            c, p, w, m = (values[key] for key in LABELS)
            n = c + p + w + m
            fields = [row["round"], area, c, p, w, m, n, percent(c + p, n), percent(c, n)]
            lines.append("| " + " | ".join(map(cell, fields)) + " |")
    lines.extend(["", "Unmapped wrong claims (excluded from the fixed denominator):"])
    for row in data["rounds"]:
        lines.append(f"- Round {row['round']}: {row.get('unmapped_wrong_claims', 0)}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scores", type=Path, help="Aggregate JSON file; never a target URL")
    args = parser.parse_args()
    try:
        print(render(json.loads(args.scores.read_text(encoding="utf-8"))), end="")
    except (OSError, ValueError) as exc:
        print(f"Invalid scores: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
