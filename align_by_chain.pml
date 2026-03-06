reference_object="e9-41bb_42_sample_70"
reference_chain="A"

python
from pymol import cmd
reference_selection = f"{reference_object} and chain {reference_chain}"
all_objects = cmd.get_names('objects')

for mobile_object in all_objects:
    if mobile_object != reference_object:
        mobile_selection = f"{mobile_object} and chain {reference_chain}"
        print(f"Aligning {mobile_selection} to {reference_selection}...")
        
        cmd.align(mobile_selection, reference_selection)
python end

print "批量对齐完成！"