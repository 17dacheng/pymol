set seq_view, on
remove resn HOH
util.cbc
split_chains

distance hbonds, chain A, chain B, 3.5, mode=2
select hbonds_atoms, ((chain A and (donors or acceptors)) within 3.5 of (chain B and (donors or acceptors))) or ((chain B and (donors or acceptors)) within 3.5 of (chain A and (donors or acceptors)))
select hbonds_res, byres hbonds_atoms
show sticks, hbonds_res
color red, hbonds_res

distance salt_bridge, chain A and resn LYS+ARG+HIS and (name NZ+NH1+NH2+NE2+ND1), chain B and resn ASP+GLU and (name OD1+OD2+OE1+OE2), 4.0, mode=2
select salt_bridge_atoms, ((chain A and (resn LYS+ARG+HIS) and (name NZ+NH1+NH2+NE2+ND1)) within 4.0 of (chain B and (resn ASP+GLU) and (name OD*+OE*))) or ((chain B and (resn LYS+ARG+HIS) and (name NZ+NH1+NH2+NE2+ND1)) within 4.0 of (chain A and (resn ASP+GLU) and (name OD*+OE*)))
select salt_bridge_res, byres salt_bridge_atoms
show sticks, salt_bridge_res
color blue, salt_bridge_res

distance hydrophobic_effect, chain A and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO, chain B and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO, 5.0, mode=2
select hydrophobic_atoms, ((chain A and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO) within 5.0 of (chain B and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO)) or ((chain B and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO) within 5.0 of (chain A and resn ALA+VAL+LEU+ILE+PHE+TRP+MET+PRO))
select hydrophobic_res, byres hydrophobic_atoms
show sticks, hydrophobic_res
color yellow, hydrophobic_res
