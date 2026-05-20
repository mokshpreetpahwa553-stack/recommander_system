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

articles=[('art_001', 'Python for Beginners - Complete Guide', 'Complete guide to learning Python programming from scratch', 'article', None, None, 'https://realpython.com/start-here', 'realpython', 'en'),
('art_002', 'Python Tutorial - W3Schools', 'Python tutorial covering basics to advanced concepts', 'article', None, None, 'https://w3schools.com/python', 'w3schools', 'en'),
('art_003', 'Learn Python Programming - Python.org', 'Official Python tutorial for beginners', 'article', None, None, 'https://docs.python.org/3/tutorial', 'python.org', 'en'),
('art_004', 'Python Crash Course - Book Review', 'Quick start guide to Python programming fundamentals', 'article', None, None, 'https://realpython.com/python-crash-course', 'realpython', 'en'),
('art_005', 'Python Basics Every Programmer Should Know', 'Essential Python basics for new programmers', 'article', None, None, 'https://medium.com/python-basics', 'medium', 'en'),
('art_006', 'Python Data Types Explained', 'Understanding Python data types and variables', 'article', None, None, 'https://realpython.com/python-data-types', 'realpython', 'en'),
('art_007', 'Python Lists and Tuples', 'Working with lists and tuples in Python', 'article', None, None, 'https://realpython.com/python-lists-tuples', 'realpython', 'en'),
('art_008', 'Python Dictionaries Guide', 'Complete guide to Python dictionaries', 'article', None, None, 'https://realpython.com/python-dicts', 'realpython', 'en'),
('art_009', 'Python Functions Tutorial', 'Learn Python functions and scope', 'article', None, None, 'https://realpython.com/defining-your-own-python-function', 'realpython', 'en'),
('art_010', 'Python Modules and Packages', 'Understanding Python modules and packages', 'article', None, None, 'https://realpython.com/python-modules-packages', 'realpython', 'en'),
('art_011', 'Python Object Oriented Programming', 'Introduction to OOP in Python', 'article', None, None, 'https://realpython.com/python3-object-oriented-programming', 'realpython', 'en'),
('art_012', 'Python Classes and Objects', 'Python classes and objects explained', 'article', None, None, 'https://realpython.com/python-class-objects', 'realpython', 'en'),
('art_013', 'Python Inheritance Tutorial', 'Python inheritance and polymorphism', 'article', None, None, 'https://realpython.com/python-inheritance', 'realpython', 'en'),
('art_014', 'Python Decorators Explained', 'Understanding Python decorators with examples', 'article', None, None, 'https://realpython.com/primer-on-python-decorators', 'realpython', 'en'),
('art_015', 'Python Generators Tutorial', 'Python generators and iterators explained', 'article', None, None, 'https://realpython.com/introduction-to-python-generators', 'realpython', 'en'),
('art_016', 'Python Context Managers', 'Context managers and with statement in Python', 'article', None, None, 'https://realpython.com/python-with-statement', 'realpython', 'en'),
('art_017', 'Python Exception Handling', 'Error handling and exceptions in Python', 'article', None, None, 'https://realpython.com/python-exceptions', 'realpython', 'en'),
('art_018', 'Python File I/O Tutorial', 'Reading and writing files in Python', 'article', None, None, 'https://realpython.com/read-write-files-python', 'realpython', 'en'),
('art_019', 'Python Regular Expressions', 'Regex in Python with re module', 'article', None, None, 'https://realpython.com/regex-python', 'realpython', 'en'),
('art_020', 'Python List Comprehension', 'Master list comprehension in Python', 'article', None, None, 'https://realpython.com/list-comprehension-python', 'realpython', 'en'),
('art_021', 'Python Pandas Tutorial', 'Complete pandas tutorial for data analysis', 'article', None, None, 'https://pandas.pydata.org/docs/user_guide', 'pandas', 'en'),
('art_022', 'Python NumPy Guide', 'NumPy for numerical computing in Python', 'article', None, None, 'https://numpy.org/doc/stable/user/quickstart', 'numpy', 'en'),
('art_023', 'Python Matplotlib Tutorial', 'Data visualization with matplotlib', 'article', None, None, 'https://matplotlib.org/stable/tutorials', 'matplotlib', 'en'),
('art_024', 'Python Scikit-Learn Guide', 'Machine learning with scikit-learn', 'article', None, None, 'https://scikit-learn.org/stable/user_guide', 'sklearn', 'en'),
('art_025', 'Python Machine Learning Basics', 'Intro to machine learning with Python', 'article', None, None, 'https://realpython.com/python-machine-learning', 'realpython', 'en'),
('art_026', 'Python Deep Learning Intro', 'Deep learning with Python and TensorFlow', 'article', None, None, 'https://www.tensorflow.org/tutorials', 'tensorflow', 'en'),
('art_027', 'Python Neural Networks Guide', 'Building neural networks in Python', 'article', None, None, 'https://keras.io/getting_started', 'keras', 'en'),
('art_028', 'Python Flask Tutorial', 'Build web apps with Flask', 'article', None, None, 'https://flask.palletsprojects.com/en/2.3.x/tutorial', 'flask', 'en'),
('art_029', 'Python Django Tutorial', 'Django web framework tutorial', 'article', None, None, 'https://docs.djangoproject.com/en/stable/intro', 'django', 'en'),
('art_030', 'Python FastAPI Guide', 'Modern Python web framework FastAPI', 'article', None, None, 'https://fastapi.tiangolo.com/tutorial', 'fastapi', 'en'),
('art_031', 'Python API Development', 'Building REST APIs with Python', 'article', None, None, 'https://realpython.com/python-api-development', 'realpython', 'en'),
('art_032', 'Python Web Scraping Guide', 'Web scraping with BeautifulSoup and requests', 'article', None, None, 'https://realpython.com/python-web-scraping', 'realpython', 'en'),
('art_033', 'Python Automation Scripts', 'Automate tasks with Python', 'article', None, None, 'https://realpython.com/python-automation', 'realpython', 'en'),
('art_034', 'Python Testing with Pytest', 'Unit testing in Python with pytest', 'article', None, None, 'https://docs.pytest.org/en/stable/getting-started', 'pytest', 'en'),
('art_035', 'Python Database Tutorial', 'Python with SQLite and PostgreSQL', 'article', None, None, 'https://realpython.com/python-database', 'realpython', 'en'),
('art_036', 'Python SQL Guide', 'SQL queries with Python', 'article', None, None, 'https://realpython.com/python-sql', 'realpython', 'en'),
('art_037', 'Python Virtual Environments', 'Managing Python virtual environments', 'article', None, None, 'https://realpython.com/python-virtual-environments', 'realpython', 'en'),
('art_038', 'Python Pip Package Manager', 'Package management with pip', 'article', None, None, 'https://realpython.com/what-is-pip', 'realpython', 'en'),
('art_039', 'Python Git Tutorial', 'Version control with Git for Python', 'article', None, None, 'https://realpython.com/python-git', 'realpython', 'en'),
('art_040', 'Python Best Practices', 'Python coding standards and best practices', 'article', None, None, 'https://realpython.com/python-best-practices', 'realpython', 'en'),
('art_041', 'Python Performance Optimization', 'Optimize Python code performance', 'article', None, None, 'https://realpython.com/python-performance', 'realpython', 'en'),
('art_042', 'Python Debugging Techniques', 'Debugging Python code effectively', 'article', None, None, 'https://realpython.com/python-debugging', 'realpython', 'en'),
('art_043', 'Python Data Science Roadmap', 'Roadmap to learning data science with Python', 'article', None, None, 'https://realpython.com/python-data-science', 'realpython', 'en'),
('art_044', 'Python NLP with NLTK', 'Natural language processing with NLTK', 'article', None, None, 'https://www.nltk.org/book', 'nltk', 'en'),
('art_045', 'Python Computer Vision OpenCV', 'Computer vision with OpenCV and Python', 'article', None, None, 'https://docs.opencv.org/master', 'opencv', 'en'),
('art_046', 'Python Machine Learning Projects', '10 ML projects for Python beginners', 'article', None, None, 'https://realpython.com/python-ml-projects', 'realpython', 'en'),
('art_047', 'Python Transformers Guide', 'Transformers and attention mechanisms in Python', 'article', None, None, 'https://huggingface.co/course', 'huggingface', 'en'),
('art_048', 'Python LLM Fine Tuning', 'Fine-tuning large language models with Python', 'article', None, None, 'https://huggingface.co/docs/transformers', 'huggingface', 'en'),
('art_049', 'Python MLOps Guide', 'MLOps and production ML with Python', 'article', None, None, 'https://realpython.com/python-mlops', 'realpython', 'en'),
('art_050', 'Python Advanced Topics', 'Advanced Python concepts for experienced developers', 'article', None, None, 'https://realpython.com/python-advanced', 'realpython', 'en')]

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
