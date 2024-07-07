library(openxlsx)
library(tidyverse)

#PROD作成
AUS_NIOT <- read.xlsx("AUS_NIOT_nov16.xlsx", sheet=2)
NIOT_aus2000 <- AUS_NIOT[AUS_NIOT["Year"]=="2000",]
PROD_aus2000 <- NIOT_aus2000[NIOT_aus2000["Origin"]=="Domestic", 5:60]
PROD_aus2000 <- PROD_aus2000[2:57,]

#FINAL作成
FINAL_aus2000 <- NIOT_aus2000[NIOT_aus2000["Origin"]=="Domestic", 61:65]
FINAL_aus2000 <- FINAL_aus2000[2:57,]

#PROD,FINAL結合
SAM_aus2000 <- PROD_aus2000
SAM_aus2000 <- SAM_aus2000 %>%  mutate("capital"="", "labor"="", "TXSP"="", "TAX2"="")
SAM_aus2000 <- cbind(SAM_aus2000, FINAL_aus2000)

#SEAからAUSだけ抜き出し
Socio_Economic_Accounts <- read.xlsx("Socio_Economic_Accounts.xlsx", sheet=2)
SEA_aus <- Socio_Economic_Accounts[Socio_Economic_Accounts["country"]=="AUS", 1:19]

#CAP&LAB作成,転置
CAP_aus <- SEA_aus[SEA_aus["variable"]=="CAP",]
CAP_aus2000 <- CAP_aus["2000"]
LAB_aus <- SEA_aus[SEA_aus["variable"]=="LAB",]
LAB_aus2000 <- LAB_aus["2000"]

CAP_aus2000_t <- t(CAP_aus2000)
LAB_aus2000_t <- t(LAB_aus2000)

#CAP&LABをSAMに結合
CAP_aus2000_t <- append(CAP_aus2000_t, c(capital="", labor="", TXSP="", TAX2="", CONS_h="", CONS_np="", CONS_g="", GFCF="", INVEN=""), after = 56)
SAM_aus2000 <- rbind(SAM_aus2000, CAP_aus2000_t)

LAB_aus2000_t <- append(LAB_aus2000_t, c(capital="", labor="", TXSP="", TAX2="", CONS_h="", CONS_np="", CONS_g="", GFCF="", INVEN=""), after = 56)
SAM_aus2000 <- rbind(SAM_aus2000, LAB_aus2000_t)

#TAX行作成
TXSP_aus <- AUS_NIOT[AUS_NIOT["Code"]=="TXSP",]
TXSP_aus2000 <- TXSP_aus[TXSP_aus["Year"]=="2000", 5:60]
TXSP_aus2000 <- TXSP_aus2000 %>%  mutate("capital"="", "labor"="", "TXSP"="", "TAX2"="", "CONS_h"="", "CONS_np"="", "CONS_g"="", "GFCF"="", "INVEN"="")
TAX2 <- NA[1:65]
SAM_aus2000 <- rbind(SAM_aus2000, TXSP_aus2000[2,1:65])
SAM_aus2000 <- rbind(SAM_aus2000, TAX2)

#FINAL行作成
CONS_h <- NA[1:65]
CONS_np <- NA[1:65]
CONS_g <- NA[1:65]
GFCF <- NA[1:65]
INVEN <- NA[1:65]
SAM_aus2000 <- rbind(SAM_aus2000, CONS_h, CONS_np, CONS_g, GFCF, INVEN)

#code列作成
code <- colnames(SAM_aus2000)
SAM_aus2000 <- cbind(code, SAM_aus2000)
