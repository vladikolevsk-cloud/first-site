import random
from flask import Flask, jsonify, render_template, request
import json
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from ai_verdict import get_build_verdict

app = Flask(__name__)
'[https://api.opendota.com/api/heroes](https://api.opendota.com/api/heroes)'
ITEMS_BASE_URL = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/items/"
headers = {"User-Agent": "Mozilla/5.0 (dota-randomizer)"}
res = requests.get('https://api.opendota.com/api/heroes', headers=headers, timeout=10)
 
print("STATUS:", res.status_code)          
print("BODY:", res.text[:300])            
 
res.raise_for_status() 
data = res.json()
 
character = []
for hero in data:
    short_name = hero['name'].replace('npc_dota_hero_', '')
    image_url = f"https://cdn.cloudflare.steamstatic.com/apps/dota2/images/dota_react/heroes/{short_name}.png"
    character.append({
       'name': hero['localized_name'],
       'image': image_url
    })

boots = [
    {"name": "Power Treads", "image": ITEMS_BASE_URL + "power_treads.png"},
    {"name": "Phase boots", "image": ITEMS_BASE_URL + "phase_boots.png"},
    {"name": "Guardian Greaves", "image": ITEMS_BASE_URL + "guardian_greaves.png"},
    {"name": "Boots of Bearning", "image": ITEMS_BASE_URL + "boots_of_bearing.png"},
    {"name": "Travel boots", "image": ITEMS_BASE_URL + "travel_boots_2.png"}
]

top_items = [
    {"name": "Silver edge", "image": ITEMS_BASE_URL + "silver_edge.png"},
    {"name": "Daedalus", "image": ITEMS_BASE_URL + "greater_crit.png"},
    {"name": "Abysall blade", "image": ITEMS_BASE_URL + "abyssal_blade.png"},
    {"name": "Bloodthorn", "image": ITEMS_BASE_URL + "bloodthorn.png"},
    {"name": "MKB", "image": ITEMS_BASE_URL + "monkey_king_bar.png"},
    {"name": "Nullifier", "image": ITEMS_BASE_URL + "nullifier.png"},
    {"name": "Overwhelming_blink", "image": ITEMS_BASE_URL + "overwhelming_blink.png"},
    {"name": "Swift blink", "image": ITEMS_BASE_URL + "swift_blink.png"},
    {"name": "Arcane blink", "image": ITEMS_BASE_URL + "arcane_blink.png"},
    {"name": "Battle fury", "image": ITEMS_BASE_URL + "bfury.png"},
    {"name": "Armlet of Mordiggan", "image": ITEMS_BASE_URL + "armlet.png"},
    {"name": "Butterfly", "image": ITEMS_BASE_URL + "butterfly.png"},
    {"name": "Desolator", "image": ITEMS_BASE_URL + "desolator.png"},
    {"name": "Parasma", "image": ITEMS_BASE_URL + "devastator.png"},
    {"name": "Divine rapier", "image": ITEMS_BASE_URL + "rapier.png"},
    {"name": "Satanic", "image": ITEMS_BASE_URL + "satanic.png"},
    {"name": "Mjollnir", "image": ITEMS_BASE_URL + "mjollnir.png"},
    {"name": "Mage Slayer", "image": ITEMS_BASE_URL + "mage_slayer.png"},
    {"name": "Revenants Brooch", "image": ITEMS_BASE_URL + "revenants_brooch.png"},
    {"name": "Radiance", "image": ITEMS_BASE_URL + "radiance.png"},
    {"name": "Manta Style", "image": ITEMS_BASE_URL + "manta.png"},
    {"name": "Disperser", "image": ITEMS_BASE_URL + "disperser.png"},
    {"name": "Hurricane Pike", "image": ITEMS_BASE_URL + "hurricane_pike.png"},
    {"name": "Harpoon", "image": ITEMS_BASE_URL + "harpoon.png"},
    {"name": "Black King Bar", "image": ITEMS_BASE_URL + "black_king_bar.png"},
    {"name": "Blade Mail", "image": ITEMS_BASE_URL + "blade_mail.png"},
    {"name": "Assault Cuirass", "image": ITEMS_BASE_URL + "assault.png"},
    {"name": "Crimson Guard", "image": ITEMS_BASE_URL + "crimson_guard.png"},
    {"name": "Aeon Disk", "image": ITEMS_BASE_URL + "aeon_disk.png"},
    {"name": "Heart of Tarrasque", "image": ITEMS_BASE_URL + "heart.png"},
    {"name": "Lotus Orb", "image": ITEMS_BASE_URL + "lotus_orb.png"},
    {"name": "Shiva's Guard", "image": ITEMS_BASE_URL + "shivas_guard.png"},
    {"name": "Eye of Skadi", "image": ITEMS_BASE_URL + "skadi.png"},
    {"name": "Linken's Sphere", "image": ITEMS_BASE_URL + "sphere.png"},
    {"name": "Heaven's Halberd", "image": ITEMS_BASE_URL + "heavens_halberd.png"},
    {"name": "Sange and Yasha", "image": ITEMS_BASE_URL + "sange_and_yasha.png"},
    {"name": "Yasha and Kaya", "image": ITEMS_BASE_URL + "yasha_and_kaya.png"},
    {"name": "Kaya and Sange", "image": ITEMS_BASE_URL + "kaya_and_sange.png"},
    {"name": "Aghanim's Scepter", "image": ITEMS_BASE_URL + "ultimate_scepter.png"},
    {"name": "Octarine Core", "image": ITEMS_BASE_URL + "octarine_core.png"},
    {"name": "Refresher orb", "image": ITEMS_BASE_URL + "refresher.png"},
    {"name": "Wind waker", "image": ITEMS_BASE_URL + "wind_waker.png"},
    {"name": "Hex", "image": ITEMS_BASE_URL + "sheepstick.png"},
    {"name": "Ethereal Blade", "image": ITEMS_BASE_URL + "ethereal_blade.png"},
    {"name": "Dagon", "image": ITEMS_BASE_URL + "dagon_5.png"},
    {"name": "BloodStone", "image": ITEMS_BASE_URL + "bloodstone.png"},
    {"name": "Aether Lens", "image": ITEMS_BASE_URL + "aether_lens.png"},
    {"name": "Khanda", "image": ITEMS_BASE_URL + "angels_demise.png"},
    {"name": "Meteor Hammer", "image": ITEMS_BASE_URL + "meteor_hammer.png"},
    {"name": "Pipe of insight", "image": ITEMS_BASE_URL + "pipe.png"},
    {"name": "Glimmer", "image": ITEMS_BASE_URL + "glimmer_cape.png"},
    {"name": "Holy Locket", "image": ITEMS_BASE_URL + "holy_locket.png"},
    {"name": "Spirit Vessel", "image": ITEMS_BASE_URL + "spirit_vessel.png"},
    {"name": "Solar Crest", "image": ITEMS_BASE_URL + "solar_crest.png"},
    {"name": "Helm of the overlord", "image": ITEMS_BASE_URL + "helm_of_the_overlord.png"},
    {"name": "Consecreted warps", "image": ITEMS_BASE_URL + "consecrated_wraps.png"},
    {"name": "Crella's Crozier", "image": ITEMS_BASE_URL + "crellas_crozier.png"},
    {"name": "Essence Distiller", "image": ITEMS_BASE_URL + "essence_distiller.png"},
    {"name": "Hydra", "image": ITEMS_BASE_URL + "hydras_breath.png"},
    {"name": "Gleipnir", "image": ITEMS_BASE_URL + "gungir.png"}
] 

roles = ["Pos 1 (Carry)", "Pos 2 (Mid)", "Pos 3 (Offlane)", "Pos 4 (Soft Support)", "Pos 5 (Hard Support)"]


def generate_build():
    chosen_boot = random.choice(boots)
    chosen_items = random.sample(top_items, 5)
    chosen_hero = random.choice(character)
    random.sample(top_items, 5)
    full_inventory = [chosen_boot] + chosen_items
    return {
        "hero": chosen_hero,
        "inventory": full_inventory
    } 

limiter = Limiter(key_func=get_remote_address, app=app)
@app.route("/api/random")
@limiter.limit('2 per second')
def get_random_build():
    return jsonify(generate_build())

@app.route("/api/role")
@limiter.limit('2 per second')
def get_random_role():
    role = random.choice(roles)
    win_chance = random.randint(0, 100)
    return jsonify({
        "role": role,
        "win_chance": win_chance
    })

@app.route("/api/verdict", methods=["POST"])
@limiter.limit('2 per second')
def get_verdict():
    data = request.get_json(force=True)
    if not data: return jsonify({"error": "Invalid JSON data"}), 400
    hero = data.get("hero")
    items = data.get("items")

    if not hero or not items:
        return jsonify({"error": "Missing hero or items"}), 400

    verdict = get_build_verdict(hero, items)
    return jsonify(verdict)

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)

