CREATE TABLE tbl_acl (
  user_id bigint NOT NULL,
  acl text [] NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (user_id)
)