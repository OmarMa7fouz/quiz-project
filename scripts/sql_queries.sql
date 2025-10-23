-- SQL Queries to view database tables
-- You can run these in SQLite Browser or Django shell
--
-- ============================================================================
-- JOIN TYPES IN THIS FILE:
-- ============================================================================
-- 1. EQUIJOIN (Regular JOIN) - Lines 8-77
--    - Joins tables based on equality condition (=)
--    - Examples: quiz JOIN category, question JOIN quiz, etc.
--
-- 2. SELF-JOIN - Lines 84-110
--    - A table joined with itself
--    - Examples: comparing quiz results, finding users who took same quiz
--
-- 3. RECURSIVE QUERIES - Lines 113-168
--    - Uses WITH RECURSIVE clause (Common Table Expressions)
--    - Examples: number sequences, hierarchies, prerequisite chains
-- ============================================================================

-- View all categories
SELECT * FROM quiz_app_category;

-- View all quizzes with category names
-- EQUIJOIN: joining quiz table with category table
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
-- EQUIJOIN: joining question table with quiz table
SELECT 
    qu.id,
    q.title as quiz,
    qu.question_text,
    qu.question_type,
    qu.points
FROM quiz_app_question qu
JOIN quiz_app_quiz q ON qu.quiz_id = q.id;

-- View all answers with question text
-- EQUIJOIN: joining answer table with question table
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
-- EQUIJOIN: joining quiz_result with user and quiz tables
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
-- EQUIJOIN (LEFT JOIN): joining quiz with questions, showing all quizzes even without questions
SELECT 
    q.title,
    COUNT(qu.id) as question_count
FROM quiz_app_quiz q
LEFT JOIN quiz_app_question qu ON q.id = qu.quiz_id
GROUP BY q.id, q.title;

-- Count answers per question
-- EQUIJOIN (LEFT JOIN): joining question with answers, showing all questions even without answers
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


-- ============================================================================
-- SELF-JOIN EXAMPLES (A table joined with itself)
-- ============================================================================

-- Example: Find users who took the same quiz (self-join on quiz_result)
-- This joins the quiz_result table with itself to find pairs of users
SELECT 
    u1.username as user1,
    u2.username as user2,
    q.title as quiz_name
FROM quiz_app_quizresult r1
-- SELF-JOIN: joining quiz_result table with itself
JOIN quiz_app_quizresult r2 ON r1.quiz_id = r2.quiz_id AND r1.user_id < r2.user_id
JOIN auth_user u1 ON r1.user_id = u1.id
JOIN auth_user u2 ON r2.user_id = u2.id
JOIN quiz_app_quiz q ON r1.quiz_id = q.id;


-- Example: Compare user scores on the same quiz (self-join)
SELECT 
    u1.username as user1,
    r1.percentage as score1,
    u2.username as user2,
    r2.percentage as score2,
    q.title as quiz_name
FROM quiz_app_quizresult r1
-- SELF-JOIN: comparing different attempts of the same quiz
JOIN quiz_app_quizresult r2 ON r1.quiz_id = r2.quiz_id AND r1.id < r2.id
JOIN auth_user u1 ON r1.user_id = u1.id
JOIN auth_user u2 ON r2.user_id = u2.id
JOIN quiz_app_quiz q ON r1.quiz_id = q.id;


-- ============================================================================
-- RECURSIVE QUERIES (Using CTEs - Common Table Expressions)
-- Note: SQLite supports recursive CTEs since version 3.8.3
-- ============================================================================

-- Example: Generate a sequence of numbers (recursive CTE)
-- RECURSIVE query that generates numbers from 1 to 10
WITH RECURSIVE number_sequence(n) AS (
    -- Base case: start with 1
    SELECT 1
    UNION ALL
    -- Recursive case: add 1 until we reach 10
    SELECT n + 1 FROM number_sequence WHERE n < 10
)
SELECT n FROM number_sequence;


-- Example: Recursive hierarchy (if categories had parent-child relationships)
-- Note: This is a conceptual example - would need a parent_id field in category table
-- RECURSIVE query to traverse category hierarchy
/*
WITH RECURSIVE category_hierarchy AS (
    -- Base case: get root categories (those without parents)
    SELECT id, name, parent_id, 0 as level
    FROM quiz_app_category
    WHERE parent_id IS NULL
    
    UNION ALL
    
    -- Recursive case: get child categories
    SELECT c.id, c.name, c.parent_id, ch.level + 1
    FROM quiz_app_category c
    JOIN category_hierarchy ch ON c.parent_id = ch.id
)
SELECT * FROM category_hierarchy ORDER BY level, name;
*/


-- Example: Find all prerequisite chains (if quizzes had prerequisites)
-- RECURSIVE query to find quiz dependency chains
/*
WITH RECURSIVE quiz_prerequisites AS (
    -- Base case: quizzes without prerequisites
    SELECT id, title, prerequisite_id, 0 as depth
    FROM quiz_app_quiz
    WHERE prerequisite_id IS NULL
    
    UNION ALL
    
    -- Recursive case: quizzes with prerequisites
    SELECT q.id, q.title, q.prerequisite_id, qp.depth + 1
    FROM quiz_app_quiz q
    JOIN quiz_prerequisites qp ON q.prerequisite_id = qp.id
)
SELECT * FROM quiz_prerequisites ORDER BY depth;
*/
