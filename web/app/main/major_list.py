major_list = ['All', 'Accounting',
'Advertise',
'Architecture',
'Art',
'Bio/BioEngi',
'Chem/ChemEngi',
'Communication',
'CS',
'CE',
'Design',
'Econ',
'Education',
'EE',
'Environment/EnvirEngi',
'Geo',
'Health',
'IEOR',
'Information',
'Journalism',
'Law',
'Material',
'Math',
'ME',
'MFE/FinMath',
'MIS',
'Other',
'OtherEngin',
'Pharm',
'Physics',
'Psych',
'Public',
'Social',
'Stat',
'Teaching/Edu',
'TESOL',
'Urban']


temp_list = []
for item in major_list:
    if item == "All":
        temp_list.append(("", "All"))

    else:
        temp_list.append((item, item))

major_list = temp_list
