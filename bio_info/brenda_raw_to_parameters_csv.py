#%%
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 10:39:37 2023
@author: tai4t
"""
from data_cleaner import remove_whitespace_comma, get_notes, to_ascii, clean_EC, clean_target, output_adjusted_txt
def search_obtain_values(enzyme_data, header, search_KW): 
    EC = enzyme_data.split("\n")[0] 
    EC = clean_EC(EC)
    out_txt = ""
    if "\n"+header in enzyme_data: # 目的の項目があるかどうか判定
        target_data = enzyme_data.split("\n" + header + "\n")[1].split("\n\n")[0]
        entries = target_data.split(search_KW + "\t")[1:]
        for entry in entries:
            entry = remove_whitespace_comma(entry) 
            try:
                S = entry.split("{")[1].split("}")[0]
            except IndexError:
                S = ""
            target = entry.split("# ")[1].split("<")[0].split("{")[0].strip()
            if header != "PROTEIN": 
                target = clean_target(target)
            try:
                notes = entry.split("(#")[1].split(">)")[0]
            except IndexError:
                notes = ""

            org_num = entry.split("#")[1].split("#")[0]
            ref = entry.split("<")[1].split(">")[0]
            pH, T, soln, notes = get_notes(entry)
            out_txt += output_adjusted_txt(EC, S, org_num, target, pH, T, soln, ref, notes)
            # ID = f"{EC}_{org_num}_{ref}_{S}_{notes}"
            # out_txt += f"\n{ID},{EC},{S},{org_num},{target},{pH},{T},{soln},{ref},{notes}"
    return out_txt


#%%
with open("brenda_2023_1.txt", "r", encoding = "UTF-8") as f:
    raw_txt = f.read() 
raw_txt = to_ascii(raw_txt)
enzyme_dataset = raw_txt.split("\nID\t")[2:] # 酵素番号でdata分割（始めの説明は飛ばす） 
header_search_KW_pairs ={"KM_VALUE":"KM", 
                        "KCAT_KM_VALUE":"KKM",
                        "TURNOVER_NUMBER":"TN",
                        "PROTEIN": "PR"} 
for header, search_KW in header_search_KW_pairs.items():
    out_txt = f"ID,EC,Substrate,org_num,{header},pH,T,soln,Reference,Notes"
    for enzyme_data in enzyme_dataset:
        out_txt += search_obtain_values(enzyme_data, header, search_KW)

    file_name = f"brenda_{search_KW}.csv".lower()    
    with open(file_name, "w", encoding = "UTF-8") as f:
        f.write(out_txt)          