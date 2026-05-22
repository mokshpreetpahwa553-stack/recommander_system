import psycopg2

#connecting to postgres
conn = psycopg2.connect(
    host="localhost",
    database="recommander_system",
    user='postgres',
    password="Sachin1130!",
    port=5432
)

cur=conn.cursor()

articles=[('art_001', 'Python Built-in Functions: A Complete Guide', 'Use Python built-in functions for math, data types, iterables, and I/O', 'article', None, None, 'https://realpython.com/python-built-in-functions', 'realpython', 'en'),
('art_002', 'How to Flatten a List of Lists in Python', 'Learn to flatten nested lists in Python programming', 'article', None, None, 'https://realpython.com/python-flatten-list', 'realpython', 'en'),
('art_003', 'Testing Your Code With Python unittest', 'Complete guide to testing Python code with unittest', 'article', None, None, 'https://realpython.com/python-unit-testing', 'realpython', 'en'),
('art_004', 'Variables in Python: Usage and Best Practices', 'Python variables explained with best practices', 'article', None, None, 'https://realpython.com/python-variables', 'realpython', 'en'),
('art_005', 'Altair: Declarative Charts With Python', 'Data visualization with Altair and Python', 'article', None, None, 'https://realpython.com/python-altair-declarative-charts', 'realpython', 'en'),
('art_006', 'Dictionaries in Python', 'Complete guide to Python dictionaries', 'article', None, None, 'https://realpython.com/python-dictionaries', 'realpython', 'en'),
('art_007', 'Using Loguru to Simplify Python Logging', 'Python logging made simple with Loguru', 'article', None, None, 'https://realpython.com/python-loguru', 'realpython', 'en'),
('art_008', 'ChatterBot: Build a Chatbot With Python', 'Build chatbots with Python and ChatterBot', 'article', None, None, 'https://realpython.com/python-chatbot-chatterbot', 'realpython', 'en'),
('art_009', 'Python Basics: A Practical Introduction to Python 3', 'Beginner Python course and sample chapters', 'article', None, None, 'https://static.realpython.com/python-basics-sample-chapters.pdf', 'realpython', 'en'),
('art_010', 'The Python Tutorial — Python 3 Documentation', 'Official Python tutorial from Python.org', 'article', None, None, 'https://docs.python.org/3/tutorial/index.html', 'python.org', 'en'),
('art_011', 'Learn Python Basics - GeeksforGeeks', 'Python basics tutorial for beginners', 'article', None, None, 'https://www.geeksforgeeks.org/python/python-basics/', 'geeksforgeeks', 'en'),
('art_012', 'The Best Way to Learn Python - FreeCodeCamp', 'Complete Python programming tutorial for beginners', 'article', None, None, 'https://www.freecodecamp.org/news/the-best-way-to-learn-python-python-programming-tutorial-for-beginners/', 'freecodecamp', 'en'),
('art_013', 'What Is the Best Way to Learn Python? - Coursera', 'Expert guide to learning Python programming', 'article', None, None, 'https://www.coursera.org/articles/best-way-to-learn-python-programming', 'coursera', 'en'),
('art_014', 'Your First Machine Learning Project in Python', 'Step-by-step ML project in Python from scratch', 'article', None, None, 'https://machinelearningmastery.com/machine-learning-in-python-step-by-step/', 'machinelearningmastery', 'en'),
('art_015', '60+ Python Projects for All Levels - DataCamp', 'Python project ideas for beginners to advanced', 'article', None, None, 'https://www.datacamp.com/blog/60-python-projects-for-all-levels-of-expertise', 'datacamp', 'en'),
('art_016', 'Python Roadmap: A 12-Month Learning Path - DataCamp', 'Structured 12-month Python learning roadmap', 'article', None, None, 'https://www.datacamp.com/blog/python-roadmap-12-month-learning-path', 'datacamp', 'en'),
('art_017', 'How to Learn Python From Scratch in 2026 - DataCamp', 'Expert guide to learning Python from scratch', 'article', None, None, 'https://www.datacamp.com/blog/how-to-learn-python-from-scratch-in-2026', 'datacamp', 'en'),
('art_018', 'Python Data Types Explained - DataCamp', 'Beginner guide to Python data types', 'article', None, None, 'https://www.datacamp.com/blog/python-data-types-explained', 'datacamp', 'en'),
('art_019', 'Python Interview Questions For 2026 - DataCamp', 'Top Python interview questions and answers', 'article', None, None, 'https://www.datacamp.com/blog/top-python-interview-questions-and-answers', 'datacamp', 'en'),
('art_020', 'Web Scraping Projects for All Skill Levels - DataCamp', 'Python web scraping project ideas', 'article', None, None, 'https://www.datacamp.com/blog/web-scraping-projects-ideas-all-skill-levels', 'datacamp', 'en')]

cur.executemany("""
    INSERT INTO resources(id, title, description, resource_type, 
    difficulty_score, difficulty_category, url, source, language)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    articles
)

conn.commit()

cur.close()
conn.close()

print("DONE!!")
