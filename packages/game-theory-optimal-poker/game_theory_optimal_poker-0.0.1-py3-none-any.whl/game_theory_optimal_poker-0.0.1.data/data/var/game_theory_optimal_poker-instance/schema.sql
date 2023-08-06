DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_map;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS hand;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE user_map (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);
INSERT INTO user_map (id, name)
VALUES 
   (0, 'computer'),
   (1, 'user');

CREATE TABLE session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE TABLE hand(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  session_id INTEGER NOT NULL,
  hand_num INTEGER NOT NULL,
  dealer INTEGER NOT NULL,
  winner INTEGER NOT NULL,
  amount_won INTEGER NOT NULL,
  start_money INTEGER NOT NULL,
  user_card1 TEXT NOT NULL,
  user_card2 TEXT NOT NULL,
  computer_card1 TEXT NOT NULL,
  computer_card2 TEXT NOT NULL,
  community_card1 TEXT,
  community_card2 TEXT,
  community_card3 TEXT,
  community_card4 TEXT,
  community_card5 TEXT,
  FOREIGN KEY (session_id) REFERENCES session (id),
  FOREIGN KEY (dealer) REFERENCES user_map (id),
  FOREIGN KEY (winner) REFERENCES user_map (id)
);