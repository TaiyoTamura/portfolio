# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 15:39:19 2023

@author: 3tamura
"""
import pandas as pd

#読み込み[n*n]
df = pd.read_csv("SAM_aus2000_index_code.csv", encoding="utf-8")
df = df.set_index("code")

#操作行・列指定
i_name = "A03"
j_name = "B"

#列基本変形（i列目にj列目の1倍を加える）[n*n]
df_add_column = df.copy()
df_add_column[i_name] = df[i_name] + df[j_name]

#j列消去[n*(n-1)]
df_add_column = df_add_column.drop(j_name, axis=1)

#行基本変形（i行目にj行目の1倍を加える）[n*(n-1)]
df_add_column_index = df_add_column.copy()
df_add_column_index.loc[i_name] = df_add_column.loc[i_name] + df_add_column.loc[j_name]

#j行消去[(n-1)*(n-1)]
df_add_column_index = df_add_column_index.drop(j_name, axis=0)

#名前変更("i_name"_"j_name")
df_new = df_add_column_index.rename(columns={i_name: i_name+"_"+j_name}, index={i_name: i_name+"_"+j_name})
