-- SQL Queries to view database tables
-- You can run these in SQLite Browser or Django shell

-- View all categories
SELECT * FROM quiz_app_category;

-- View all quizzes with category names
SELECT 
    q.id,
    q.title,
    c.name as category,
    q.difficulty,
    q.duration,
    q.pass_percentage,
    q.is_active
FROM quiz_app_quiz q
JOIN quiz_app_category c ON q.category_id = c.id;

-- View all questions with quiz names
SELECT 
    qu.id,
    q.title as quiz,
    qu.question_text,
    qu.question_type,
    qu.points
FROM quiz_app_question qu
JOIN quiz_app_quiz q ON qu.quiz_id = q.id;

-- View all answers with question text
SELECT 
    a.id,
    q.question_text,
    a.answer_text,
    a.is_correct
FROM quiz_app_answer a
JOIN quiz_app_question q ON a.question_id = q.id;

-- View all users
SELECT id, username, email, is_staff, is_superuser, date_joined 
FROM auth_user;

-- View quiz results
SELECT 
    r.id,
    u.username,
    q.title as quiz,
    r.score,
    r.total_points,
    r.percentage,
    r.passed,
    r.completed
FROM quiz_app_quizresult r
JOIN auth_user u ON r.user_id = u.id
JOIN quiz_app_quiz q ON r.quiz_id = q.id;

-- Count questions per quiz
SELECT 
    q.title,
    COUNT(qu.id) as question_count
FROM quiz_app_quiz q
LEFT JOIN quiz_app_question qu ON q.id = qu.quiz_id
GROUP BY q.id, q.title;

-- Count answers per question
SELECT 
    q.question_text,
    COUNT(a.id) as answer_count,
    SUM(CASE WHEN a.is_correct = 1 THEN 1 ELSE 0 END) as correct_answers
FROM quiz_app_question q
LEFT JOIN quiz_app_answer a ON q.id = a.question_id
GROUP BY q.id, q.question_text;

-- View all tables in database
SELECT name FROM sqlite_master WHERE type='table';

-- View table structure (schema)
SELECT sql FROM sqlite_master WHERE type='table' AND name='quiz_app_quiz';

