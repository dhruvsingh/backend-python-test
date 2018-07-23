/*
 values for completed
 0 - Not Done
 1 - Done
*/
ALTER TABLE todos ADD COLUMN completed INTEGER NOT NULL default 0 check (completed = 1 or completed = 0);
