#!/usr/bin/env python3
"""Carte des lieux de tournage du Seigneur des Anneaux en Nouvelle-Zélande.

Produit 2-slides/assets/Carte_NZ_lieux_tournage.svg : trait de côte et ombrage du relief
issus de Natural Earth (domaine public), noms des lieux selon la traduction de Daniel Lauzon.

Données (à télécharger et dézipper dans un même dossier, passé en argument) :
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip
  https://naciscdn.org/naturalearth/10m/physical/ne_10m_minor_islands.zip
  https://naciscdn.org/naturalearth/10m/raster/SR_HR.zip

Dépendances : numpy, Pillow, pyshp (pip install pyshp).

Usage : python3 scripts/carte_nz.py <dossier_natural_earth> [sortie.svg]
"""
import base64
import io
import math
import os
import sys

import numpy as np
import shapefile  # pyshp
from PIL import Image, ImageDraw, ImageFilter

# --- Emprise et projection (équirectangulaire, corrigée à la latitude moyenne) ---
LON_MIN, LON_MAX = 165.8, 179.2
LAT_MIN, LAT_MAX = -47.5, -34.1
H = 1280                                   # unités SVG (affichage : 640 px de haut)
K = H / (LAT_MAX - LAT_MIN)                # unités par degré de latitude
COSL = math.cos(math.radians((LAT_MIN + LAT_MAX) / 2))
W = round((LON_MAX - LON_MIN) * COSL * K)


def proj(lon, lat):
    return ((lon - LON_MIN) * COSL * K, (LAT_MAX - lat) * K)


# --- Couleurs (palette du thème tolkien.css) ---
PARCHMENT = "#f4ecd8"
INK = "#2b2118"
INK_SOFT = "#5c4a3a"
GOLD = "#a67c2e"
SEA = "#d3dad3"
SEA_LINE = "#b4c0b9"
LAND_RGB = np.array([233, 220, 186], dtype=float)
FONT = "'EB Garamond 12', 'EB Garamond', Garamond, serif"

# --- Lieux : (nom Lauzon, lieu réel, lon, lat, position de l'étiquette lon/lat, ancrage) ---
LIEUX = [
    ("Hobbitebourg", "Matamata", 175.683, -37.872, 174.0, -36.9, "end"),
    ("Montagne du Destin", "Mont Ngauruhoe", 175.632, -39.157, 173.7, -38.2, "end"),
    ("Gouffre de Helm", "Carrière de Dry Creek", 174.97, -41.16, 173.6, -39.5, "end"),
    ("Fendeval", "Parc de Kaitoke", 175.18, -41.08, 175.2, -42.25, "start"),
    ("Sud de Fendeval", "Mont Olympus, Kahurangi", 172.60, -41.25, 171.8, -40.75, "end"),
    ("Vallée de|Ruisselombre", "Mont Owen, Kahurangi", 172.54, -41.55, 171.2, -41.95, "end"),
    ("Edoras", "Mount Sunday", 171.03, -43.58, 173.7, -43.85, "start"),
    ("Argonath", "Rivière Kawarau", 168.90, -45.01, 171.4, -45.55, "start"),
]


def read_parts(path):
    """Anneaux (listes de (lon, lat)) des polygones qui touchent l'emprise."""
    sf = shapefile.Reader(path)
    rings = []
    for shp in sf.shapes():
        x0, y0, x1, y1 = shp.bbox
        if x1 < LON_MIN or x0 > LON_MAX or y1 < LAT_MIN or y0 > LAT_MAX:
            continue
        idx = list(shp.parts) + [len(shp.points)]
        for a, b in zip(idx[:-1], idx[1:]):
            pts = shp.points[a:b]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            if max(xs) < LON_MIN or min(xs) > LON_MAX or max(ys) < LAT_MIN or min(ys) > LAT_MAX:
                continue
            rings.append(pts)
    return rings


def simplify(pts, tol):
    """Douglas-Peucker en unités SVG."""
    if len(pts) < 3:
        return pts
    a, b = np.array(pts[0]), np.array(pts[-1])
    arr = np.array(pts)
    d = b - a
    n = np.hypot(*d)
    if n == 0:
        dist = np.hypot(*(arr - a).T)
    else:
        dist = np.abs(d[0] * (arr[:, 1] - a[1]) - d[1] * (arr[:, 0] - a[0])) / n
    i = int(np.argmax(dist))
    if dist[i] > tol:
        return simplify(pts[: i + 1], tol)[:-1] + simplify(pts[i:], tol)
    return [pts[0], pts[-1]]


def main():
    data = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(__file__), "..", "2-slides", "assets", "Carte_NZ_lieux_tournage.svg")

    rings = read_parts(os.path.join(data, "ne_10m_land.shp"))
    rings += read_parts(os.path.join(data, "ne_10m_minor_islands.shp"))
    prings = [[proj(*p) for p in r] for r in rings]
    prings = [r for r in prings if len(r) > 3]

    # --- Masque des terres (suréchantillonné pour l'anticrénelage) ---
    SS = 2
    mask = Image.new("L", (W * SS, H * SS), 0)
    dr = ImageDraw.Draw(mask)
    for r in prings:
        dr.polygon([(x * SS, y * SS) for x, y in r], fill=255)
    mask = mask.resize((W, H), Image.LANCZOS)

    # --- Ombrage du relief (SR_HR, 1/60 de degré par pixel) ---
    Image.MAX_IMAGE_PIXELS = None
    sr = Image.open(os.path.join(data, "SR_HR.tif"))
    c0 = int((LON_MIN + 180) * 60)
    c1 = int(math.ceil((LON_MAX + 180) * 60))
    r0 = int((90 - LAT_MAX) * 60)
    r1 = int(math.ceil((90 - LAT_MIN) * 60))
    shade = sr.crop((c0, r0, c1, r1)).convert("L").resize((W, H), Image.BICUBIC)
    shade = shade.filter(ImageFilter.GaussianBlur(0.6))
    s = np.asarray(shade, dtype=float)
    m = np.asarray(mask, dtype=float) / 255
    ref = np.median(s[m > 0.9])
    rel = np.clip(s / ref, 0.45, 1.25)
    # Ombrage léger : on n'applique qu'une partie de l'écart à la valeur de plaine
    factor = 1 + 0.7 * (rel - 1)
    rgb = np.clip(LAND_RGB[None, None, :] * factor[:, :, None], 0, 255)
    rgba = np.dstack([rgb, m * 255]).astype(np.uint8)
    buf = io.BytesIO()
    Image.fromarray(rgba, "RGBA").save(buf, "PNG", optimize=True)
    relief = base64.b64encode(buf.getvalue()).decode()

    # --- Trait de côte simplifié ---
    paths = []
    for r in prings:
        sr_ = simplify(r, 0.8)
        if len(sr_) < 4:
            continue
        paths.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in sr_) + "Z")
    coast = " ".join(paths)

    # --- Étiquettes ---
    labels = []
    for nom, reel, lon, lat, llon, llat, anchor in LIEUX:
        px, py = proj(lon, lat)
        lx, ly = proj(llon, llat)
        # Un « | » dans le nom force un retour à la ligne
        lignes = nom.split("|")
        dy = 52 * (len(lignes) - 1)
        # Le trait de rappel aboutit au bord de la dernière ligne du nom, côté point
        tx = lx + 12 if anchor == "end" else lx - 12
        labels.append(
            f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{tx:.1f}" y2="{ly + dy - 14:.1f}" '
            f'stroke="{INK_SOFT}" stroke-width="2" stroke-dasharray="6 4"/>')
        for i, ligne in enumerate(lignes):
            labels.append(
                f'<text x="{lx:.1f}" y="{ly + 52 * i:.1f}" text-anchor="{anchor}" class="nom">{ligne}</text>')
        labels.append(
            f'<text x="{lx:.1f}" y="{ly + dy + 36:.1f}" text-anchor="{anchor}" class="reel">{reel}</text>')
    points = [
        f'<circle cx="{proj(lon, lat)[0]:.1f}" cy="{proj(lon, lat)[1]:.1f}" r="7" '
        f'fill="{GOLD}" stroke="{INK}" stroke-width="2.5"/>'
        for _, _, lon, lat, *_ in LIEUX]

    # --- Rose des vents simple ---
    cx, cy = proj(167.6, -35.3)
    rose = f'''<g transform="translate({cx:.1f},{cy:.1f})" stroke="{INK_SOFT}" stroke-width="2">
    <circle r="34" fill="none"/>
    <path d="M0,-58 L10,0 L0,58 L-10,0 Z" fill="{PARCHMENT}"/>
    <path d="M0,-58 L10,0 L-10,0 Z" fill="{GOLD}"/>
    <path d="M-58,0 L0,8 L58,0 L0,-8 Z" fill="{PARCHMENT}"/>
    <text y="-68" text-anchor="middle" class="rose" stroke="none">N</text>
  </g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W // 2}" height="{H // 2}" viewBox="0 0 {W} {H}">
  <!-- Généré par scripts/carte_nz.py. Données : Natural Earth (domaine public). -->
  <style>
    text {{ font-family: {FONT}; fill: {INK}; }}
    .nom {{ font-size: 52px; font-weight: 600; paint-order: stroke; stroke: {PARCHMENT}; stroke-width: 9px; stroke-linejoin: round; }}
    .reel {{ font-size: 33px; font-style: italic; fill: {INK_SOFT}; paint-order: stroke; stroke: {PARCHMENT}; stroke-width: 7px; stroke-linejoin: round; }}
    .rose {{ font-size: 34px; fill: {INK_SOFT}; }}
  </style>
  <clipPath id="cadre"><rect x="18" y="18" width="{W - 36}" height="{H - 36}"/></clipPath>
  <rect width="{W}" height="{H}" fill="{SEA}"/>
  <g clip-path="url(#cadre)">
  <g fill="none" stroke-linejoin="round">
    <path d="{coast}" stroke="{SEA_LINE}" stroke-width="26" opacity="0.35"/>
    <path d="{coast}" stroke="{SEA_LINE}" stroke-width="12" opacity="0.6"/>
  </g>
  <image width="{W}" height="{H}" xlink:href="data:image/png;base64,{relief}"/>
  <path d="{coast}" fill="none" stroke="{INK_SOFT}" stroke-width="2" stroke-linejoin="round"/>
  </g>
  {rose}
  {"".join(labels)}
  {"".join(points)}
  <rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{GOLD}" stroke-width="6"/>
  <rect x="18" y="18" width="{W - 36}" height="{H - 36}" fill="none" stroke="{GOLD}" stroke-width="1.5"/>
</svg>
'''
    with open(out, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{out} : {W // 2}x{H // 2} px, {len(svg) // 1024} Ko")


if __name__ == "__main__":
    main()
