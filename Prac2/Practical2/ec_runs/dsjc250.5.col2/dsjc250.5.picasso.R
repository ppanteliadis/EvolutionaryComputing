# Generate graphs for the 2nd practical on EC
# Iteratively goes through the directories in ec_runs and generates the plots
# for the final report

# Mute warnings
options(warn=-1)

if (!require(ggplot2, quietly = T)){
    library(ggplot2)
}

if (!require(RColorBrewer, quietly = T)) {
    library(RColorBrewer)
}

# Set the stage for the outputs
if (!dir.exists("Plots"))
    dir.create("Plots")


# Define a custom color blind friendly palette
cb.palette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442")
names(cb.palette) = as.factor(c(26, 27, 28, 29, 30))


# Generate the Fitness as a function of time plots
for (i in 1:5){
    i <- 1
    run <- paste("run", i, sep = '')
    
    # Initialize a ggplot object for this run
    plot <- ggplot() +
        ggtitle(paste("dsjc250.5.col", run)) +
        scale_x_continuous(limits = c(0, 100)) +
        scale_y_continuous(limits = c(0, 50)) +
        theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 
    
    for (j in 27:30){
        curr.run <- paste(run,"/", "dsjc250.5.col_", i, "_", j, ".log", sep = '')
        if (file.exists(curr.run)) {
            # Read the file in a dataframe
            df <- read.csv(curr.run, header = T, sep = '\t')
            df$Colors <- as.factor(j)
            plot <- plot + 
                geom_line(data = df, aes(x = Seconds, y = BestFitness, color = Colors)) +
                scale_color_manual(values = c("26" = "#999999", "27" = "#E69F00", "28" = "#56B4E9", "29" = "#009E73", "30" = "#F0E442"))
        }
    }
    
    png(paste("Plots/dsjc250.5.col_", run, "_fit_sec.png", sep = ''))
    print(plot)
    dev.off()
}

# Generate the Fitness as a function of Generations plot
for (i in 1:5){
    run <- paste("run", i, sep = '')
    
    # Initialize a ggplot object for this run
    plot <- ggplot() +
        ggtitle(paste("dsjc250.5.col", run)) +
        scale_y_continuous(limits = c(0, 50)) + 
        scale_x_continuous(limits = c(0, 300)) +
        theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 
    
    for (j in 29:30){
        curr.run <- paste(run,"/", "dsjc250.5.col_", i, "_", j, ".log", sep = '')
        if (file.exists(curr.run)) {
            # Read the file in a dataframe
            df <- read.csv(curr.run, header = T, sep = '\t')
            df$Colors <- as.factor(j)
            plot <- plot + 
                geom_line(data = df, aes(x = Generations, y = BestFitness, color = Colors)) +
                scale_color_manual(values = c("26" = "#999999", "27" = "#E69F00", "28" = "#56B4E9", "29" = "#009E73", "30" = "#F0E442"))
        }
    }
    
    png(paste("Plots/dsjc250.5.col_", run, "_fit_gen.png", sep = ''))
    print(plot)
    dev.off()
}