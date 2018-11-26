
#install.packages("'pinnacle.data'", lib="C:/R/Rpackages")

Install from Cran (NOT ON CRAN YET)

install.packages('pinnacle.data')
install.packages('odds.converter')
install.packages("devtools")

library(pinnacle.data)
library(odds.converter)
library(dplyr)

data("MLB2016")


MLB2016 <- MLB2016 %>% mutate(AwayStartingPitcher=tolower(ifelse(grepl(" ", AwayStartingPitcher), AwayStartingPitcher, paste(substring(AwayStartingPitcher, 1,1),substring(AwayStartingPitcher, 2)))),
                            HomeStartingPitcher=tolower(ifelse(grepl(" ", HomeStartingPicher), HomeStartingPicher, paste(substring(HomeStartingPicher, 1,1),substring(HomeStartingPicher, 2)))),
                            AwayStartingPitcher=gsub("\\.", "", AwayStartingPitcher),
                            HomeStartingPitcher=gsub("\\.", "", HomeStartingPitcher)
)

Sys.setenv(TZ = "America/Toronto")

MLB2016_2 <- MLB2016[, -c(11,12)]
write.table(MLB2016_2, file="MLB2016.csv", sep = ',', row.names = F)

## Extracting lines
MLB2016_lines <- MLB2016[, 'Lines']
df_lines <- NULL
for(i in 1:length(MLB2016_lines$Lines)) {
  game1 <- MLB2016_lines[i,]
  df <- data.frame(game1$Lines)
  df$GameId <- rep(MLB2016[i,]$GameID, nrow(df))
  if (!is.null(df_lines)) {
    df_lines <- rbind(df_lines, df)
  } else {
    df_lines = df
  }
}
write.table(df_lines, file="df_lines.csv", sep = ',', row.names = F)
length(unique(df_lines$GameId))

