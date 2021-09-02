CREATE TABLE tbl_auth (
  user_id bigint NOT NULL,
  password VARCHAR(100) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (user_id)
)