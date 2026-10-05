# Introduction & Problem Definition

I would like to predict whether or not I won a game of Super Smash Brothers Melee. To do so, my target variable will be whether or not I won. Since victory is binary, this will be a classification problem. 

Although the greater public at large does not stand to benefit from my findings, I do. This is an interesting question to investigate, as it might be possible to find patterns in my own data that I can learn from. Perhaps there is a character I struggle against, or a stage that aligns best with my strategy.

Sun Tzu once said that if you know your enemy and know yourself, you need not fear the result of a thousand battles. I doubt he was talking about video games, and this project won't help me know my enemy. That said, it will help me understand myself, so ideally I'll need not fear the result of a couple extra battles by the end of this.

# Background & Context

### The Game

For this project, knowledge of this game is required to understand the analysis. The nuances aren't relevant, but I will summarize all of the relevant details. Super Smash Brothers Melee (which I will henceforth refer to as Melee) is a platform fighting game released for the Nintendo GameCube in 2001. Two players will face off against each other as one of 26 characters, and each has four lives, known as "stocks." When a player reaches zero lives, they lose. Each match is on an 8:00 minute maximum timer, and at the end of this timer (rarely reached, never reached by me) the player with less stocks (or more damage if there is no difference in stock count) loses. Each of my games were played on one of six stages, each with their own platform layout and length, which can empower or dampen certain strategies.

Where Melee differentiates itself from other fighting games like Tekken or Street Fighter is the damage system. Instead of dying after taking a certain amount of damage (a health bar), characters instead take increased knockback from moves as they take more damage, and die when they are forced out of the bounds of the stage. As an example, Sheik's basic aerial attack would barely move an opponent at 0 percent (damage is known as percent), but an opponent at 140 percent would go flying into the edge of the stage (known as the blastzone) and die. Again, in summary, as a character takes more damage, they are knocked back more.

It is also important to that each character functions differently. Some characters run faster, some jump higher, some have greater range. Beyond their physics, each character also has their own (mostly) unique set of moves. Each character has different strengths and weaknesses to take advantage of. Characters are not created equal, and some are noticably better than others in almost every circumstance, but that is beyond the scope of this project.

### Previous Work

My previous statistical project was exploring a different game, Team Fortress 2. This study aims to improve upon some of the pitfalls I ran into during my prior study. While investigating Team Fortress 2, I examined the strength of different weapons for a certain role. I used a dataset from a certain server, which had data from many different players. An issue I encountered was that I could not quantify the skill of the player, nor could I account for the context of the match. Another challenge (although I wouldn't say pitfall) was that determining how "strong" a weapon is wasn't terribly quantifiable. Determining how likely I am to win is a straightforward target variable, and will make for easier analysis.

To rectify these errors, I decided that Melee would be a much more suitable game to examine. For one, I no longer need to account for skill of the player, given that the player (yours truly) remains constant. Far more importantly in my opinion, the context of Melee games is much easier to quantify. Understanding the context to a Team Fortress 2 game requires qualitative analysis, whereas a Melee game can be fairly accurately summarized through the variables of stage and characters.

# Data Analysis & Summary

### Creating My Dataset

The data used for this project has come from the past three months of my Melee games. Each game was stored as a .slp file, which measures controller inputs on each frame of the game. Melee runs at 60 frames per second, and each game is usually somewhere between two and four minutes. My raw dataset consists of around 800 .slp files, representing 800 games of Melee, some of which get tuned out during my data cleaning process.

Due to the sheer amount of information in each .slp file, I was able to track numerous variables. I will now explain each variable in a list:

- **Player & Opponent Character**: The characters selected by myself and my opponent. Typically, I pick Sheik, though I may pick Yoshi if my intention is to demonstrate style rather than win.
- **Stage**: There are six playable stages used in my dataset. They do have fair influence on how a match plays out, but that is beyond the scope of this project.
- **Player & Opponent Total Damage**: The total damage dealt by either myself or my opponent.
- **Player & Opponent Openings**: The number of openings obtained by either myself or my opponent across the match. An opening (defined by Slippi, the medium through which I play Melee) is a period of time. It begins when a player is able to land a combo, where one move stuns the opponent long enough for the player to land a second move. The opening ends once the aggrieved player is actionable (able to input moves) for 45 frames.
- **Player Neutral Wins**: The number of neutral wins obtained by either myself or my opponent across the match. A neutral break is very similar to an opening, but does not require a combo to be considered an opening. Openings count as neutral breaks, but a neutral break might not always be an opening. For example, landing a single strong attack is a neutral break, but not an opening.
- **Total Neutral Breaks**: The combination of neutral breaks between myself and my opponent.
- **Match Length**: An integer, representing the number of frames in a game. A game ends and frames stop being counted once someone loses their last stock.

One variable that would be very helpful to track, but is (in my opinion) impossible to track, is mindset. There are days when I am focused, there are days where I am not. There was a study decades ago that aimed to disprove the notion that a hot streak improved performance, aimed at basketball. However, from a newer study on basketball, they claim that "not only is this streak selection bias large enough to invalidate the conclusions of previous studies, but it masks significant evidence of substantial hot hand shooting in their data" (Miller). The study goes on to explain that performance streaks do actually have an effect on continued performance. However, there is simply no way for me to even remotely quantify this. I suppose I could have evaluated my focus on a scale after each match, but I have a fervent hatred of the self-evaluated 1-10 metric.

### Data Understanding & Exploration

When evaluating my models, I provided it with an example game of my Sheik against a Fox that was a fairly close game. I tried using two random states, 42 and 39. For random state 42, the random trees and gradient boosting both predicted I'd lose, only winning around 48 percent of the time. The logistic regression was far less forgiving, with a 27 percent chance of victory. Much to my chagrin, the pessimistic logistic regression had 77 percent accuracy, compared to the 75 percent accuracy of my other two models. For random state 39, all of the models were quite confident I'd win, and the logistic regression had improved to over 80 percent accuracy. Obviously, this concerns me, since the random state should not affect the results so much.

It occured to me after these results, then, that around 600 data entries was not as much data as I thought it was. Since there are 26 playable characters in melee, I actually don't even have a hundred games of comparison per character. Notably, some characters are much more common to see than others. Fox, Marth, Falco, Sheik, and Captain Falcon are all pretty common characters to see, whereas characters like Mario, Donkey Kong, Ice Climbers, and Link are almost never seen. I want to be clear that it isn't as though I only had 23 datapoints for my Sheik versus each character (that math comes from 600/26), but it is true that I didn't reach 100 entries for a single character. I'd like to revisit this project when I reach 2500 .slp files on my laptop and see if the results change, though that won't be for a very long time.

Across different characters, the odds of me winning generally hover between 45 and 55 percent. There are exceptions to this, like Jigglypuff and Ice Climbers who I have an abyssmal record against. It does make sense to me that my record is fairly evenly distributed. Although different characters do have strengths and weaknesses against each other, each match generally comes down to the skill of the player. The platform I use to play melee, Slippi, does match players against opponents of similar skill, which does explain the fairly even winrates.

### Data Preparation & Feature Selection

Earlier, I explained that my dataset was created from hundreds of .slp files, which store raw controller inputs. Astute readers may have realized that 60 raw controller inputs per second are almost completely uninterpretable. For my dataset, I had to convert these .slp files into a workable .csv for my code. Unfortunately for me, constructing a .slp parser to extract the variables I desired was well beyond my expertise, and would take tens of hours of work. Fortunately for me, someone else (the creator of Slippi) already made one and I used that to convert my files into a .csv for easy use. The [github repository](https://github.com/project-slippi/slippi-js) is linked here.

One stat that I'd originally parsed from the .slp files was kills, which indicate how many stocks a player took during a game. The model was very confident I'd win whenever I took 4 stocks (p=1) and very confident I wouldn't whenever I didn't (p=0). As it turns out, since you only have 4 stocks per game, kills are a direct proxy variable for whether or not you win. To avoid obvious data leakage, I did not let my model use this variable.

To split the training and testing data, I used pretty standard settings of 80% training and 20% testing. I also tried the experiment with two different random states to see if that impacted the data, and as explained earlier, it had a substantial impact.

# The Model

### Baseline & Model Development

The baseline I established for developing my models was a logistic regression. Regression is easy for statistical analysis, and a good benchmark to compare my more advanced models to. I trained two models, those being Random Forest and Gradient Boosting classifiers.

The Random Forest model was chosen due to it's association with classification tasks. Since I had several variables for a model to play with, I figured a decision tree would preduce accurate results. The Gradient Boosting model was chosen after I found it while researching for this project. Per IBM, the gradient boosting algorithm builds models sequentially, each step tries to correct the mistakes of the previous iteration (Noble). This concept intrigued me since I figured the self-correctiveness could lead to higher accuracy, though it ended up just as effective as the Random Forest model.

The model I ended up selecting was, to my dismay, the logistic regression. In both of the random states I experimented with, its accuracy was higher than both of the machine learning models. Boring as it may be, regression is a powerful statistical tool, and should not be underestimated.

### Model Interpretation & Insights

The models all concluded that openings were the strongest determiner of who would win. I am glad to see this as the result, as it's also been the conclusion of the community for years. Getting an opening on your opponent is incredibly important to winning in melee, since combos deal immense damage, put your opponent in poor positions, and prevent them from hitting you. In fact, in an experiment where researchers attempted to create an AI, they tracked five metrics when training their AI: kills, damage, opening conversion rate, openings per kill, damage per opening (Lee). Opening conversion rate is openings over neutral wins, for further explanation.

The model performs very sporadically on characters I don't have much data against, but this is to be expected. On the characters with plenty of data, I do have winrates close to 50 percent. I already explained a potential cause of this earlier, that being the matchmaking system.

One interesting conclusion that is fair to draw from the model is my poor performance on Pokemon Stadium, especially against Fox and Falco. While this conclusion wouldn't be interesting to someone active in the Melee community, since this is the common stage of choice for Fox and Falco when fighting Sheik, I do think it's interesting that these stereotypes are actually statistically founded and provable. I would chalk up my poor performance on this stage to the uneven ground, which impacts Sheik's long, grounded combos far more than Fox or Falco's (typically) air-based combos.

Beyond that, the model cannot tell me much with certainty. There isn't enough data to draw confident conclusions, and since my winrate against most characters is around 50 percent, there isn't much interesting there. I cannot say that Fox is a particularly hard matchup for me, or that Marth is an easy one, despite what the community agrees on about Sheik. Most importantly given my research question, I cannot predict whether I will win a match with great certainty. I think that sort of makes sense, though. It's not as though I always lose against Fox on Pokemon Stadium, or that I always beat Samus on Battlefield. Even if I had an 80% winrate on certain circumstances, a good model would still predict incorrectly 20% of the time.

# Limits, Ethics, & Reflection

One bias in the gap that I would actually be happy to see is an artificially lowered winrate for me. On Slippi, you can quit out of a game. Some (not a lot, but some) opponents do quit out before they lose, either due to anger or wanting to play the next game. During my data cleaning process, I ensured that the game had to be played to completion (someone reaches 0 stocks) for it to count, otherwise it would be scrubbed. This means that there are a few wins I would have had that were scrubbed because the game wasn't completed. To what extent this affected the model, I do not know.

No one will be affected by false predictions. The dedicated population of people watching me play and betting on me (currently and almost certainly forever 0) won't be able to look at my model for advice, since the model is attempting to guess whether or not I **did** win, not whether or not I **will** win.

Although this model is not currently ready for real-world decision making, I do have faith that with more data, it could reveal some very interesting patterns in my gameplay, particularly in hard matchups for me. It should be stated that while the model's goal is to predict whether or not I won a game based on match performance, the actual purpose of the model is to reflect on my gameplay.

I would be interested in remaking this model with just characters and stages. As I went through this project, I realized that the retrospective statistics offer too much information sometimes. If the point of the model is to figure out where I struggle and where I thrive, then it shouldn't worry about how I did in *a* match, but how I did in the *majority* of matches.

# Code and Transparency

### Sources

Lee, M., Hu, W., Do, S. (2025). Training Super Smash Bros. Melee Agents. Stanford University. https://cs224r.stanford.edu/spring_2025/projects/pdfs/cs224rfinalprojectreport.pdf

Miller, J. B., Sanjurjo, A. (2019). A Bridge from Monty Hall to the Hot Hand: The Principle of Restricted Choice. Journal of Economic Perspectives—Volume 33. https://pubs.aeaweb.org/doi/pdfplus/10.1257/jep.33.3.144


Noble, Joshua. (2025). Gradient boosting classifiers in Scikit-Learn and Caret. IBM. https://www.ibm.com/think/tutorials/gradient-boosting-classifier