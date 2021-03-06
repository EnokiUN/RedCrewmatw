USE redcrewmate;
CREATE TABLE IF NOT EXISTS economy (
	user_id VARCHAR(26) NOT NULL,
	balance INTEGER NOT NULL DEFAULT 0,
	xp INTEGER NOT NULL DEFAULT 0,
	level INTEGER NOT NULL DEFAULT 1,
	PRIMARY KEY (user_id)
);
CREATE TABLE IF NOT EXISTS cooldowns (
	user_id VARCHAR(26) NOT NULL,
	work INTEGER NOT NULL DEFAULT 0,
	beg INTEGER NOT NULL DEFAULT 0,
	search INTEGER NOT NULL DEFAULT 0,
	steal INTEGER NOT NULL DEFAULT 0,
	hourly INTEGER NOT NULL DEFAULT 0,
	daily INTEGER NOT NULL DEFAULT 0,
	FOREIGN KEY (user_id) REFERENCES economy(user_id)
);
