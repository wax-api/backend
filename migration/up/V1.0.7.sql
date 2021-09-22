INSERT INTO tbl_api_acl(id, method, path, acl)
VALUES (1, 'POST', '/login', '{"G", "U/*"}'),
(2, 'GET', '/app/me', '{"U/*"}'),
(3, 'POST', '/app/team', '{"U/*"}')
