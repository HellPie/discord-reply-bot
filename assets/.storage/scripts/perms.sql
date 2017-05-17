DROP TABLE IF EXISTS `perms`;
CREATE TABLE IF NOT EXISTS `perms` (
  server_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL,
  perm INTEGER,

  CONSTRAINT PK__server_id__role_id PRIMARY KEY (server_id, role_id)
)
