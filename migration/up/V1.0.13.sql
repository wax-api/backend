CREATE TABLE tbl_interface (
  id bigint NOT NULL,
  iid bigint NOT NULL,
  project_id bigint NOT NULL,
  directory_iid bigint NOT NULL,
  name varchar(200) NOT NULL,
  method varchar(10) NOT NULL,
  path varchar(200) NOT NULL,
  status varchar(20) NOT NULL,
  create_user_id bigint NOT NULL,
  update_user_id bigint NOT NULL,
  endpoint text NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  UNIQUE (iid, project_id)
)