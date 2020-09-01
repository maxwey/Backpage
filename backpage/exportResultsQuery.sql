.mode csv
.headers ON

SELECT
    t.timestamp as 'Action Timestamp (UTC)',
    u.name as 'User Display Name',
    ru.user_name as 'Username',
    t.action as 'User Action',
    t.content as 'User Action Content',
    p.id as 'Post ID',
    p.create_date as 'Post Create Date (UTC)',
    p.author_id as 'Post Author ID',
    pu.name as 'Post Author Name',
    p.text as 'Post Text'
FROM
    feed_postinteractiontracker as t
    INNER JOIN feed_user as u ON u.id = t.user_id
    INNER JOIN feed_post as p ON p.id = t.post_id
    INNER JOIN feed_realuser as ru ON ru.user_ptr_id = u.id
    INNER JOIN feed_user as pu ON p.author_id = pu.id;
