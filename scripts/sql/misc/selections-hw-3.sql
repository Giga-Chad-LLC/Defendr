/*
Query 1

Description:
    Retrieve infoboxes and their associated field data for the given user ID. For fields with a 'TEXT' type, collect data from the 'text_fields' table, and for fields with a 'SELECTION' type, gather data from the 'selection_fields' table along with their corresponding data from the 'options' table.

    This query will be used to gather account data once a user logged in.

Screenshots:
    See 'scripts/sql/misc/assets/hw3/query-1.png' to view the query output
*/

SELECT
    i.id AS infobox_id,
    i.title AS infobox_title,
    f.id AS field_id,
    f.label AS field_label,
    f.type AS field_type,
    tf.value AS text_field_value,
    o.label AS option_label,
    o.selected AS option_selected
FROM infoboxes i
INNER JOIN fields f ON i.id = f.infobox_id
LEFT JOIN text_fields tf ON f.id = tf.field_id AND f.type = 'TEXT'
LEFT JOIN selection_fields sf ON f.id = sf.field_id AND f.type = 'SELECTION'
LEFT JOIN options o ON sf.id = o.selection_field_id
WHERE i.user_id = /* USER_ID */;



/*

Query 2

Description:
    Count number of service link infoboxes for all users sorted in descending order and limited to the records where the count is greater than zero.

Screenshots:
    See 'scripts/sql/misc/assets/hw3/query-2.png' to view the query output
*/

SELECT
    u.id AS user_id,
    u.email AS user_email,
    COUNT(DISTINCT i.id) AS service_link_infobox_count
FROM users u
LEFT JOIN infoboxes i ON u.id = i.user_id AND i.layout = 'ONLINE_SERVICE'
GROUP BY u.id, u.email
HAVING service_link_infobox_count > 0
ORDER BY service_link_infobox_count DESC;



/*

Query 3

Description:
    Count the number of infoboxes of all users grouped by the infobox layouts and user ids


Screenshots:
    See 'scripts/sql/misc/assets/hw3/query-3.png' to view the query output
*/

SELECT
    u.id AS user_id,
    i.layout AS infobox_layout,
    COUNT(i.id) AS infobox_count
FROM users u
LEFT JOIN infoboxes i ON u.id = i.user_id
GROUP BY u.id, i.layout
ORDER BY user_id, infobox_layout;