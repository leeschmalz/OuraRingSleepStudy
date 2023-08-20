library(data.table)
library(dplyr)
library(ggplot2)
library(lubridate)

sleep_data <- fread("./data/sleep_heartrate_data.csv") %>% mutate(time = ymd_hm(time)) %>% rename(sleep_id = id)
alcohol_data <- fread("./data/alcohol_data.csv") %>% mutate(date = as.Date(date))
alcohol_data <- alcohol_data %>% mutate(sleep_id = as.character(NA))

# add sleep id's to alcohol data
for (row in 1:nrow(alcohol_data)){
  date1 <- alcohol_data$date[row]
  print(date1)
  
  # if not sleeping between 10pm and 1am, skip
  window <- sleep_data %>% filter( between(time, ymd_hm(paste0(as.character(date1)," 22:00")), ymd_hm(paste0(as.character(date1+1)," 2:00"))) )
  if (nrow(window)==0) {next}
  if (length(unique(window$sleep_id))>1) {stop(paste0("multiple ids on ", date1))}
  
  # add the sleep_id to alcohol data
  alcohol_data$sleep_id[which(alcohol_data$date==date1)] <- window$sleep_id[1]
}

sleep_data <- sleep_data %>% inner_join(alcohol_data %>% filter(!is.na(value),!is.na(sleep_id)) %>% select(-date) %>% tidyr::pivot_wider(), by="sleep_id")
sleep_data <- sleep_data %>%
  mutate(alcohol_bin = cut(alcohol, 
                           breaks = c(-Inf, 0, 1, 2, 3, 4, 7, Inf), 
                           labels = c("0", "1", "2", "3", "4", "5-7", "8+"), 
                           right = TRUE, 
                           include.lowest = TRUE))

sleep_data <- sleep_data %>%
  group_by(sleep_id) %>%
  mutate(start = min(time)) %>%
  ungroup() %>% 
  mutate(mins_from_start = as.integer(time - start) / 60)

ggplot(sleep_data, aes(x=mins_from_start, y=hr, color=alcohol_bin, group=sleep_id)) +
  geom_line(alpha=0.2) +
  geom_smooth(method="loess", se=FALSE, aes(group=alcohol_bin)) +
  theme_bw()

ggplot() +
  #geom_line(data = sleep_data %>% filter(sleep_id %in% sample(unique(sleep_data$sleep_id), 40)), mapping=aes(x=mins_from_start, y=hr, color=alcohol_bin, group=sleep_id), alpha=0.4) +
  geom_smooth(data = sleep_data, method="loess", se=FALSE, mapping=aes(x=mins_from_start, y=hr, color=alcohol_bin, group=alcohol_bin)) +
  labs(color = "Number of \nAlcoholic Drinks") +
  theme_bw()

ggplot() +
  geom_line(data = sleep_data %>% filter(row_number() == 1), mapping=aes(x=mins_from_start, y=hr, color=alcohol_bin, group=sleep_id), alpha=0.4)

avg_hr_data <- sleep_data %>%
  group_by(sleep_id, alcohol_bin) %>%
  summarize(avg_hr = mean(hr, na.rm = TRUE))

ggplot(avg_hr_data, aes(x=alcohol_bin, y=avg_hr)) +
  geom_boxplot() +
  labs(x = "Number of Alcoholic Drinks", y = "Avg Heart Rate per Night") +
  theme_minimal()