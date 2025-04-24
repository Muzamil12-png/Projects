-- Determine the potential thief by looking for those with suspicious activity.
SELECT name
FROM suspects
WHERE number_of_crimes > 1;  -- Adjust the threshold for previous crimes if necessary.

-- Identify the thief's movements on the date of the crime.
SELECT name, location
FROM movements
WHERE person_id = (SELECT id FROM suspects WHERE name = 'Suspected Thief')
  AND date = '2024-01-01';  -- Ensure the date matches the day of the theft.

-- Investigate connections between the residents to uncover possible accomplices.
SELECT r1.name AS resident, r2.name AS related_person
FROM residents r1
JOIN relationships r2 ON r1.id = r2.person_id
WHERE r1.name = 'Suspected Thief';  -- Replace with the actual suspected thief's name.

-- Analyze any past suspicious activity or criminal history of the suspect.
SELECT name, number_of_crimes
FROM suspects
WHERE name = 'Suspected Thief';  -- Replace with the actual suspect's name.

-- Investigate the thief's escape route and the city they may have fled to.
SELECT name, city
FROM movements
WHERE person_id = (SELECT id FROM suspects WHERE name = 'Suspected Thief')
  AND date BETWEEN '2024-01-01' AND '2024-01-02';  -- Use the correct escape date range.

-- Investigate the potential accomplice who might have helped the thief escape.
SELECT name
FROM people
WHERE id IN (
    SELECT accomplice_id
    FROM escape_plans
    WHERE thief_id = (SELECT id FROM suspects WHERE name = 'Suspected Thief')
);

-- Check for accomplices in the escape plans based on the thief's ID and escape date.
SELECT name
FROM people
WHERE id IN (
    SELECT accomplice_id
    FROM escape_plans
    WHERE thief_id = (SELECT id FROM suspects WHERE name = 'Suspected Thief')
    AND escape_date = '2024-01-01'
);
