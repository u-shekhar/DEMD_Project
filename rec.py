# Dataframe manipulation library
import pandas as pd

# To supress warnings
import warnings
warnings.filterwarnings('ignore')


# ### Creating the user input
title_1 = input("Enter the first movie name : ")
rating_1 = float(input("Enter the rating for the first movie : "))
title_2 = input("Enter the second movie name : ")
rating_2 = float(input("Enter the rating for the second movie : "))
title_3 = input("Enter the first movie name : ")
rating_3 = float(input("Enter the rating for the above movie : "))
title_4 = input("Enter the first movie name : ")
rating_4 = float(input("Enter the rating for the above movie : "))
title_5 = input("Enter the first movie name : ")
rating_5 = float(input("Enter the rating for the above movie : "))

def movie_recommender(title_1,rating_1,title_2,rating_2,title_3,rating_3,title_4,rating_4,title_5,rating_5) :
    # Importing required files
    movies_df = pd.read_csv(r'C:\Users\ujjwa\Desktop\Python\DEMD\Project\movies.csv')

    # Checking the movies dataframe
    # movies_df.head()

    # ### Data preprocessing

    # The year in the title of the movie is of no use as such. Let's make a new column out of it.

    # Using regular expressions to find a year stored between parentheses
    # We specify the parantheses so we don't conflict with movies that have years in their titles
    movies_df['year'] = movies_df.title.str.extract('(\(\d\d\d\d\))',expand=False)

    # Removing the parentheses
    movies_df['year'] = movies_df.year.str.extract('(\d\d\d\d)',expand=False)

    # Removing the years from the 'title' column
    movies_df['title'] = movies_df.title.str.replace('(\(\d\d\d\d\))', '')

    # Using the strip function to remove any whitespace characters that may have appeared
    movies_df['title'] = movies_df['title'].apply(lambda x: x.strip())
    # movies_df.head()


    # Now stripping the genres based on '|' to form a list.
    #Every genre is separated by |, using the split function on |
    movies_df['genres'] = movies_df.genres.str.split('|')
    # movies_df.head()


    # Now creating the one hot encoded version for the data frame. Here we will have a column for each genre, representing the genres for every single row of movies.
    #Copying the movie dataframe into a new one.
    moviesWithGenres_df = movies_df.copy()

    #For every row in the dataframe, iterate through the list of genres and place a 1 into the corresponding column
    for index, row in movies_df.iterrows(): # Gives index and all data for each row
        
        for genre in row['genres']: # Picking the list of genres for that particular movie/row from movies_df
            
            moviesWithGenres_df.at[index, genre] = 1 
            # Put '1' in the exact positions in the new copied dataframe 
            # creating new columns for each genres. Index would be same as movies_df.
            # The positions where '1' was not places would be na.    
            # Here the 1s represent that the particular movie belongs to that genre.
            
    #Filling in the NaN values with 0 to show that a movie doesn't have that column's genre
    moviesWithGenres_df = moviesWithGenres_df.fillna(0)
    # moviesWithGenres_df.head()


    # ## Content Based Recommendation

    # - Here, we're going to try to figure out the users' favorite genres from the movies based on ratings given by them.
    # - We'll build the user profile of the user and understand which genres the user likes the most and which genre the least. Based on this user profiling, we will try to recommend best 20 movies to the user.
    # - The recommendation would be based on the genres of the movies that he liked would be suggested to him/her.
    # 
    # Let's begin by creating an input user to recommend movies to: ('Active User')
    # 
    # (To add more movies, we can simply increase the movies in the userInput. We should write it in capital letters and if a movie starts with a "The", like "The Matrix" then write it in like this: 'Matrix, The' .)

    # # ### Creating the user input
    # title_1 = input("Enter the first movie name : ")
    # rating_1 = float(input("Enter the rating for the first movie : "))
    # title_2 = input("Enter the second movie name : ")
    # rating_2 = float(input("Enter the rating for the second movie : "))
    # title_3 = input("Enter the first movie name : ")
    # rating_3 = float(input("Enter the rating for the above movie : "))
    # title_4 = input("Enter the first movie name : ")
    # rating_4 = float(input("Enter the rating for the above movie : "))
    # title_5 = input("Enter the first movie name : ")
    # rating_5 = float(input("Enter the rating for the above movie : "))


    userInput = [
                {'title':title_1, 'rating':rating_1},
                {'title':title_2, 'rating':rating_2},
                {'title':title_3, 'rating':rating_3},
                {'title':title_4, 'rating':rating_4},
                {'title':title_5, 'rating':rating_5}
                ] 

    # Using the dictionary to create the data frame
    inputMovies = pd.DataFrame(userInput)
    # inputMovies


    # # Creating the user input data frame (Considering only 5 movies here)

    # # Storing the details in a list of dictionaries.
    # # Here there should not be any repetition of movies. It would create problem while setting movieId as index later. 

    # userInput = [
    #             {'title':'Breakfast Club, The', 'rating':5},
    #             {'title':'Toy Story', 'rating':3},
    #             {'title':'Jumanji', 'rating':1},
    #             {'title':'Pulp Fiction', 'rating':5},
    #             {'title':'Mulan', 'rating':5},
    #             {'title':'Akira', 'rating':4.5}
    #             ] 

    # # Using the dictionary to create the data frame
    # inputMovies = pd.DataFrame(userInput)
    # inputMovies


    # ### Identifying the movies from user input and mapping it with the ratings

    # Now we have to find the movie id from movies data set and map this rating to that movie.
    # P.S :
    # - If the movie is not in our original dataset or is mis spelled then it could not be found and can't be proceeded further with that movie.


    # Filtering out the movies by title
    # Creating the list of movie titles in the inputMovies.
    # Filtering the original movies_df based on titles present in the list

    inputId = movies_df[movies_df['title'].isin(inputMovies['title'].tolist())]
    print(len(inputId))

    # Merging it so we can get the movieId. It's implicitly merging it by title.
    inputMovies = pd.merge(inputId, inputMovies)

    #inputMovies


    # Dropping genres and year column that is not required.
    inputMovies = inputMovies.drop(['genres','year'], axis = 1)

    # Final input dataframe
    inputMovies


    # #### If a movie we added above, is not here, then it might not be present in the original data frame or it might spelled wrong. We can check this manually to confirm. We should also check for capitalisation.
    # 

    # ### Filtering these input movies from moviesWithGenres_df
    # - We will create a new data frame of it as userMovies

    # In[12]:


    #Filtering out the movies from the input
    # Creating list of movie id's from inputMovies that we mapped to original movies_df.
    # Using this list we will filter the moviesWithGenres_df to have rows of only those 5 movies

    userMovies = moviesWithGenres_df[moviesWithGenres_df['movieId'].isin(inputMovies['movieId'].tolist())]
    # userMovies


    # ### For creating user profile, we need only the genres.
    # - Removing the remaining columns.

    #Resetting the index to avoid future issues. Index would not be required for this data frame in future.
    # It's just for building user profile.
    userMovies = userMovies.reset_index(drop=True)

    # Dropping the other columns except different genre columns 
    userGenreTable = userMovies.drop(['movieId','title','genres','year'], axis = 1)
    # userGenreTable


    # - From the userGenreTable, we can definitely tell which genres he has watched or based on these 5 movies, we can determine the genres to which these movies fall into.
    # - By applying the ratings as weight and aggregating the scores for each genre, we can identify which would be the ratings he like the most.

    # #### Now we can use the ratings for each movie and multiply it with the genres and sum up the values for a particular genre to get the weight of the genre. 
    # 
    # #### This way we can get the user profile and his interests in different genres of movies.

    # Checking the input ratings for each movie
    # inputMovies['rating']


    # ## Creating the user profile

    # Now multiplying the rating with the genre table and summing up to get the genre weights for that particular user i.e creating a user profile.

    # - For multiplying the userGenreTable and inputMovies rating column, the dimension of them should match like, if one has n rows and the other should have n columns.
    # - Since, we want the final output as the weighted scores of all the genres, we will have to take transpose of it and multiply by ratings. This way we match the dimension requirement as well as the we get the desired output.
    # - It would be like the first genre Adventure field for each movies would be multiplied to corresponding ratings and summed up to give one value for Adventure genre. That would be the user preference for the genre Adventure. 
    # - This would continue for every single genre we had created a column of.


    # Taking the dot produt to get weights
    userProfile = userGenreTable.transpose().dot(inputMovies['rating'])

    #The user profile
    userProfile_df = pd.DataFrame(data=userProfile, columns=['Preferences'])
    # userProfile_df


    #  ### This is the user profile we wanted.
    #  - Here we can see that this particular user likes comedy the most!
    #  - From this we can make sure we never suggest the user the movies which fall into the genres with have a score of 0 in the user profile. We can suggest the movies that fall into the genres with maximum scores.

    # ## Recommendation based on user profile
    # - Now we will try to score every movie in our actual moviesWithgenre_df using this preference weights

    # In[16]:


    #Now let's get the genres of every movie in our original dataframe and setting the movie id as index also

    genreTable = moviesWithGenres_df.set_index(moviesWithGenres_df['movieId'])
    # genreTable


    # - We only need the genres for finding the preference of each movies based on user profile. So, dropping rest all the columns.


    # Dropping the unnecessary columns

    genreTable = genreTable.drop(['movieId','title','genres','year'], axis = 1)
    # genreTable.head()


    # In[18]:


    # Verifying the size 
    #genreTable.shape


    # - Now we have just the genres for all movies in our dataset with their index as movieId
    # - For calculating the scores for every movie, we will take the weighted average of every movie based on user profile. 
    # - For this we will need to take the dot product of the user profile with the genres table created in previous step. 
    # - It would result in a single score for every single movie based on which we can make the recommendation.

    # In[19]:


    # Multiplying the genres table by the weights (user preferences) and then taking the weighted average.
    # Here the genre table is from the actual dataframe not the one used for creating user profile with only 5 records.

    recommendationList = ((genreTable*userProfile).sum(axis=1))/(userProfile.sum())
    #recommendationList


    # Sort our recommendations in descending order
    recommendationList = recommendationList.sort_values(ascending=False)

    # Checking the result obtained
    # recommendationList.head()


    # - Now we have all the movies in our database with their preference scores. 
    # - But we should make sure that we don't recommend the movies that the user has reviewed for or the input movies in this case.
    # - So, removing the input movies from the recommendation list.

    # ### Removing input movies from recommendation list
    # Removing the input movies

    for id in inputId.movieId.tolist() :
        recommendationList.pop(id)


    # - Now we have the prefect list with the user preference scores for all the other movies. Now, we can sort this in descending order and suggest the top 20 movies to the user.

    # ## The final recommendation


    #The final recommendation table with top 20 movies

    recommendationTable_df = movies_df.loc[movies_df['movieId'].isin(recommendationList.head(20).keys())]
    #recommendationTable_df.head()


    # - Resetting the index, as it is not required now.

    # In[23]:


    # Resetting the index.

    recommendationTable_df = recommendationTable_df.reset_index(drop=True)
    #rec = recommendationTable_df[["title","year","genres"]][:5].to_json(orient='records')
    return recommendationTable_df


suggestions = movie_recommender(title_1,rating_1,title_2,rating_2,title_3,rating_3,title_4,rating_4,title_5,rating_5)

print(suggestions.title[0],suggestions.year[0])