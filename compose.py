"""Draw a one-page front-page infographic of Thursday 26 November 2026 world news.

Build-time only: reads the story lists defined below and writes entry.png
(1024 x 1024) next to this script. No network, no randomness, no clock, so
every run produces the same bytes. Uses Pillow locally; the graded program
(main.ts) only copies the finished PNG, so the grader needs no Pillow.
"""

import json
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

CREAM = (247, 243, 233)
PAPER = (255, 253, 247)
NAVY = (11, 31, 58)
NAVY_LIGHT = (23, 52, 88)
INK = (18, 18, 18)
MUTED = (96, 94, 88)
LINE = (198, 192, 178)
RED = (176, 42, 42)
GOLD = (184, 138, 30)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSerif-Bold.ttf", 56)
F_DATE = font("DejaVuSans-Bold.ttf", 19)
F_STRAP = font("DejaVuSans.ttf", 12)
F_CHECK = font("DejaVuSans-Bold.ttf", 12)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 15)
F_LEAD_BODY = font("DejaVuSans.ttf", 11)
F_SEC = font("DejaVuSans-Bold.ttf", 13)
F_HEAD = font("DejaVuSans-Bold.ttf", 11)
F_BODY = font("DejaVuSans.ttf", 10)
F_TIME = font("DejaVuSans-Bold.ttf", 11)
F_TBODY = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 10)
F_FOOTB = font("DejaVuSans-Bold.ttf", 10)
F_NUM = font("DejaVuSans-Bold.ttf", 11)
F_LEG = font("DejaVuSans.ttf", 8)
F_MAPNUM = font("DejaVuSans-Bold.ttf", 8)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- stories
# (region, headline, one-line summary, lon, lat) — lon/lat None = no map dot.
# Regions: NA North America, LAT Latin America, EUR Europe, ME Middle East,
# AFR Africa, SA South Asia, EA East Asia, OCE Oceania, SCI Space & Science.
STORIES = [
    ("NA", "US proposes tariffs on 14 partners",
     "China, the EU, Japan and India face new country tariffs; India 25%, Japan 15%.",
     -77.0, 38.9),
    ("NA", "Macy's 100th parade postponed by storm",
     "First weather delay in a century; New York parade moves to Saturday, 8:30 a.m.",
     -74.0, 40.7),
    ("ME", "Cairo tanker fire kills at least 31",
     "Fuel tanker overturns and bursts into flames on the ring road; about 21 hurt.",
     31.2, 30.0),
    ("ME", "Houthis hit Saudi ports and oil refinery",
     "Strikes on Ras Tanura and Riyadh; 11 hurt at a tower; oil rises over 2%.",
     50.0, 26.6),
    ("NA", "Nasdaq nears bear market in AI sell-off",
     "Tech shares slide again; S&P 500 down 0.25%; Nvidia rating in question.",
     -74.0, 40.7),
    ("EUR", "Ukraine hits 5 jets at Russian airbase",
     "Savasleyka airfield struck; Russia hits Kyiv with ballistic missiles.",
     30.5, 50.4),
    ("ME", "US tells citizens to leave Iran",
     "Washington warns hostilities could escalate fast as Gulf war fears grow.",
     51.4, 35.7),
    ("EA", "First Pakistani astronaut reaches Tiangong",
     "Muhammad Zeeshan Ali boards China's station aboard Shenzhou-24.",
     100.3, 40.9),
    ("ME", "Judges urge dropping Netanyahu bribery case",
     "Israeli court sees little chance of conviction in the most serious charge.",
     35.2, 31.8),
    ("ME", "Gaza strike kills Hamas security chief",
     "Mohammed Abu al-Ouf killed with his wife and two daughters, doctors say.",
     34.5, 31.5),
    ("NA", "Jensen Huang returns as Nvidia CEO",
     "Back after resigning over reported affairs; lawmakers demand answers.",
     -122.0, 37.35),
    ("NA", "FCC approves SpaceX's 1m satellites",
     "Plan for up to a million satellites for orbital data centres clears the FCC.",
     -118.3, 33.9),
    ("EA", "China investigates Shanghai party chief",
     "Chen Jining, a Politburo member, probed for serious discipline violations.",
     121.5, 31.2),
    ("EUR", "Leaked data: Russia lost ~490,000 troops",
     "BBC analysis of leaked figures; another count puts the toll above 700,000.",
     37.6, 55.75),
    ("NA", "King tides and storms flood California",
     "Record tides driven by El Nino swamp roads and businesses on the coast.",
     -122.5, 37.8),
    ("EUR", "Spain votes Sunday with right favoured",
     "Snap election: Feijoo's Popular Party leads polls; may need Vox to govern.",
     -3.7, 40.4),
    ("EUR", "EU leaders meet over 2 trillion euro budget",
     "Special Brussels summit on the bloc's next long-term budget; deal far off.",
     4.35, 50.85),
    ("EA", "Bank of Korea raises rate to 3.25%",
     "First rise in two years; 2027 growth forecast lifted to 4.1%.",
     127.0, 37.5),
    ("EUR", "UK energy bills to rise 26% in January",
     "Ofgem lifts the price cap; a typical bill rises to 2,166 pounds a year.",
     -0.12, 51.5),
    ("NA", "Huawei guilty of stealing US trade secrets",
     "New York jury convicts on 10 of 12 counts, including bank fraud.",
     -73.95, 40.65),
    ("EA", "Kim Jong Un vows more nuclear weapons",
     "North Korea's leader tours nuclear plants and ignores Trump's overture.",
     125.75, 39.0),
    ("AFR", "Drone strikes kill 15 in Sudan's Blue Nile",
     "Ed Damazin and El Roseires hit; Sudan rejects Ethiopia's offer to host talks.",
     34.4, 11.8),
    ("EA", "Hong Kong marks year since fire killed 168",
     "Families of Wang Fuk Court victims still await full answers, a year on.",
     114.2, 22.3),
    ("SA", "India marks 18 years since 26/11 attacks",
     "Mumbai remembers 166 killed in 2008; leaders pledge zero tolerance on terror.",
     72.9, 19.1),
    ("EUR", "Gukesh-Sindarov: Game 3 in Geneva, 1-1",
     "World chess title match level after two draws; Sindarov has White in Game 3.",
     6.14, 46.2),
    ("SCI", "Hera images show Dimorphos crater",
     "ESA releases pictures of the stadium-sized crater left by NASA's DART impact.",
     None, None),
    ("NA", "Pig-kidney patient a year off dialysis",
     "Molly Falco passes a year after a gene-edited pig kidney transplant.",
     -71.0, 42.35),
    ("OCE", "Australia-Solomon Islands security treaty",
     "No foreign military base on the islands; Canberra becomes primary partner.",
     160.0, -9.4),
    ("LAT", "Colombia police free 76 supermarket hostages",
     "Cartagena siege ends after 17 hours; one gunman killed, four arrested.",
     -75.5, 10.4),
    ("AFR", "UK sends convicted refugees to Eswatini",
     "First known permanent forced resettlement abroad; a Sri Lankan man dies.",
     31.4, -26.5),
    ("SA", "Bangladesh garment wage rises after unrest",
     "Minimum pay up to 17,000 taka; at least 140 factories closed amid protests.",
     90.4, 23.8),
    ("EUR", "US-backed deal for Lukoil's overseas assets",
     "Consortium to buy the sanctioned oil firm's international business.",
     37.6, 55.75),
    ("EUR", "1,990 migrants reach Canary Islands in a day",
     "Fifteen boats arrive, most from Senegal and Gambia, rescue service says.",
     -16.0, 28.3),
    ("AFR", "UN warns aid cuts may raise HIV infections",
     "UNAIDS expects new infections to rise in 2027 for the first time in years.",
     6.14, 46.2),
    ("EUR", "Abrego Garcia leaves US for Spain",
     "Wrongly deported in 2025, he arrives in Spain after a 20-month legal fight.",
     -3.7, 40.4),
    ("EUR", "Poundland collapses; 11,000 jobs at risk",
     "UK discount chain enters administration after owners fail to find a buyer.",
     -0.12, 51.5),
]

REGION_COLORS = {
    "NA": (176, 42, 42), "LAT": (217, 123, 41), "EUR": (42, 93, 176),
    "ME": (122, 63, 160), "AFR": (42, 138, 74), "SA": (194, 24, 122),
    "EA": (15, 123, 125), "OCE": (107, 124, 0), "SCI": (85, 85, 85),
}
REGION_NAMES = {
    "NA": "N. America", "LAT": "Latin Am.", "EUR": "Europe",
    "ME": "Middle East", "AFR": "Africa", "SA": "S. Asia",
    "EA": "E. Asia", "OCE": "Oceania", "SCI": "Space/Sci",
}

TIMELINE = [
    ("00:30", "Macy's confirms 100th parade moves to Saturday (storm)"),
    ("01:00", "Bank of Korea lifts its rate to 3.25%"),
    ("05:25", "India marks 18 years since 26/11; Mumbai on alert"),
    ("09:00", "EU leaders open budget summit in Brussels"),
    ("13:00", "Houthi strikes hit Saudi ports; oil jumps 2%"),
    ("14:00", "Gukesh-Sindarov Game 3 begins in Geneva"),
    ("16:00", "US publishes tariff plan for 14 partners"),
    ("21:00", "Nasdaq closes near bear market after AI sell-off"),
]

IN_BRIEF = ("IN BRIEF: Liverpool 3-0 Club Brugge  ·  Miss Universe: Jennifer Barreto "
            "(Puerto Rico)  ·  Duran Duran guitarist Andy Taylor dies at 65  ·  Nepal "
            "declares 213 Indians missing presumed dead  ·  Greek workers strike  ·  "
            "CAS gives Africa Cup title back to Senegal  ·  Indonesia mine flood kills 13")


# ---------------------------------------------------------------- scenes
def draw_balloon_scene(d, x0, y0, w, h):
    """Macy's balloon in a storm: grey sky, rain, tilted balloon."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(58, 74, 96))
    d.ellipse([x0 + 8, y0 + 4, x0 + 90, y0 + 26], fill=(38, 50, 68))
    d.ellipse([x0 + 150, y0 + 10, x0 + 250, y0 + 30], fill=(38, 50, 68))
    for i in range(14):  # rain slashes
        rx = x0 + 12 + i * 23
        d.line([rx, y0 + 34, rx - 8, y0 + 62], fill=(150, 170, 200), width=2)
    # balloon: red with gold stripes, tilted by the wind
    d.ellipse([x0 + 105, y0 + 8, x0 + 205, y0 + 78], fill=(176, 42, 42))
    d.ellipse([x0 + 130, y0 + 8, x0 + 180, y0 + 78], fill=(212, 175, 55))
    d.ellipse([x0 + 145, y0 + 8, x0 + 165, y0 + 78], fill=(176, 42, 42))
    d.polygon([(x0 + 150, y0 + 78), (x0 + 160, y0 + 78), (x0 + 155, y0 + 92)],
              fill=(120, 30, 30))
    d.line([x0 + 148, y0 + 92, x0 + 148, y0 + 100], fill=(60, 40, 20), width=2)
    d.line([x0 + 162, y0 + 92, x0 + 162, y0 + 100], fill=(60, 40, 20), width=2)
    d.rectangle([x0 + 142, y0 + 100, x0 + 168, y0 + 110], fill=(90, 60, 30))
    # wind streaks
    for yy in (y0 + 40, y0 + 58, y0 + 76):
        d.line([x0 + 215, yy, x0 + 285, yy - 6], fill=(200, 210, 225), width=2)
        d.line([x0 + 225, yy + 8, x0 + 275, yy + 2], fill=(200, 210, 225), width=2)
    # rooftops at the bottom
    d.rectangle([x0, y0 + h - 16, x0 + w, y0 + h], fill=(30, 38, 52))
    d.rectangle([x0 + 20, y0 + h - 34, x0 + 60, y0 + h - 16], fill=(44, 54, 72))
    d.rectangle([x0 + 250, y0 + h - 28, x0 + 300, y0 + h - 16], fill=(44, 54, 72))


def draw_fire_scene(d, x0, y0, w, h):
    """Cairo ring-road tanker fire: flames over a tanker truck."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(40, 32, 28))
    d.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=(24, 20, 18))
    # smoke
    for cx, cy, r in ((x0 + 90, y0 + 22, 16), (x0 + 130, y0 + 12, 20),
                      (x0 + 175, y0 + 20, 15), (x0 + 215, y0 + 10, 18)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 85, 80))
    # flames
    d.polygon([(x0 + 70, y0 + 78), (x0 + 95, y0 + 18), (x0 + 115, y0 + 55),
               (x0 + 140, y0 + 8), (x0 + 165, y0 + 52), (x0 + 190, y0 + 22),
               (x0 + 215, y0 + 78)], fill=(230, 110, 20))
    d.polygon([(x0 + 100, y0 + 78), (x0 + 120, y0 + 38), (x0 + 140, y0 + 62),
               (x0 + 160, y0 + 34), (x0 + 180, y0 + 78)], fill=(245, 200, 40))
    # tanker truck
    d.rectangle([x0 + 60, y0 + 78, x0 + 230, y0 + 100], fill=(120, 125, 130))
    d.ellipse([x0 + 60, y0 + 78, x0 + 230, y0 + 92], fill=(150, 155, 160))
    d.rectangle([x0 + 230, y0 + 84, x0 + 262, y0 + 100], fill=(176, 42, 42))
    d.ellipse([x0 + 82, y0 + 98, x0 + 102, y0 + 112], fill=(10, 10, 10))
    d.ellipse([x0 + 190, y0 + 98, x0 + 210, y0 + 112], fill=(10, 10, 10))
    d.ellipse([x0 + 238, y0 + 98, x0 + 256, y0 + 112], fill=(10, 10, 10))


def draw_rocket_scene(d, x0, y0, w, h):
    """Shenzhou-24 / Tiangong: rocket rising past a space station."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(10, 16, 34))
    for sx, sy in ((x0 + 20, y0 + 14), (x0 + 60, y0 + 30), (x0 + 250, y0 + 18),
                   (x0 + 290, y0 + 44), (x0 + 40, y0 + 70), (x0 + 270, y0 + 84),
                   (x0 + 200, y0 + 8), (x0 + 120, y0 + 52)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    # station: two modules + solar panels
    d.rectangle([x0 + 205, y0 + 26, x0 + 235, y0 + 44], fill=(200, 205, 210))
    d.rectangle([x0 + 235, y0 + 30, x0 + 262, y0 + 40], fill=(160, 165, 175))
    d.rectangle([x0 + 180, y0 + 30, x0 + 205, y0 + 40], fill=(40, 90, 180))
    d.rectangle([x0 + 262, y0 + 30, x0 + 290, y0 + 40], fill=(40, 90, 180))
    d.ellipse([x0 + 212, y0 + 30, x0 + 222, y0 + 40], fill=(120, 125, 135))
    # rocket
    d.polygon([(x0 + 95, y0 + 6), (x0 + 115, y0 + 6), (x0 + 105, y0 - 8)],
              fill=(176, 42, 42))
    d.rectangle([x0 + 95, y0 + 6, x0 + 115, y0 + 66], fill=(235, 238, 240))
    d.rectangle([x0 + 95, y0 + 30, x0 + 115, y0 + 42], fill=(176, 42, 42))
    d.polygon([(x0 + 95, y0 + 66), (x0 + 85, y0 + 82), (x0 + 95, y0 + 78)],
              fill=(212, 175, 55))
    d.polygon([(x0 + 115, y0 + 66), (x0 + 125, y0 + 82), (x0 + 115, y0 + 78)],
              fill=(212, 175, 55))
    d.polygon([(x0 + 99, y0 + 66), (x0 + 111, y0 + 66), (x0 + 105, y0 + 80)],
              fill=(245, 160, 40))
    d.polygon([(x0 + 102, y0 + 66), (x0 + 108, y0 + 66), (x0 + 105, y0 + 76)],
              fill=(255, 220, 90))
    # earth curve at the bottom
    d.ellipse([x0 - 60, y0 + h - 8, x0 + w + 60, y0 + h + 60], fill=(42, 93, 176))
    d.ellipse([x0 + 30, y0 + h - 2, x0 + 120, y0 + h + 26], fill=(42, 138, 74))


def draw_map_icon(d, kind, cx, cy):
    """Tiny scene icon drawn on the map at (cx, cy)."""
    if kind == "balloon":
        d.ellipse([cx - 6, cy - 8, cx + 6, cy + 4], fill=(176, 42, 42))
        d.line([cx - 2, cy + 4, cx - 2, cy + 8], fill=(60, 40, 20), width=1)
        d.line([cx + 2, cy + 4, cx + 2, cy + 8], fill=(60, 40, 20), width=1)
        d.rectangle([cx - 3, cy + 8, cx + 3, cy + 11], fill=(90, 60, 30))
    elif kind == "flame":
        d.polygon([(cx - 6, cy + 7), (cx - 3, cy - 4), (cx, cy + 2),
                   (cx + 3, cy - 7), (cx + 6, cy + 7)], fill=(230, 110, 20))
        d.polygon([(cx - 3, cy + 7), (cx, cy - 1), (cx + 3, cy + 7)],
                  fill=(245, 200, 40))
    elif kind == "chess":
        d.rectangle([cx - 10, cy - 10, cx + 9, cy + 9], fill=(255, 255, 255),
                    outline=(18, 18, 18), width=1)
        for r in range(3):
            for c in range(3):
                if (r + c) % 2 == 0:
                    d.rectangle([cx - 8 + c * 5, cy - 8 + r * 5,
                                 cx - 4 + c * 5, cy - 4 + r * 5], fill=(18, 18, 18))
    elif kind == "rocket":
        d.rectangle([cx - 3, cy - 8, cx + 3, cy + 4], fill=(235, 238, 240))
        d.polygon([(cx - 3, cy - 8), (cx + 3, cy - 8), (cx, cy - 12)],
                  fill=(176, 42, 42))
        d.polygon([(cx - 2, cy + 4), (cx + 2, cy + 4), (cx, cy + 10)],
                  fill=(245, 160, 40))
    elif kind == "satellite":
        d.rectangle([cx - 8, cy - 2, cx - 3, cy + 2], fill=(40, 90, 180))
        d.rectangle([cx + 3, cy - 2, cx + 8, cy + 2], fill=(40, 90, 180))
        d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=(200, 205, 210))
        d.line([cx - 6, cy - 6, cx + 6, cy + 6], fill=(212, 175, 55), width=1)


# ---------------------------------------------------------------- map
def draw_map(d, x0, y0, w, h):
    """Simplified world map from the countries GeoJSON in /tmp."""
    geo_path = "/tmp/world.geo.json"
    land = (232, 222, 196)
    edge = (190, 180, 150)
    try:
        with open(geo_path, encoding="utf-8") as fh:
            geo = json.load(fh)
    except OSError:
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=land)
        geo = None
    if geo is not None:
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(238, 240, 242))
        lat_top, lat_bot = 84.0, -58.0

        def proj(lon, lat):
            px = x0 + (lon + 180.0) / 360.0 * w
            py = y0 + (lat_top - lat) / (lat_top - lat_bot) * h
            return px, py

        for feat in geo["features"]:
            g = feat["geometry"]
            if g is None:
                continue
            polys = []
            if g["type"] == "Polygon":
                polys = [g["coordinates"]]
            elif g["type"] == "MultiPolygon":
                polys = g["coordinates"]
            for poly in polys:
                for ring in poly:
                    pts = [proj(lon, lat) for lon, lat in ring]
                    if len(pts) >= 3:
                        d.polygon(pts, fill=land, outline=edge)
        # graticule
        for lon in (-120, -60, 0, 60, 120):
            gx = x0 + (lon + 180.0) / 360.0 * w
            d.line([gx, y0, gx, y0 + h], fill=(214, 216, 218), width=1)
        # story dots, coloured by region
        for region, _head, _body, lon, lat in STORIES:
            if lon is None:
                continue
            px, py = proj(lon, lat)
            col = REGION_COLORS[region]
            d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col,
                      outline=(255, 255, 255), width=1)
        # numbered badges for the three lead stories (offset so the
        # close Washington / New York pair does not collide)
        for num, (lon, lat, ox, oy) in ((1, (-77.0, 38.9, -16, 12)),
                                        (2, (-74.0, 40.7, 2, -14)),
                                        (3, (31.2, 30.0, -2, -14))):
            px, py = proj(lon, lat)
            px, py = px + ox, py + oy
            d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=NAVY,
                      outline=(255, 255, 255), width=1)
            t = str(num)
            tw = d.textlength(t, font=F_MAPNUM)
            d.text((px - tw / 2, py - 5), t, font=F_MAPNUM, fill=(255, 255, 255))
        # tiny scene icons on the map
        px, py = proj(-74.0, 40.7)
        draw_map_icon(d, "balloon", px + 16, py - 14)
        px, py = proj(31.2, 30.0)
        draw_map_icon(d, "flame", px + 15, py - 13)
        px, py = proj(50.0, 26.6)
        draw_map_icon(d, "flame", px + 14, py + 12)
        px, py = proj(6.14, 46.2)
        draw_map_icon(d, "chess", px - 16, py - 12)
        px, py = proj(100.3, 40.9)
        draw_map_icon(d, "rocket", px + 15, py - 12)
        px, py = proj(-118.3, 33.9)
        draw_map_icon(d, "satellite", px - 14, py + 12)
    return


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # outer frame
    d.rectangle([4, 4, W - 5, H - 5], outline=INK, width=2)

    # ---- masthead
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=F_MAST)
    d.text(((W - tw) / 2, 12), title, font=F_MAST, fill=NAVY)
    d.line([24, 84, W - 24, 84], fill=INK, width=2)
    date_line = "THURSDAY 26 NOVEMBER 2026"
    dw = d.textlength(date_line, font=F_DATE)
    d.text(((W - dw) / 2, 90), date_line, font=F_DATE, fill=RED)
    strap = "36 stories  ·  9 regions  ·  One day, the whole world"
    sw = d.textlength(strap, font=F_STRAP)
    d.text(((W - sw) / 2, 114), strap, font=F_STRAP, fill=MUTED)
    d.text((24, 114), "No. 330", font=F_STRAP, fill=MUTED)
    d.text((W - 24 - d.textlength("One day in print", font=F_STRAP), 114),
           "One day in print", font=F_STRAP, fill=MUTED)

    # ---- date-check band
    d.rectangle([12, 134, W - 12, 158], fill=NAVY)
    check = ("DATE CHECK  —  Every story below happened, or was first reported, "
             "on Thursday 26 November 2026.")
    d.text((20, 140), check, font=F_CHECK, fill=(255, 255, 255))

    # ---- lead stories (3 columns with drawn scenes)
    leads = [
        (draw_balloon_scene, "MACY'S 100TH PARADE POSTPONED",
         "A nor'easter forces the first weather delay in the parade's "
         "100-year history. It moves to Saturday, 8:30 a.m."),
        (draw_fire_scene, "TANKER FIRE KILLS 31 ON CAIRO RING ROAD",
         "A fuel tanker overturns and bursts into flames on the Cairo ring "
         "road. At least 31 die, about 21 hurt."),
        (draw_rocket_scene, "FIRST PAKISTANI ASTRONAUT REACHES TIANGONG",
         "Muhammad Zeeshan Ali boards China's station aboard Shenzhou-24 — "
         "the first foreign national on Tiangong."),
    ]
    col_w = (W - 24 - 2 * 12) // 3
    ly = 166
    lead_h = 156
    for i, (scene, head, body) in enumerate(leads):
        x0 = 12 + i * (col_w + 12)
        d.rectangle([x0, ly, x0 + col_w, ly + lead_h], fill=PAPER,
                    outline=LINE, width=1)
        # draw the scene on its own layer so nothing spills past the panel
        scene_img = Image.new("RGB", (col_w - 8, 80), (0, 0, 0))
        sd = ImageDraw.Draw(scene_img)
        scene(sd, 0, 0, col_w - 8, 80)
        img.paste(scene_img, (x0 + 4, ly + 4))
        ty = ly + 88
        for line in wrap(d, head, F_LEAD_HEAD, col_w - 12):
            d.text((x0 + 6, ty), line, font=F_LEAD_HEAD, fill=INK)
            ty += 18
        max_body = max(0, (ly + lead_h - 4 - ty) // 13)
        for line in wrap(d, body, F_LEAD_BODY, col_w - 12)[:max_body]:
            d.text((x0 + 6, ty), line, font=F_LEAD_BODY, fill=(40, 40, 40))
            ty += 13
        # red number badge, top-right corner of the scene
        d.ellipse([x0 + col_w - 26, ly + 8, x0 + col_w - 6, ly + 28],
                  fill=RED)
        t = str(i + 1)
        tw2 = d.textlength(t, font=F_NUM)
        d.text((x0 + col_w - 16 - tw2 / 2, ly + 12), t, font=F_NUM,
               fill=(255, 255, 255))

    # ---- map + timeline row
    my = 330
    mh = 150
    # map panel
    mx0, mw = 12, 588
    d.rectangle([mx0, my, mx0 + mw, my + mh], fill=PAPER, outline=LINE, width=1)
    d.text((mx0 + 8, my + 5), "WHERE THE DAY HAPPENED — WORLD MAP",
           font=F_SEC, fill=NAVY)
    d.text((mx0 + mw - 8 - d.textlength("Dots = story places, coloured by region",
                                       font=F_LEG), my + 8),
           "Dots = story places, coloured by region", font=F_LEG, fill=MUTED)
    draw_map(d, mx0 + 6, my + 24, mw - 12, mh - 48)
    # legend (SCI has no map dot, so it is left out)
    lx = mx0 + 8
    ly2 = my + mh - 16
    for code in ("NA", "LAT", "EUR", "ME", "AFR", "SA", "EA", "OCE"):
        d.ellipse([lx, ly2 + 1, lx + 8, ly2 + 9], fill=REGION_COLORS[code])
        lx += 11
        name = REGION_NAMES[code]
        d.text((lx, ly2), name, font=F_LEG, fill=INK)
        lx += d.textlength(name, font=F_LEG) + 8
    # timeline panel
    tx0, tw2 = 612, W - 12 - 612
    d.rectangle([tx0, my, tx0 + tw2, my + mh], fill=PAPER, outline=LINE, width=1)
    d.text((tx0 + 8, my + 5), "THE DAY IN UTC", font=F_SEC, fill=NAVY)
    d.line([tx0 + 62, my + 28, tx0 + 62, my + mh - 6], fill=LINE, width=2)
    ty = my + 26
    for t, ev in TIMELINE:
        d.ellipse([tx0 + 56, ty + 2, tx0 + 68, ty + 14], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((tx0 + 8, ty), t, font=F_TIME, fill=NAVY)
        for line in wrap(d, ev, F_TBODY, tw2 - 78):
            d.text((tx0 + 76, ty), line, font=F_TBODY, fill=INK)
            ty += 13
        ty += 2

    # ---- story index: 36 stories in 3 columns
    iy = 488
    d.text((12, iy), "THE DAY'S 36 STORIES", font=F_SEC, fill=NAVY)
    d.text((W - 12 - d.textlength("Numbered 1-36 · regions in colour",
                                  font=F_LEG), iy + 3),
           "Numbered 1-36 · regions in colour", font=F_LEG, fill=MUTED)
    d.line([12, iy + 20, W - 12, iy + 20], fill=INK, width=2)
    col_w = (W - 24 - 2 * 12) // 3
    row_h = 38
    for idx, (region, head, body, _lon, _lat) in enumerate(STORIES):
        col = idx // 12
        row = idx % 12
        x0 = 12 + col * (col_w + 12)
        y0 = iy + 26 + row * row_h
        if row:
            d.line([x0, y0 - 3, x0 + col_w, y0 - 3], fill=LINE, width=1)
        # number badge
        d.ellipse([x0, y0, x0 + 18, y0 + 18], fill=REGION_COLORS[region])
        t = str(idx + 1)
        tw3 = d.textlength(t, font=F_NUM)
        d.text((x0 + 9 - tw3 / 2, y0 + 2), t, font=F_NUM, fill=(255, 255, 255))
        tx = x0 + 24
        head_lines = wrap(d, head, F_HEAD, col_w - 24)
        n_head = min(len(head_lines), 2)
        ty = y0
        for line in head_lines[:n_head]:
            d.text((tx, ty), line, font=F_HEAD, fill=INK)
            ty += 13
        body_lines = wrap(d, body, F_BODY, col_w - 24)
        for line in body_lines[: 3 - n_head]:
            d.text((tx, ty), line, font=F_BODY, fill=(52, 52, 52))
            ty += 12

    # ---- footer: in brief + sources
    fy = iy + 26 + 12 * row_h + 4
    d.line([12, fy, W - 12, fy], fill=INK, width=2)
    ty = fy + 6
    for line in wrap(d, IN_BRIEF, F_FOOT, W - 24):
        d.text((12, ty), line, font=F_FOOT, fill=INK)
        ty += 13
    src = ("Sources: BBC · Reuters · CNN · Al Jazeera · The Guardian · AP · Yonhap · "
           "One Turn — compiled 26 Nov 2026. THE WORLD TODAY · Thursday 26 November 2026.")
    d.text((12, ty + 2), src, font=F_FOOT, fill=MUTED)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
