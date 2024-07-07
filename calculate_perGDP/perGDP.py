# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 15:33:43 2024

@author: 3tamura
"""
import pandas as pd

#%%File Name
GDP_File = "OECD_GDP_1947q1-2023q4.csv"
CurrentAccount_File = "OECD_CurrentAccount_1955q1-2023q4.csv"
GoodsBalance_File = "OECD_GoodsBalance_1955q1-2023q4.csv"
FinalConsumption_File = "OECD_FinalConsumption_1947q1-2023q4.csv"

#ファイル名リスト
file_names = [CurrentAccount_File, GoodsBalance_File]

#%%import
df_gdp = pd.read_csv(GDP_File, encoding="utf-8")
df_gdp = df_gdp[df_gdp["Subject"]=="Gross domestic product - expenditure approach"]

countries = df_gdp["Country"].unique().tolist()

#%%GoodsBalance
#データインポート
df_GoodsBalance = pd.read_csv(GoodsBalance_File)

for country in countries:
    goodsbalance_data = df_GoodsBalance[df_GoodsBalance["Country"]==country][["TIME", "Value"]]
    gdp_data = df_gdp[df_gdp["Country"]==country][["TIME", "Value"]]
    goodsbalance_merged_data = pd.merge(gdp_data, goodsbalance_data, on="TIME", how='outer')
	#計算
    goodsbalance_merged_data["perGDP"] = goodsbalance_merged_data["Value_y"]/goodsbalance_merged_data["Value_x"]
    goodsbalance_merged_data = goodsbalance_merged_data.rename(columns={"Value_x": "GDP", "Value_y": "GoodsBalance"})
    goodsbalance_merged_data.to_csv(f"perGDP_{country}_GoodsBalance.csv")
    
#%%CurrentAccount
df_CurrentAccount = pd.read_csv(CurrentAccount_File)

for country in countries:
    currentaccount_data = df_CurrentAccount[df_CurrentAccount["Country"]==country][["TIME", "Value"]]
    gdp_data = df_gdp[df_gdp["Country"]==country][["TIME", "Value"]]
    currentaccount_merged_data = pd.merge(gdp_data, currentaccount_data, on="TIME", how='outer')
	#計算
    currentaccount_merged_data["perGDP"] = currentaccount_merged_data["Value_y"]/currentaccount_merged_data["Value_x"]
    currentaccount_merged_data = currentaccount_merged_data.rename(columns={"Value_x": "GDP", "Value_y": "CurrentAccount"})
    currentaccount_merged_data.to_csv(f"perGDP_{country}_CurrentAccount.csv")
    
#%%Using_FinalConsumption
#Saving = GDP - FinalConsumption
#Investment = Saving - CurrentAccount

df_FinalComsumption = pd.read_csv(FinalConsumption_File)

#Saving&Investment
for country in countries:
    #Saving計算
    target_data = df_FinalComsumption[df_FinalComsumption["Country"]==country][["TIME", "Value"]]
    gdp_data = df_gdp[df_gdp["Country"]==country][["TIME", "Value"]]
    saving_data = pd.merge(gdp_data, target_data, on="TIME", how='outer')
    saving_data["perGDP"] = 1 - (saving_data["Value_y"]/saving_data["Value_x"])
    saving_data = saving_data.rename(columns={"Value_x": "GDP", "Value_y": "Saving"})
    saving_data.to_csv(f"perGDP_{country}_Saving.csv")
    
    #Investment計算
    currentaccount_data_ = df_CurrentAccount[df_CurrentAccount["Country"]==country][["TIME", "Value"]]
    investment_data = pd.merge(saving_data, currentaccount_data_, on="TIME", how='outer')
    investment_data["Investment"] = investment_data["Saving"] - investment_data["Value"]
    investment_data["perGDP"] = investment_data["Investment"] / investment_data["GDP"]
    investment_data =  investment_data.drop(["Saving", "Value"], axis=1).reindex(["TIME", "GDP", "Investment", "perGDP"], axis='columns')
    investment_data.to_csv(f"perGDP_{country}_Investment.csv")