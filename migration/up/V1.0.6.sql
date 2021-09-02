CREATE TABLE tbl_team (
  id bigint NOT NULL,
  name VARCHAR(200) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)