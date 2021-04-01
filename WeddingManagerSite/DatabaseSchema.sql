CREATE TABLE Family(
	family_id VARCHAR(32) PRIMARY KEY,
	family_label VARCHAR(64) UNIQUE NOT NULL,
	invitation_id VARCHAR(32),
	FOREIGN KEY (invitation_id) REFERENCES Invitation(invitation_id)
);

CREATE TABLE Guest(
	guest_id VARCHAR(32) PRIMARY KEY,
	first_name VARCHAR(16) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	relation_en VARCHAR(32),
	FOREIGN KEY (relation_en) REFERENCES Relation(relation_en)
);

CREATE TABLE Relation(
	relation_en VARCHAR(32) PRIMARY KEY,
	relation_mk VARCHAR(32) NOT NULL,
	relation_it VARCHAR(32) NOT NULL
);

CREATE TABLE Invitation(
	invitation_id VARCHAR(32) PRIMARY KEY,
	invitation_sent BOOLEAN DEFAULT FALSE,
	send_date TIMESTAMP,
	invitation_seen BOOLEAN DEFAULT FALSE,
	seen_date TIMESTAMP,
	response VARCHAR(64),
	email_id VARCHAR(32),
	FOREIGN KEY (email_id) REFERENCES Invitation_Email(email_id)
);

CREATE TABLE Invitation_Email(
	email_id VARCHAR(32) PRIMARY KEY,
	to_field VARCHAR(128) NOT NULL,
	cc_field VARCHAR(256),
	from_field VARCHAR(128) NOT NULL,
	subject_field VARCHAR(256) NOT NULL,
	body_field TEXT NOT NULL
);