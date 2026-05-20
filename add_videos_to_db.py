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

'''videos = [('vid_001', 'Python for Beginners - Full Course', 'Complete Python tutorial for absolute beginners covering basics to intermediate', 'video', None, None, 'https://youtube.com/watch?v=rfscVS0vtbw', 'youtube', 'en'),
('vid_002', 'Python Tutorial for Beginners 1', 'Python basics introduction tutorial for new programmers', 'video', None, None, 'https://youtube.com/watch?v=_uQrJ0TkZlc', 'youtube', 'en'),
('vid_003', 'Python Tutorial - Python Full Course for Beginners', 'Learn Python programming from scratch in this complete course', 'video', None, None, 'https://youtube.com/watch?v=kqtD5dpn9C8', 'youtube', 'en'),
('vid_004', 'Python Crash Course', 'Quick Python crash course for new programmers learning basics', 'video', None, None, 'https://youtube.com/watch?v=hXE78ekPiss', 'youtube', 'en'),
('vid_005', 'Python Tutorial for Beginners', 'Python programming tutorial covering fundamentals', 'video', None, None, 'https://youtube.com/watch?v=rfscVS0vtbw', 'youtube', 'en'),
('vid_006', 'Python for Data Science - Course for Beginners', 'Learn Python for data science and analysis', 'video', None, None, 'https://youtube.com/watch?v=LHBI6iFg1OY', 'youtube', 'en'),
('vid_007', 'Intermediate Python Programming Course', 'Take your Python skills to the next level', 'video', None, None, 'https://youtube.com/watch?v=Z1Yd7upQsXY', 'youtube', 'en'),
('vid_008', 'Advanced Python Tutorial', 'Advanced Python concepts and techniques', 'video', None, None, 'https://youtube.com/watch?v=JUhIul4CkbE', 'youtube', 'en'),
('vid_009', 'Python Decorators Tutorial', 'Learn Python decorators explained clearly', 'video', None, None, 'https://youtube.com/watch?v=F5mRW0jY4Yc', 'youtube', 'en'),
('vid_010', 'Python OOP Tutorial', 'Object oriented programming in Python', 'video', None, None, 'https://youtube.com/watch?v=BJ-Kv14t33E', 'youtube', 'en')]'''

'''videos=[('vid_011', 'Python Tutorial for Absolute Beginners', 'Complete Python tutorial for absolute beginners with no coding experience', 'video', None, None, 'https://youtube.com/watch?v=rfscVS0vtbw', 'youtube', 'en'),
('vid_012', 'Python Programming Full Course', 'Learn Python programming from scratch with practical examples', 'video', None, None, 'https://youtube.com/watch?v=_uQrJ0TkZlc', 'youtube', 'en'),
('vid_013', 'Learn Python - Full Course for Beginners', 'Free Python course for beginners covering all fundamentals', 'video', None, None, 'https://youtube.com/watch?v=kqtD5dpn9C8', 'youtube', 'en'),
('vid_014', 'Python Course for Beginners', 'Start learning Python with this beginner-friendly course', 'video', None, None, 'https://youtube.com/watch?v=eWRfhZUzrAc', 'youtube', 'en'),
('vid_015', 'Python Basics for Beginners', 'Python basics tutorial covering variables loops functions', 'video', None, None, 'https://youtube.com/watch?v=hXE78ekPiss', 'youtube', 'en'),
('vid_016', 'Python Advanced Tutorial', 'Advanced Python concepts for experienced developers', 'video', None, None, 'https://youtube.com/watch?v=Z1Yd7upQsXY', 'youtube', 'en'),
('vid_017', 'Python for Data Science Full Course', 'Complete data science course using Python and pandas', 'video', None, None, 'https://youtube.com/watch?v=LHBI6iFg1OY', 'youtube', 'en'),
('vid_018', 'Python Machine Learning Tutorial', 'Learn machine learning with Python and scikit-learn', 'video', None, None, 'https://youtube.com/watch?v=N5fT2JvZJ6c', 'youtube', 'en'),
('vid_019', 'Python Pandas Tutorial Full Course', 'Master pandas for data analysis in Python', 'video', None, None, 'https://youtube.com/watch?v=vmEHCJofslg', 'youtube', 'en'),
('vid_020', 'Python NumPy Tutorial for Beginners', 'Learn NumPy for numerical computing in Python', 'video', None, None, 'https://youtube.com/watch?v=qOKmXPU8IN8', 'youtube', 'en'),
('vid_021', 'Python Flask Tutorial Full Course', 'Build web applications with Flask in Python', 'video', None, None, 'https://youtube.com/watch?v=Z1RJmh_OqeA', 'youtube', 'en'),
('vid_022', 'Python Django Tutorial Full Course', 'Learn Django web framework for Python developers', 'video', None, None, 'https://youtube.com/watch?v=rHux0gMZ3Eg', 'youtube', 'en'),
('vid_023', 'Python Deep Learning Tutorial', 'Deep learning with Python TensorFlow and Keras', 'video', None, None, 'https://youtube.com/watch?v=tPYjSzfFJAV', 'youtube', 'en'),
('vid_024', 'Python Testing Tutorial', 'Unit testing and pytest in Python explained', 'video', None, None, 'https://youtube.com/watch?v=6tNS--WepLI', 'youtube', 'en'),
('vid_025', 'Python Best Practices Tutorial', 'Python coding standards and best practices guide', 'video', None, None, 'https://youtube.com/watch?v=jxVtwoySeYM', 'youtube', 'en')]'''

videos = [('vid_026', 'Python Web Scraping Tutorial', 'Learn web scraping with Python BeautifulSoup and requests', 'video', None, None, 'https://youtube.com/watch?v=ng2X945v8IY', 'youtube', 'en'),
('vid_027', 'Python API Tutorial', 'Build APIs with Python FastAPI and RESTful services', 'video', None, None, 'https://youtube.com/watch?v=Gs0gAC4gCDY', 'youtube', 'en'),
('vid_028', 'Python Database Tutorial', 'Connect Python to databases with SQLite and PostgreSQL', 'video', None, None, 'https://youtube.com/watch?v=2TBXU_p3q8U', 'youtube', 'en'),
('vid_029', 'Python Automation Tutorial', 'Automate tasks with Python scripting and scheduling', 'video', None, None, 'https://youtube.com/watch?v=ZFydKWdZfM4', 'youtube', 'en'),
('vid_030', 'Python Regex Tutorial', 'Regular expressions in Python explained with examples', 'video', None, None, 'https://youtube.com/watch?v=K8L6MLKbl4Q', 'youtube', 'en'),
('vid_031', 'Python File Handling Tutorial', 'Read write and manipulate files in Python', 'video', None, None, 'https://youtube.com/watch?v=UlB9s51Yh8I', 'youtube', 'en'),
('vid_032', 'Python Exceptions Tutorial', 'Error handling and exceptions in Python explained', 'video', None, None, 'https://youtube.com/watch?v=Vk9QanM9x0E', 'youtube', 'en'),
('vid_033', 'Python Lambda Functions Tutorial', 'Lambda functions and map filter reduce in Python', 'video', None, None, 'https://youtube.com/watch?v=1KMpriJN1k0', 'youtube', 'en'),
('vid_034', 'Python List Comprehension Tutorial', 'Master list comprehension in Python programming', 'video', None, None, 'https://youtube.com/watch?v=3hP4ypbst7g', 'youtube', 'en'),
('vid_035', 'Python Generators Tutorial', 'Python generators and iterators explained clearly', 'video', None, None, 'https://youtube.com/watch?v=bD05uGo_sVI', 'youtube', 'en'),
('vid_036', 'Python Context Managers Tutorial', 'Context managers and with statement in Python', 'video', None, None, 'https://youtube.com/watch?v=C-sXF8XkUGY', 'youtube', 'en'),
('vid_037', 'Python Iterators Tutorial', 'Iterators and iterables in Python explained', 'video', None, None, 'https://youtube.com/watch?v=9Leyn72qkuY', 'youtube', 'en'),
('vid_038', 'Python Virtual Environments Tutorial', 'Create and manage virtual environments in Python', 'video', None, None, 'https://youtube.com/watch?v=N4mJrT2FD10', 'youtube', 'en'),
('vid_039', 'Python Pip Tutorial', 'Python package manager pip explained with examples', 'video', None, None, 'https://youtube.com/watch?v=GoFhq67v7q0', 'youtube', 'en'),
('vid_040', 'Python Git Tutorial', 'Version control with Git and Python projects', 'video', None, None, 'https://youtube.com/watch?v=SWYqpDaiY_Tc', 'youtube', 'en'),
('vid_041', 'Python Machine Learning Basics', 'Intro to machine learning with Python scikit-learn', 'video', None, None, 'https://youtube.com/watch?v=i_Lw9JtY4gQ', 'youtube', 'en'),
('vid_042', 'Python Neural Networks Tutorial', 'Build neural networks in Python from scratch', 'video', None, None, 'https://youtube.com/watch?v=tPYjSzfFJAV', 'youtube', 'en'),
('vid_043', 'Python Computer Vision Tutorial', 'Computer vision with OpenCV and Python', 'video', None, None, 'https://youtube.com/watch?v=WQGb2CMA38E', 'youtube', 'en'),
('vid_044', 'Python Natural Language Processing', 'NLP with Python NLTK and spaCy libraries', 'video', None, None, 'https://youtube.com/watch?v=801MebkxJ4E', 'youtube', 'en'),
('vid_045', 'Python Data Visualization Tutorial', 'Data visualization with matplotlib seaborn and plotly', 'video', None, None, 'https://youtube.com/watch?v=0h8LT51v8PY', 'youtube', 'en'),
('vid_046', 'Python SQL Tutorial', 'SQL queries and database operations with Python', 'video', None, None, 'https://youtube.com/watch?v=HpA4vAzIqgE', 'youtube', 'en'),
('vid_047', 'Python TestingPytest Tutorial', 'Unit testing with pytest in Python projects', 'video', None, None, 'https://youtube.com/watch?v=osatureJp3c', 'youtube', 'en'),
('vid_048', 'Python Debugging Tutorial', 'Debugging techniques and tools in Python', 'video', None, None, 'https://youtube.com/watch?v=pg-LqOKLu28', 'youtube', 'en'),
('vid_049', 'Python Performance Optimization', 'Optimize Python code for speed and memory', 'video', None, None, 'https://youtube.com/watch?v=vyKl945iSEE', 'youtube', 'en'),
('vid_050', 'Python Project Ideas Tutorial', '10 Python project ideas for beginners to advanced', 'video', None, None, 'https://youtube.com/watch?v=8ext9G7xspg', 'youtube', 'en')]

cur.executemany(
    """
    INSERT INTO resources(id, title, description, resource_type, 
    difficulty_score, difficulty_category, url, source, language)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
    videos
)

conn.commit()

cur.close()
conn.close()

print("DONE!!")

