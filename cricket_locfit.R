ballbyball <- read.csv('C:/Users/Ryan/Dropbox/analytics/cricket/balls_with_info_small.csv', stringsAsFactors = FALSE)
ballbyball$date <- as.Date(ballbyball$date, format="%m/%d/%Y")
ballbyball <- ballbyball[order(ballbyball$date, ballbyball$game_id),]

inn1 <- ballbyball[ballbyball$innings %in% '1st innings',]
inn2 <- ballbyball[ballbyball$innings %in% '2nd innings',]

# train on 2009 to 2012 games
train_inn1 <- inn1[inn1$date < as.Date('2013-01-01',format='%Y-%m-%d'),]
train_inn2 <- inn2[inn2$date < as.Date('2013-01-01',format='%Y-%m-%d'),]

predict_inn1 <- inn1[inn1$date >= as.Date('2013-01-01',format='%Y-%m-%d'),]
predict_inn2 <- inn2[inn2$date >= as.Date('2013-01-01',format='%Y-%m-%d'),]

library(locfit)
win_prob_inn1 <- locfit(bat_win ~
                          inn_runs +
                          inn_wickets +
                          balls_left +
                          resources_left,
                        family = 'binomial',
                        data = train_inn1)
win_prob_inn2 <- locfit(bat_win ~
                          inn_runs +
                          inn_wickets +
                          balls_left +
                          resources_left +
                          runs_to_chase,
                        family = 'binomial',
                        data = train_inn2)

predictions_inn1 <- predict(win_prob_inn1, newdata = predict_inn1, se = TRUE, type = 'response')
predictions_inn2 <- predict(win_prob_inn2, newdata = predict_inn2, se = TRUE, type = 'response')

predict_inn1$win_prob <- predictions_inn1$fit
predict_inn1$moe <- predictions_inn1$se.fit
predict_inn2$win_prob <- (1-predictions_inn2$fit)
predict_inn2$moe <- predictions_inn2$se.fit

all_predict <- rbind(predict_inn1, predict_inn2)
all_predict <- all_predict[order(all_predict$game_id, all_predict$innings),]

indvsa <- all_predict[all_predict$game_id %in% 656423,]
indvuae <- all_predict[all_predict$game_id %in% 656439,]

random <- all_predict[all_predict$game_id %in% sample(unique(all_predict$game_id),1),]
plot(1:nrow(random), random$win_prob, type = 'l')
View(random)
