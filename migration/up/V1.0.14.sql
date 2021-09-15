CREATE TABLE tbl_entity (
  id bigint NOT NULL,
  project_id bigint NOT NULL,
  superset_id bigint NOT NULL,
  name varchar(200) NOT NULL,
  create_user_id bigint NOT NULL,
  update_user_id bigint NOT NULL,
  content text NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id)
)