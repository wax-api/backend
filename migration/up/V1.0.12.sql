CREATE TABLE tbl_directory (
  id bigint NOT NULL,
  project_id bigint NOT NULL,
  name varchar(200) NOT NULL,
  parent bigint NOT NULL,
  position int NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)