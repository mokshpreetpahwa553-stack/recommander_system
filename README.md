# recommander_system
# StudyHub

StudyHub is a learning resource recommender. You tell it what you want to learn, how experienced you are, and what kind of resource you like (a video or an article), and it gives you a short list of matches sorted in a sensible order for your level.

I built it as a Python project with a Streamlit front end, a PostgreSQL database, and a small machine learning pipeline that estimates how hard a piece of text is to read.

## What it does

1. Collects videos from the YouTube Data API and articles from NewsAPI for a long list of Python topics.
2. Turns the title and description of every resource into a numeric embedding so that meaning can be compared.
3. Scores each resource for reading difficulty with a regression model trained on readability datasets, then groups resources into three levels: beginner, intermediate and advanced.
4. Takes a user's goal, level and preferred format, finds the most relevant resources, and orders them to suit the user's level.
5. Lets users sign up, sign in, or continue as a guest, and saves their search history.

## How the recommendation works

The recommender is built from a few small steps, each in its own file.

**Relevance.** The user's goal is embedded with the `all-MiniLM-L6-v2` sentence transformer. Because the embeddings are normalised, a simple dot product gives the cosine similarity between the goal and every stored resource. The top 20 by similarity are kept.

**Format preference.** Each of those 20 gets a final score of 0.6 times its similarity plus 0.4 times a preference value. The preference value is 1.0 if the resource format matches what the user asked for and 0.3 otherwise. The top 10 by final score move on.

**Difficulty ordering.** The 10 resources are arranged according to the user's level:

* A beginner sees level 1, then 2, then 3.
* An intermediate user sees level 2, then 3, then 1.
* An advanced user sees level 3, then 2, then 1.

Inside each difficulty level, resources are sorted by their final score, highest first.

**Difficulty scoring.** A TF IDF vectoriser and a linear regression model are trained on two readability datasets, where a higher target means easier text. Predictions for all stored resources are standardised, and the 33rd and 67th percentiles are used as cut points. The lowest third becomes level 1, the middle third level 2 and the top third level 3. The raw score is also stored in the database.

There is also an older module, `user_resource_difficulty.py`, that scores resources by the gap between user level and resource level. It is kept for reference and is not used in the current pipeline.

## Project structure

| `main_streamlit.py` - Streamlit app with sign in, sign up, guest mode and history menus |
| `recommander_system.py` - Collects user input, builds the profile, runs the recommender and prints results |
| `goal_topic_similarity.py` - Embeds the user goal and ranks resources by cosine similarity |
| `output_difficultyLevel_sort.py` - Orders results for beginner, intermediate and advanced users |
| `fetch_resources_from_postgres.py` - Reads videos or articles from the database |
| `fetch_youtubeVids_using_api.py` - Fetches videos from the YouTube Data API |
| `fetch_articles_using_api.py` - Fetches articles from NewsAPI |
| `add_videos_to_db.py` - Runs a large batch of video queries and inserts results with embeddings |
| `add_articles_to_db.py` - Does the same for articles |
| `difficluty_scoreANDembedding.py` - Scores difficulty for every stored resource and builds embeddings |
| `difficulty_model.py` - Trains and saves the difficulty regression pipeline |
| `logistic_reg.py` - An earlier experiment that classified difficulty with logistic regression |
| `user_input_credentials.py` - Sign up and sign in with Argon2 password hashing |
| `user_resource_difficulty.py` - Older gap based difficulty scoring, currently unused |
| `db_config.py` - Reads database settings from environment variables |
| `pass_checker.py` - A separate command line password tool, not part of the recommender |

## Database

The main table is `resources`.

| Column | Type | Notes |
| --- | --- | --- |
| `resource_id` | integer | Primary key, generated from a sequence |
| `title` | text | Required |
| `description` | text | Optional |
| `resource_type` | text | Either `video` or `article` |
| `difficulty_score` | numeric(10,3) | Standardised score from the regression model |
| `difficulty_category` | smallint | 1, 2 or 3, enforced by a check constraint |
| `url` | text | Required |
| `source` | text | Channel or publication name |
| `language` | varchar(15) | Defaults to `en` |
| `embedding` | real[] | 384 dimensional sentence embedding |

Other tables used by the app are `users` (username, email, password hash), `query_history` (user, query text, resource type used) and `view_history`, which references `resources.resource_id` through a foreign key.

## Getting started

### What you need

* Python 3.10 or newer
* PostgreSQL running locally or somewhere you can reach
* A YouTube Data API key
* A NewsAPI key


### Install

```bash
git clone <your repository url>
cd <your repository folder>
python -m venv venv
source venv/bin/activate
pip install streamlit psycopg2-binary sentence-transformers scikit-learn pandas numpy joblib argon2-cffi colorama python-dotenv requests google-api-python-client
```

### Configure

Create a `.env` file in the project root. Never commit it.

```

POSTGRES_PASSWORD=your_password_here
YOUTUBE_API_KEY=your_youtube_key
ARTICLES_API_KEY=your_newsapi_key
```

Then create the database and the tables described above.

### Build the data

Run these in order from the project root.

```bash
python difficulty_model.py
python add_videos_to_db.py
python add_articles_to_db.py
```

The first command trains the difficulty model and saves it as `text_scorer_pipeline.pkl`. The next two fetch resources, store them with embeddings, remove duplicate URLs, and then score difficulty for everything in the table. These scripts send a very large number of API requests, so check your daily quota first.

### Run the app

```bash
streamlit run main_streamlit.py
```

Choose Sign in, Sign up or Guest, then open the Recommendation system option. Signed in users have their searches saved.

## Known limitations

* The recommender currently supports videos and articles only. Courses and research papers appear as options but have no data behind them yet.
* The goal and level inputs in `recommander_system.py` use the terminal `input()` function, so they are better suited to the command line than to the Streamlit page.
* Difficulty is judged from the title and description only, so it is an estimate and not a true measure of how hard a resource is.

## Ideas for the future

* Use the user's intent and view history to improve ranking.
* Add courses and research papers as resource types.
* Move the Streamlit app to proper form inputs instead of terminal prompts.
* Evaluate the difficulty model against hand labelled examples.
