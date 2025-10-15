#!/usr/bin/env python3
import sys, argparse
from xml.etree import ElementTree as ET

def main():
    p = argparse.ArgumentParser(description="Show uncovered files/lines from coverage.xml")
    p.add_argument("coverage_xml", nargs="?", default="coverage.xml")
    p.add_argument("--top", type=int, default=25, help="Show top N files by uncovered lines")
    args = p.parse_args()

    tree = ET.parse(args.coverage_xml)
    root = tree.getroot()
    # Coverage XML for coverage.py uses 'packages/package/classes/class/lines/line'
    data = []
    for cls in root.findall(".//class"):
        filename = cls.get("filename")
        missed = 0
        missed_lines = []
        for ln in cls.findall(".//line"):
            if ln.get("hits") == "0":
                missed += 1
                num = ln.get("number")
                if num: missed_lines.append(int(num))
        if missed:
            data.append((missed, filename, missed_lines))
    data.sort(reverse=True)
    print(f"Uncovered files (top {args.top}):")
    for i, (missed, fn, lines) in enumerate(data[:args.top], 1):
        chunks = summarize_lines(lines)
        print(f"{i:>2}. {fn}  — uncovered {missed} lines  — segments: {chunks}")

def summarize_lines(lines):
    if not lines: return "[]"
    lines = sorted(lines)
    segs = []
    start = prev = lines[0]
    for n in lines[1:]:
        if n == prev + 1:
            prev = n
            continue
        segs.append((start, prev))
        start = prev = n
    segs.append((start, prev))
    return ", ".join([f"{a}" if a==b else f"{a}-{b}" for a,b in segs])

if __name__ == "__main__":
    main()
