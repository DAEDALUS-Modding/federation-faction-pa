import shutil
import os
import os.path
import json

import paeiou

from pa_location import pa_location

gen = "gen"
dl_path = "download"
stage_path = "stage"

mod_urls = {
    "legion": "https://github.com/Legion-Expansion/Legion-Expansion/releases/latest/download/com.pa.legion-expansion-server.zip",
    "s17": "https://github.com/DAEDALUS-Modding/Section-17/releases/latest/download/s17-server.zip"
}

def gen_unit_shadows():
    def write_shadowed_json(unit, unit_filename):
        out_filename = os.path.join(gen, unit_filename[1:])
        os.makedirs(os.path.dirname(out_filename), exist_ok = True)
        with open(out_filename, "w") as out:
            json.dump(unit, out)

    def adj_build_types(units, adjustment):
        for unit_filename in units:
            with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
                unit = json.load(unit_file)
            unit["buildable_types"] = f"({unit['buildable_types']}){adjustment}"
            write_shadowed_json(unit, unit_filename)

    def override_build_types(unit_filename, new_build):
        with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
            unit = json.load(unit_file)
        unit["buildable_types"] = new_build
        write_shadowed_json(unit, unit_filename)

    def carry_over_shadows(units):
        for unit_filename in units:
            with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
                unit = json.load(unit_file)
            write_shadowed_json(unit, unit_filename)

    paeiou.simulate_mod_mount(pa_location, mod_urls, dl_path, stage_path)


    # MLA and Legion Commanders may both build the Federation Factories
    comms = [
        "/pa/units/commanders/base_commander/base_commander.json",
        "/pa/units/commanders/l_base/l_base.json",
    ]
    adj_build_types(comms, " | (Custom4 & Cmdbuild - Custom1 - Custom2 - Custom3)")

    mla_factories = [
        "/pa/units/air/air_factory/air_factory.json",
        "/pa/units/land/bot_factory/bot_factory.json",
        "/pa/units/sea/naval_factory/naval_factory.json",
        "/pa/units/orbital/orbital_launcher/orbital_launcher.json",
        "/pa/units/land/vehicle_factory/vehicle_factory.json",
        "/pa/units/sea/naval_factory_adv/naval_factory_adv.json",
        "/pa/units/land/bot_factory_adv/bot_factory_adv.json",
        "/pa/units/air/air_factory_adv/air_factory_adv.json",
        "/pa/units/land/vehicle_factory_adv/vehicle_factory_adv.json",
        "/pa/units/orbital/orbital_factory/orbital_factory.json",
        "/pa/units/land/unit_cannon/unit_cannon.json"
    ]
    carry_over_shadows(mla_factories)

    mla_fabricators = [
        "/pa/units/land/fabrication_bot/fabrication_bot.json",
        "/pa/units/land/fabrication_vehicle/fabrication_vehicle.json",
        "/pa/units/air/fabrication_aircraft/fabrication_aircraft.json",
        "/pa/units/land/fabrication_bot_combat/fabrication_bot_combat.json",
        "/pa/units/sea/fabrication_barge/fabrication_barge.json",
        "/pa/units/land/fabrication_bot_combat_adv/fabrication_bot_combat_adv.json",
        "/pa/units/orbital/orbital_fabrication_bot/orbital_fabrication_bot.json",
        "/pa/units/land/fabrication_bot_adv/fabrication_bot_adv.json",
        "/pa/units/land/fabrication_vehicle_adv/fabrication_vehicle_adv.json",
        "/pa/units/air/fabrication_aircraft_adv/fabrication_aircraft_adv.json",
        "/pa/units/sea/fabrication_ship_adv/fabrication_ship_adv.json",
        "/pa/units/land/bot_support_commander/bot_support_commander.json"
    ]
    carry_over_shadows(mla_fabricators)

def main():
    if os.path.isdir(gen):
        shutil.rmtree(gen)

    shutil.copytree("export", gen, dirs_exist_ok=True)

    paeiou.paeiou( 
        mod_id = "com.pa.daedalus.federat", 
        paeiou_unit_path = "PAEIOU_units/", 
        unit_add_list = "unit_add_list.txt", 
        output_path = "gen/",
        mod_prefix = "federat",
        server = True,
        client = False,
        pa_path = pa_location
    )
    gen_unit_shadows()

if __name__ == '__main__':
    main()
