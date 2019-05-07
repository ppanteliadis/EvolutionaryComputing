# Generate graphs for the 1st practical on EC
# Run individually as Rscript --vanilla graphs.R. Prerequisite: The results of the main algorithm are stored in a directory Data
# Mute warnings
args = commandArgs(trailingOnly=TRUE)
options(warn=-1)

if (!require(ggplot2, quietly = T)){
    library(ggplot2, quietly = T)
}

plots.dir   <- args[1]
data.dir    <- args[2]


# Get the data in to dataframes.
two.point.single.data   <- read.csv(paste(data.dir,'/2-point_single.csv', sep=''), header = T, sep = ';')
graphs.data             <- read.csv(paste(data.dir,'/graphs.csv', sep=''), header = T, sep = ';')
tables.data             <- read.csv(paste(data.dir,'/tables.csv', sep=''), header = T, sep = ';')
uniform.data            <- read.csv(paste(data.dir,'/uniform_single.csv', sep=''), header = T, sep = ';')



# Some processing...
# Sort graphs based on population size and experiment (1st and 3rd column)
graphs.sorted   <- graphs.data[with(graphs.data, order(graphs.data[,1], graphs.data[,2])), ]
graph1          <- graphs.sorted[which(graphs.sorted$Fitness.Function == 'Counting'),]
graph2          <- graphs.sorted[which(graphs.sorted$Fitness.Function == 'Deceptive Tight'),]
graph3          <- graphs.sorted[which(graphs.sorted$Fitness.Function == 'Non-Deceptive Tight'),]
graph4          <- graphs.sorted[which(graphs.sorted$Fitness.Function == 'Deceptive Random'),]
graph5          <- graphs.sorted[which(graphs.sorted$Fitness.Function == 'Non-Deceptive Random'),]



# Add generations to the 2 point and uniform data. Every row, corresponds to another generation. 1st row = 1st generation, etc...
two.point.single.processed              <- two.point.single.data
two.point.single.processed$Generation   <- c(1:nrow(two.point.single.processed))

uniform.processed                       <- uniform.data
uniform.processed$Generation            <- c(1:nrow(uniform.processed))


# Preprocess the joint tables
# Merge the columns we are interested in.
uni.2.point         <- merge(data.frame(uniform.processed[,c(2,3,4,5)], row.names = NULL),
                     data.frame(two.point.single.processed[, c(2,3,4,5)], row.names = NULL), 
                     by = 0, all = TRUE)

uni.2.point.sorted  <- uni.2.point[order(uni.2.point$Generation.y),]



# Start plotting the graphs

# Graph1: Counting Ones Function
graph.1.plot <- ggplot(graph1, aes(x = Population.Size, y = Successes)) + 
    geom_line(aes(colour = Crossover.Function)) + 
    geom_point(aes(colour = Crossover.Function), size=3) + 
    geom_hline(yintercept=24, linetype="dashed", color = "black") +
    xlab("Population") +
    ylab("Successes") +
    ggtitle("Counting Ones Function")+
    scale_color_discrete(name = "Crossover Function") + 
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

graph.1.plot <- graph.1.plot +
    scale_y_continuous(breaks = sort(c(ggplot_build(graph.1.plot)$layout$panel_ranges[[1]]$y.major_source, 24)))

png(paste(plots.dir,"graph1_plot.png", sep = ''))
graph.1.plot
graphics.off()

# Graph2: Deceptive Trap Function (tightly linked)
graph.2.plot <- ggplot(graph2, aes(x = Population.Size, y = Successes)) + 
    geom_line(aes(colour = Crossover.Function)) + 
    geom_point(aes(colour=Crossover.Function), size=3) + 
    geom_hline(yintercept=24, linetype="dashed", color = "black") +
    xlab("Population") +
    ylab("Successes") +
    ggtitle("Deceptive Trap Function (tightly linked)")+
    scale_color_discrete(name = "Crossover Function") + 
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

graph.2.plot <- graph.2.plot +
    scale_y_continuous(breaks = sort(c(ggplot_build(graph.2.plot)$layout$panel_ranges[[1]]$y.major_source, 24)))

png(paste(plots.dir,"graph2_plot.png", sep = ''))
graph.2.plot
graphics.off()



# Graph3: Non-deceptive Trap Function (tightly linked)
graph.3.plot <- ggplot(graph3, aes(x = Population.Size, y = Successes)) + 
    geom_line(aes(colour = Crossover.Function)) + 
    geom_point(aes(colour=Crossover.Function), size=3) + 
    geom_hline(yintercept=24, linetype="dashed", color = "black") +
    xlab("Population") +
    ylab("Successes") +
    ggtitle("Non-Deceptive Trap Function (tightly linked)")+
    scale_color_discrete(name = "Crossover Function") + 
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

graph.3.plot <- graph.3.plot +
    scale_y_continuous(breaks = sort(c(ggplot_build(graph.3.plot)$layout$panel_ranges[[1]]$y.major_source, 24)))

png(paste(plots.dir, "graph3_plot.png", sep = ''))
graph.3.plot
graphics.off()

# Graph4: Deceptive Trap Function (randomly linked).
graph.4.plot <- ggplot(graph4, aes(x = Population.Size, y = Successes)) + 
    geom_line(aes(colour = Crossover.Function)) + 
    geom_point(aes(colour=Crossover.Function), size=3) + 
    geom_hline(yintercept=24, linetype="dashed", color = "black") +
    xlab("Population") +
    ylab("Successes") +
    ggtitle("Deceptive Trap Function (randomly linked)")+
    scale_color_discrete(name = "Crossover Function") + 
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

graph.4.plot <- graph.4.plot +
    scale_y_continuous(breaks = sort(c(ggplot_build(graph.4.plot)$layout$panel_ranges[[1]]$y.major_source, 24)))

png(paste(plots.dir, "graph4_plot.png", sep = ''))
graph.4.plot
graphics.off()




# Graph5: Non-deceptive Trap Function (randomly linked).
graph.5.plot <- ggplot(graph5, aes(x = Population.Size, y = Successes)) + 
    geom_line(aes(colour = Crossover.Function)) + 
    geom_point(aes(colour=Crossover.Function), size=3) + 
    geom_hline(yintercept=24, linetype="dashed", color = "black") +
    xlab("Population") +
    ylab("Successes") +
    ggtitle("Non-deceptive Trap Function (randomly linked)")+
    scale_color_discrete(name = "Crossover Function") + 
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

graph.5.plot <- graph.5.plot +
    scale_y_continuous(breaks = sort(c(ggplot_build(graph.5.plot)$layout$panel_ranges[[1]]$y.major_source, 24)))

png(paste(plots.dir, "graph5_plot.png", sep = ''))
graph.5.plot
graphics.off()



# Fitness mean as a function of Generation
uni.2.point.fitness.mean.plot <- ggplot(data = uni.2.point.sorted, aes(x = Generation.y, y = Fitness.Mean.y)) +
    geom_line(aes(y = Fitness.Mean.x, colour = "Uniform")) +
    geom_line(aes(y = Fitness.Mean.y, colour = "2-Point")) +
    xlab("Generation") +
    ylab("Fitness mean") +
    ggtitle("Fitness mean as a function of generation") +
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

png(paste(plots.dir, "Fitness_mean_generation_plot.png", sep = ''))
uni.2.point.fitness.mean.plot
graphics.off()

# Standard deviation as a function of Generation
uni.2.point.fitness.sd.plot <- ggplot(data = uni.2.point.sorted, aes(x = Generation.y, y = Fitness.Standard.Deviation.y)) +
    geom_line(aes(y = Fitness.Standard.Deviation.x, colour = "Uniform")) +
    geom_line(aes(y = Fitness.Standard.Deviation.y, colour = "2-Point")) +
    xlab("Generation") +
    ylab("Fitness standard deviation") +
    ggtitle("Fitness standard deviation as a function of generation") +
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

png(paste(plots.dir, "Fitness_sd_generation_plot.png", sep = ''))
uni.2.point.fitness.sd.plot
graphics.off()



# Selection errorr as a function of Generation
uni.2.point.selection.error.plot <- ggplot(data = uni.2.point.sorted, aes(x = Generation.y, y = Selection.Error.y)) +
    geom_line(aes(y = Selection.Error.x, colour = "Uniform")) +
    geom_line(aes(y = Selection.Error.y, colour = "2-Point")) +
    xlab("Generation") +
    ylab("Selection Error") +
    ggtitle("Selection Error as a function of generation") +
    theme(legend.title = element_text(face = "bold"), plot.title = element_text(hjust = 0.5)) 

png(paste(plots.dir, "Selection_error_generation_plot.png", sep = ''))
uni.2.point.selection.error.plot
graphics.off()

