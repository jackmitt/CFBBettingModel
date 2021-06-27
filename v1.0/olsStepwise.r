library(tidyverse)
library(MASS)

data <- read.csv("./csv_data/bigboyAlt.csv")
XcolsNA <- data %>% dplyr::select(5:158, 166, 168, 170:193)
# Spread <- data %>% select(168)
Xcols <- na.omit(XcolsNA)

spreadModel = lm(Actual.Spread~.,Xcols)
summary(spreadModel)

step.model <- stepAIC(spreadModel, direction = "backward", trace = 1)
summary(step.model)
