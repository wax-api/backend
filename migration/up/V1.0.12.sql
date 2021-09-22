CREATE TABLE tbl_directory (
  id bigint NOT NULL,
  iid bigint NOT NULL,
  project_id bigint NOT NULL,
  name varchar(200) NOT NULL,
  parent bigint NOT NULL,
  position int NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  UNIQUE (iid, project_id)
)