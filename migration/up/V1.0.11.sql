CREATE TABLE tbl_project_user (
  id bigint NOT NULL,
  project_id bigint NOT NULL,
  user_id bigint NOT NULL,
  role varchar(20) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id),
  UNIQUE (project_id, user_id)
)