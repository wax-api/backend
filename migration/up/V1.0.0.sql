CREATE TABLE tbl_user (
  id bigint NOT NULL,
  avatar varchar(200),
  truename varchar(100) NOT NULL,
  email varchar(200) NOT NULL UNIQUE,
  team_id bigint NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)