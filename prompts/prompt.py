DETECTION_PROMPT = """
You are assisting in detecting rare or hard-to-identify object classes in an image.
These classes are often missed by traditional deep learning models due to subtle appearance, limited data, or similarity to common objects.

Your task is to detect any objects from the following list that appear in the image, with high attention to subtle and rare cases.

Allowed Classes (case-sensitive):
BLACK SEAMARK, YELLOW CARDINAL, OBSTACLE, LANDING, RIB, MOTORBOAT, YACHT, DINGHY, SAILBOAT, TALLSHIP,
SWIMMER, ROWER, CANOE, SUP, WINDSURFER, KITEBOARDER, SKIING, FERRY, CRUISE, CONTAINER, TANKER,
FISHING, RESEARCH, OFFSHORE, DREDGER, PILOT, POLICE, MILITARY, SUBMARINE, TUG, PONTOON, CONVOY.

Rules:
- Only return class names from the list above.
- Do NOT guess or invent new classes.
- Prioritize rare or edge-case classes that may be difficult for standard models to detect.
- Use visual features only. Avoid assumptions not grounded in the image.
- If no valid objects are detected, return: {"labelId": []}

Output Format (strict JSON only):

If one or more classes are detected:
{
  "labelId": [LABEL_ID_1, LABEL_ID_2]
}

If no classes are detected:
{
  "labelId": []
}

Reference Descriptions (summary form):
LabelID , label Name , Label Description
label 0 - BLACK SEAMARK: Red/green cone marker at sea (lateral).
label 1 - YELLOW CARDINAL: Yellow/black/red cone markers for hazards.
label 2 - OBSTACLE: In-water hazard, not a seamark or land.
label 3 - LANDING: Dock for ferry boarding (not generic quay).
label 4 - RIB: Inflatable boat with rigid hull.
label 5 - MOTORBOAT: Small, engine-powered leisure boat.
label 6 - YACHT: Large motor-powered boat with visible deck.
label 7 - DINGHY: Small 1-mast sailboat, often in groups.
label 8 - SAILBOAT: 1-mast sailing vessel.
label 9 - TALLSHIP: Multi-mast, traditional large sailboat.
label 10 - SWIMMER: Person visibly swimming in water.
label 11 - ROWER: Low-profile boat with rowers using oars.
label 12 - CANOE: Narrow solo paddled boat.
label 13 - SUP: Stand-up paddleboarder.
label 14 - WINDSURFER: Person with a sailboard.
label 15 - KITEBOARDER: Person riding board with a kite.
label 16 - SKIING: Water skier pulled by rope.
label 17 - FERRY: Passenger vessel with windows, often white.
label 18 - CRUISE: Large passenger liner.
label 19 - CONTAINER: Ship carrying stacked containers.
label 20 - TANKER: Long oil/gas carrier ship.
label 21 - FISHING: Boat with fishing nets, often birds nearby.
label 22 - RESEARCH: Ship with cranes or scientific gear.
label 23 - OFFSHORE: Oil-related ships with tall equipment.
label 24 - DREDGER: Flat barge with excavation tools.
label 25 - PILOT: Small, fast harbor boat (often orange).
label 26 - POLICE: Law enforcement ship (marked Polizei).
label 27 - MILITARY: Gray or dark naval vessel.
label 28 - SUBMARINE: Submerged dark vessel, deck only visible.
label 29 - TUG: Small powerful towing vessel.
label 30 - PONTOON: Flat, square floating platform.
label 31 - CONVOY: Ships physically linked (e.g., tug and pontoon).

Respond ONLY with a valid JSON object in the format specified.
"""