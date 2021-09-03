CREATE TABLE tbl_project (
  id bigint NOT NULL,
  name varchar(100) NOT NULL,
  remark text NOT NULL,
  visibility varchar(20) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (id)
)