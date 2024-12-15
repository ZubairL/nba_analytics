install.packages(c("tictoc","wehoop", "progressr", "dplyr"))
library(wehoop)
library(tictoc)
library(progressr)
library(dplyr)

# Pull most recent 12 years of play by play data
tictoc::tic() 
progressr::with_progress({
  # API times out with more than 3 years
  wnba_pbp3 <- wehoop::load_wnba_pbp(c(2013, 2014, 2015))
  wnba_pbp4 <- wehoop::load_wnba_pbp(c(2016, 2017, 2018))
  wnba_pbp1 <- wehoop::load_wnba_pbp(c(2019, 2020, 2021))
  wnba_pbp2 <- wehoop::load_wnba_pbp(c(2022, 2023, 2024))

})
tictoc::toc()
wnba_df <- bind_rows(wnba_pbp3, wnba_pbp4, wnba_pbp1,  wnba_pbp2)
write.csv(wnba_df,"wnba_pbp_2013-24.csv", row.names = FALSE)


# Pull player box score data by game
gameids <- unique(wnba_df$game_id)

tictoc::tic()
progressr::with_progress({
  # API times out with more than 3 years
  wnba_player3 <- wehoop::load_wnba_player_box(c(2013, 2014, 2015))
  wnba_player4 <- wehoop::load_wnba_player_box(c(2016, 2017, 2018))
  wnba_player1 <- wehoop::load_wnba_player_box(c(2019, 2020, 2021))
  wnba_player2 <- wehoop::load_wnba_player_box(c(2022, 2023, 2024))

})
tictoc::toc()
wnba_player_df <- bind_rows(wnba_player3, wnba_player4, wnba_player1,  wnba_player2)
write.csv(wnba_player_df,"wnba_playerbox_2019-24.csv", row.names = FALSE)


# Pull team box score data by game
gameids <- unique(wnba_df$game_id)

tictoc::tic() 
progressr::with_progress({
  # API times out with more than 3 years
  wnba_team3 <- wehoop::load_wnba_team_box(c(2013, 2014, 2015))
  wnba_team4 <- wehoop::load_wnba_team_box(c(2016, 2017, 2018))
  wnba_team1 <- wehoop::load_wnba_team_box(c(2019, 2020, 2021))
  wnba_team2 <- wehoop::load_wnba_team_box(c(2022, 2023, 2024))
  
})
tictoc::toc()
wnba_team_df <- bind_rows(wnba_team3,wnba_team4, wnba_team1,  wnba_team2)
write.csv(wnba_team_df,"wnba_teambox_2013-24.csv", row.names = FALSE)

# Pull schedule & game details
tictoc::tic() 
progressr::with_progress({
  # API times out with more than 3 years
  wnba_sched3 <- wehoop::load_wnba_schedule(c(2013, 2014, 2015))
  wnba_sched4 <- wehoop::load_wnba_schedule(c(2016, 2017, 2018))
  wnba_sched1 <- wehoop::load_wnba_schedule(c(2019, 2020, 2021))
  wnba_sched2 <- wehoop::load_wnba_schedule(c(2022, 2023, 2024))
  
})
tictoc::toc()
wnba_sched_df <- bind_rows(wnba_sched3, wnba_sched4, wnba_sched1,  wnba_sched2)
write.csv(wnba_sched_df,"wnba_schedule_2013-24.csv", row.names = FALSE)


# individual games
# x <- wehoop::wnba_data_pbp(game_id = "1022100189")

#check number of games in 2024
#test <- wnba_df[wnba_df$season == 2024,]
#test2 <-unique(test$game_id)
