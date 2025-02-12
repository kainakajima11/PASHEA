```yaml
para : ["Cr", "Mn", "Fe", "Co", "Ni", "H", "O", "Ti"]

# consolidate_phase_ratio_file.py
consolidatePhaseRatioFile :
    input_dir : "."
    input_filename : "phase_ratio"
    output_dir : "."
    csv_filename : "PhaseRatio"
# make_GB_model.py
makeGBModel :
    crack_type: "Tri" # Tri, Rec, Hex
      #car_file_path : "/nfshome17/knakajima/work/BaseStructure/car/Ni015.car"
    car_file_path : "/nfshome17/knakajima/work/BaseStructure/car/Ni_sigma5.car"
      #replicate_num : [14, 6, 3]
    replicate_num : [15, 14, 7]
    crack_depth : 0.33
    crack_angle : 0.28
    empty_length : 25.0
      #lattice_const : [3.57, 18.203454313280364, 18.203454313280364]
    lattice_const : [3.57, 7.98275908059, 7.98275908059] # to012, multiply 2.236066969353008 013, 3.162287173666288
    output_file_path : "input01111.rd"
    type_ratio : [0, 25, 25, 25, 25, 0, 0]
    both_direction : False
    crack_size : 5.0
# add_strain_line.py
addStrainLine :
    input_file_path : None
    strain_velocity : 1.0
# calculate_mols_num_needed.py
calculateMolsNumNeeded :
    init_mol : [6,6,7] # this list become sf.atoms[type]
    aim_density : 1.50
calculateAlloyDensity :
    crystal_type : "FCC"
    lattice_const : [3.57, 3.57, 3.57]
AlloyDensity :
    CrMnFeCoNi : 8.050866744877927
```
