CREATE TABLE tbl_project (
  id bigint NOT NULL,
  team_id bigint NOT NULL,
  name varchar(100) NOT NULL,
  remark text NOT NULL,
  visibility varchar(20) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)