CREATE TABLE tbl_mock (
  id bigint NOT NULL,
  project_id bigint NOT NULL,
  interface_id bigint NOT NULL,
  status_code varchar(20) NOT NULL,
  content_type varchar(100) NOT NULL,
  mockjs text NOT NULL,
  content text NOT NULL,
  type varchar(20) NOT NULL,
  headers text NOT NULL,
  active int NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  read_acl text [] NOT NULL,
  write_acl text [] NOT NULL,
  PRIMARY KEY (id)
)