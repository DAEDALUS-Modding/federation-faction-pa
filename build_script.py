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
    "legion": "https://github.com/Legion-Expansion/Legion-Expansion/releases/latest/download/com.pa.legion-expansion-server.zip"
}

def gen_unit_shadows():
    def adj_build_types(units, adjustment):
        for unit_filename in units:
            with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
                unit = json.load(unit_file)
            unit["buildable_types"] = f"({unit['buildable_types']}){adjustment}"

            out_filename = os.path.join(gen, unit_filename[1:])
            os.makedirs(os.path.dirname(out_filename), exist_ok = True)
            with open(out_filename, "w") as out:
                json.dump(unit, out)

    def override_build_types(unit_filename, new_build):
        with open(os.path.join(stage_path, unit_filename[1:])) as unit_file:
            unit = json.load(unit_file)
        unit["buildable_types"] = new_build

        out_filename = os.path.join(gen, unit_filename[1:])
        os.makedirs(os.path.dirname(out_filename), exist_ok = True)
        with open(out_filename, "w") as out:
            json.dump(unit, out)

    paeiou.simulate_mod_mount(pa_location, mod_urls, dl_path, stage_path)


    # MLA and Legion Commanders may both build the Federation Factories
    comms = [
        "/pa/units/commanders/base_commander/base_commander.json",
        "/pa/units/commanders/l_base/l_base.json",
    ]
    adj_build_types(comms, " | (Custom4 & Cmdbuild - Custom1 - Custom2 - Custom3)")

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
