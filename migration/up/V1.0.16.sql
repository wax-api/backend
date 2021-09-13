CREATE TABLE tbl_api_acl (
  id bigint NOT NULL,
  method varchar(20) NOT NULL,
  path varchar(255) NOT NULL,
  acl text [] NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  UNIQUE (method, path)
)