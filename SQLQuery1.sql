-- Step 1: Create the database
CREATE DATABASE recipe_management;
GO

-- Use the newly created database
USE recipe_management;
GO

-- Step 2: Create the `recipes` table
CREATE TABLE recipes (
    id INT IDENTITY(1,1) PRIMARY KEY,       -- Auto-incrementing primary key
    name NVARCHAR(100) UNIQUE NOT NULL,      -- Recipe name, unique and required
    ingredients NVARCHAR(MAX) NOT NULL       -- Ingredients as a comma-separated string
);
GO

-- Step 3: Create the `pantry` table
CREATE TABLE pantry (
    ingredient NVARCHAR(100) UNIQUE NOT NULL -- Ingredient name, unique and required
);
GO

-- Step 4: Insert sample recipes into the `recipes` table
INSERT INTO recipes (name, ingredients) VALUES 
('pancakes', 'flour, eggs, milk, butter, sugar, baking powder'),
('spaghetti bolognese', 'spaghetti, ground beef, tomato sauce, onion, garlic, olive oil'),
('omelette', 'eggs, milk, salt, pepper, cheese'),
('salad', 'lettuce, tomato, cucumber, olive oil, salt, pepper');
GO

-- Step 5: Insert sample pantry items into the `pantry` table
INSERT INTO pantry (ingredient) VALUES 
('flour'),
('eggs'),
('milk'),
('butter'),
('sugar'),
('spaghetti'),
('ground beef'),
('tomato sauce'),
('onion'),
('garlic'),
('olive oil'),
('lettuce'),
('tomato'),
('cucumber'),
('salt'),
('pepper');
GO
