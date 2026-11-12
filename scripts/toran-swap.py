#!/usr/bin/env python3
"""Swap the hero mehrab-arch SVG for a toran (marigold + mango-leaf
doorway garland) with hanging jhalar strings.  All motifs are written
as literal inline SVG elements (no <use>, explicit classed fills).
Also fixes the U+2161 Roman-numeral tofu in chapter-num."""

import math
import re

ROOT = "/home/z/my-project/neelambari-invitation"
INDEX = ROOT + "/index.html"


def q_point(p0, c, p2, t):
    """Point on a quadratic bezier at parameter t."""
    x = (1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * c[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * c[1] + t ** 2 * p2[1]
    return x, y


def leaf(x, y, tilt, length=23, width=7.5):
    """A mango leaf hanging from (x, y), tilted by `tilt` degrees.
    Returns (body_path, vein_path) with literal coordinates."""
    a = math.radians(tilt)
    ca, sa = math.cos(a), math.sin(a)

    def pt(dx, dy):
        return (x + dx * ca - dy * sa, y + dx * sa + dy * ca)

    # tip and two side control pairs, rotated around the attach point
    tip = pt(0, length)
    c1 = pt(-width, length * 0.3)
    c2 = pt(-width * 0.85, length * 0.78)
    c3 = pt(width * 0.85, length * 0.78)
    c4 = pt(width, length * 0.3)
    body = (
        f'M{x:.1f} {y:.1f} '
        f'C {c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {tip[0]:.1f} {tip[1]:.1f} '
        f'C {c3[0]:.1f} {c3[1]:.1f} {c4[0]:.1f} {c4[1]:.1f} {x:.1f} {y:.1f} Z'
    )
    vein = f'M{x:.1f} {y + 2:.1f} L {tip[0]:.1f} {tip[1] - 1.5:.1f}'
    return body, vein


def bell(x, y, w=5.6, h=9.5):
    """A small temple bell centred on x, rim at y.  Returns paths."""
    dome = (
        f'M{x - w:.1f} {y:.1f} '
        f'C {x - w:.1f} {y - h * 1.15:.1f} {x + w:.1f} {y - h * 1.15:.1f} {x + w:.1f} {y:.1f} '
        f'L {x + w + 1.1:.1f} {y + 2.6:.1f} L {x - w - 1.1:.1f} {y + 2.6:.1f} Z'
    )
    loop_cy = y - h * 1.15 - 1.2
    return dome, loop_cy


def sprig(x, y, flip=1):
    """Two tiny leaves fanning out from (x, y)."""
    return (
        f'M{x:.1f} {y:.1f} C {x + flip * 4.4:.1f} {y + 1.2:.1f} {x + flip * 7.2:.1f} {y + 4.4:.1f} {x + flip * 8.4:.1f} {y + 8.6:.1f} '
        f'C {x + flip * 4.6:.1f} {y + 6.8:.1f} {x + flip * 1.6:.1f} {y + 3.6:.1f} {x:.1f} {y:.1f} Z'
    )


def build_toran():
    P0, C, P2 = (0, 16), (330, 42), (660, 16)
    parts = []

    # ── the two hanging ropes ────────────────────────────────────
    parts.append(
        f'<path class="ktor-rope" d="M{P0[0]} {P0[1]} Q{C[0]} {C[1]} {P2[0]} {P2[1]}"/>'
    )
    parts.append(
        f'<path class="ktor-rope ktor-rope--soft" d="M{P0[0]} {P0[1] + 4.5} Q{C[0]} {C[1] + 4.5} {P2[0]} {P2[1] + 4.5}"/>'
    )

    # ── beads strung along the upper rope ───────────────────────
    for i in range(23):
        t = 0.03 + i * (0.94 / 22)
        bx, by = q_point(P0, C, P2, t)
        r = 2.1 if i % 2 == 0 else 1.4
        cls = "ktor-bead" if i % 3 else "ktor-bead ktor-bead--jewel"
        parts.append(f'<circle class="{cls}" cx="{bx:.1f}" cy="{by - 2.6:.1f}" r="{r}"/>')

    # ── mango-leaf fringe ───────────────────────────────────────
    leaf_xs = [46 + i * ((614 - 46) / 13) for i in range(14)]
    for i, lx in enumerate(leaf_xs):
        ly = q_point(P0, C, P2, lx / 660)[1] + 1.5
        tilt = 9 if i % 2 == 0 else -9
        body, vein = leaf(lx, ly, tilt, length=30 if i % 2 == 0 else 25, width=9)
        cls = "ktor-leaf" if i % 2 == 0 else "ktor-leaf--deep"
        parts.append(f'<path class="{cls}" d="{body}"/>')
        parts.append(f'<path class="ktor-vein" d="{vein}"/>')

    # ── the marigold garland ────────────────────────────────────
    for i in range(10):
        mx = 70 + i * ((590 - 70) / 9)
        my = q_point(P0, C, P2, mx / 660)[1] + 15
        rb, rt, rc = (10.6, 8.1, 4.6) if i % 2 == 0 else (8.6, 6.5, 3.7)
        parts.append(f'<path class="ktor-leaf--deep" d="{sprig(mx - rb - 2, my + 4.5, -1)}"/>')
        parts.append(f'<path class="ktor-leaf--deep" d="{sprig(mx + rb + 2, my + 4.5, 1)}"/>')
        parts.append(f'<circle class="ktor-mari--base" cx="{mx:.1f}" cy="{my:.1f}" r="{rb}"/>')
        parts.append(f'<circle class="ktor-mari" cx="{mx:.1f}" cy="{my - rt * .45:.1f}" r="{rt}"/>')
        parts.append(f'<circle class="ktor-mari--core" cx="{mx:.1f}" cy="{my - rt * .78:.1f}" r="{rc}"/>')

    # ── hanging tassels between the blooms ──────────────────────
    tassel_specs = [(128, 40, "diamond"), (240, 58, "bell"), (330, 48, "diamond"),
                    (420, 58, "bell"), (532, 40, "diamond")]
    for tx, length, kind in tassel_specs:
        ty = q_point(P0, C, P2, tx / 660)[1]
        parts.append(f'<path class="ktor-tassel" d="M{tx} {ty:.1f} L {tx} {ty + length:.1f}"/>')
        parts.append(f'<circle class="ktor-bead ktor-bead--jewel" cx="{tx}" cy="{ty + length * .55:.1f}" r="1.8"/>')
        end_y = ty + length
        if kind == "diamond":
            parts.append(
                f'<path class="ktor-diamond" d="M{tx} {end_y - 4.4:.1f} L {tx + 3.6} {end_y:.1f} '
                f'L {tx} {end_y + 4.4:.1f} L {tx - 3.6} {end_y:.1f} Z"/>'
            )
        else:
            dome, loop_cy = bell(tx, end_y, w=6.4, h=11)
            parts.append(f'<path class="ktor-bell" d="{dome}"/>')
            parts.append(f'<circle class="ktor-rope" cx="{tx}" cy="{loop_cy:.1f}" r="1.8"/>')
            parts.append(f'<circle class="ktor-bell-clap" cx="{tx}" cy="{end_y + 5:.1f}" r="1.4"/>')

    # ── the two jhalar strings flanking the crown ───────────────
    for jx in (38, 622):
        top_y, end_y = 26, 330
        parts.append(f'<path class="ktor-jline" d="M{jx} {top_y} L {jx} {end_y}"/>')
        y = top_y + 16
        i = 0
        while y < end_y - 14:
            if i % 2 == 0:  # jasmine bud
                parts.append(f'<circle class="ktor-jbud" cx="{jx}" cy="{y:.1f}" r="3"/>')
                parts.append(f'<circle class="ktor-jbud-core" cx="{jx}" cy="{y - 0.5:.1f}" r="1.2"/>')
            else:           # sapphire jewel
                parts.append(f'<circle class="ktor-jewel" cx="{jx}" cy="{y:.1f}" r="2.3"/>')
            y += 16.5
            i += 1
        dome, loop_cy = bell(jx, end_y + 10, w=6.8, h=11.5)
        parts.append(f'<path class="ktor-leaf--deep" d="{sprig(jx - 6, end_y - 2, -1)}"/>')
        parts.append(f'<path class="ktor-leaf--deep" d="{sprig(jx + 6, end_y - 2, 1)}"/>')
        parts.append(f'<path class="ktor-bell" d="{dome}"/>')
        parts.append(f'<circle class="ktor-rope" cx="{jx}" cy="{loop_cy:.1f}" r="1.9"/>')
        parts.append(f'<circle class="ktor-bell-clap" cx="{jx}" cy="{end_y + 17.6:.1f}" r="1.5"/>')

    return (
        '<svg class="kcard__toran" viewBox="0 0 660 360" preserveAspectRatio="xMidYMin meet" '
        'aria-hidden="true" focusable="false">\n              '
        + "\n              ".join(parts)
        + "\n            </svg>"
    )


def main():
    with open(INDEX, "r", encoding="utf-8") as fh:
        html = fh.read()

    # 1 ─ replace the arch svg block with the toran (idempotent:
    #     on later runs the existing toran block is swapped in place)
    arch_pattern = re.compile(
        r'<!-- the mehrab: the card is die-cut like the reference —\n'
        r'(.*?\n)*?\s*<svg class="kcard__arch".*?</svg>', re.DOTALL)
    toran_pattern = re.compile(
        r'<!-- the toran: a marigold-and-mango-leaf doorway garland\n'
        r'(.*?\n)*?\s*<svg class="kcard__toran".*?</svg>', re.DOTALL)
    comment = (
        "<!-- the toran: a marigold-and-mango-leaf doorway garland\n"
        "                 strung across the card, with jhalar strings of\n"
        "                 jasmine and sapphire beads hanging at the sides —\n"
        "                 the welcome every Indian door wears -->"
    )
    new_html, n = arch_pattern.subn(comment + "\n            " + build_toran(), html)
    if n != 1:
        new_html, n = toran_pattern.subn(comment + "\n            " + build_toran(), html)
    assert n == 1, f"toran/arch block matched {n} times"

    # 2 ─ Roman numeral tofu -> ASCII (first run only)
    new_html = new_html.replace("\u2161", "II")

    with open(INDEX, "w", encoding="utf-8") as fh:
        fh.write(new_html)
    print("toran swapped in, numeral fixed")


if __name__ == "__main__":
    main()
