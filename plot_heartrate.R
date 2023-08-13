library(data.table)
library(dplyr)
library(ggplot2)
library(lubridate)

data <- fread("./data/heartrate_sleep_example.csv") %>% mutate(time = ymd_hm(time))

ggplot(data, aes(x=time,y=heartrate)) +
  geom_line() +
  ylim(c(30,70))
