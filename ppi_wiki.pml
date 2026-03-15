set seq_view, on
run D:\vscode\pymol\InterfaceResidues.py
interfaceResidue fold_biotheus_inc_5e_9_model_0_target, chain A, chain B
select hydrophobes, (resn ala+gly+val+ile+leu+phe+met+pro+trp)
color red, (interface and hydrophobes and (!name c+n+o))

run D:\Pymol-script-repo\scripts\get_raw_distances.py
distance hbonds, chain A, chain B, 3.5, mode=2
D_hbonds = get_raw_distances("hbonds")
print("number of h-bonds:", len(D_hbonds))

distance salt_bridge, chain A and resn LYS+ARG+HIS and (name NZ+NH1+NH2+NE2+ND1), chain B and resn ASP+GLU and (name OD1+OD2+OE1+OE2), 4.0, mode=2
D_salt = get_raw_distances("salt_bridge")
print("number of salt_bridge:", len(D_salt))

python

if D_hbonds:   
    hbond_atoms = set()
    for atom1, atom2, dist in D_hbonds:
        obj1, idx1 = atom1
        obj2, idx2 = atom2
        hbond_atoms.add(f"{obj1} and index {idx1}")
        hbond_atoms.add(f"{obj2} and index {idx2}")
    hbond_sel = ' + '.join(hbond_atoms)
    cmd.select("hbonds_res", f"byres ( {hbond_sel} )")
    cmd.color("blue", "hbonds_res")
else:
    print("No D_hbonds")

if D_salt:
    salt_atoms = set()
    for atom1, atom2, dist in D_salt:
        obj1, idx1 = atom1
        obj2, idx2 = atom2
        salt_atoms.add(f"{obj1} and index {idx1}")
        salt_atoms.add(f"{obj2} and index {idx2}")
    salt_sel = ' + '.join(salt_atoms)
    cmd.select("salt_bridge_res", f"byres ( {salt_sel} )")
    cmd.color("orange", "salt_bridge_res")
else:
    print("No D_salt")

python end