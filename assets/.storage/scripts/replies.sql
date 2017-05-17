DROP TABLE IF EXISTS `replies`;
CREATE TABLE IF NOT EXISTS `replies` (
  server_id INTEGER NOT NULL,
  input TEXT NOT NULL,
  output TEXT NOT NULL,

  CONSTRAINT PK__server_id__input PRIMARY KEY (server_id, input)
)
