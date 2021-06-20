CREATE TABLE Group(
	/*ID for the group*/
	group_id VARCHAR(32) PRIMARY KEY,
	/*Identifying label*/
	group_label VARCHAR(64) UNIQUE NOT NULL,
	/*The primary contact for the group*/
	primary_contact VARCHAR(32),
	FOREIGN KEY (primary_contact) REFERENCES Guest(guest_id)
);

CREATE TABLE Guest(
	/*Unique Identifier*/
	guest_id VARCHAR(32) PRIMARY KEY,
	first_name VARCHAR(16) NOT NULL,
	last_name VARCHAR(32) NOT NULL,
	/*Relationship*/
	relation_en VARCHAR(32),
	whose_guest VARCHAR(8) NOT NULL,
	home_address VARCHAR(128),
	phone_number VARCHAR(16),
	email VARCHAR(64),
	fb_link VARCHAR(256),
	/*If invited_as_group is TRUE, this is a reference to the group theyre a part of.*/
	group_id VARCHAR (32),
	/*States whether this person is overseas*/
	is_overseas BOOLEAN DEFAULT FALSE,
	/*Invitation this guest is associated with.*/
	invitation_id VARCHAR(32),
	/*Determines if the user has responded yet. True = Yes, False = No, Null = No response.*/
	is_attending BOOLEAN,
	FOREIGN KEY (relation_en) REFERENCES Guest_Relation(relation_en),
	FOREIGN KEY (group_id) REFERENCES Group(group_id),
	FOREIGN KEY (invitation_id) REFERENCES Invitation(invitation_id)
);

CREATE TABLE Guest_Relation(
	relation_en VARCHAR(32) PRIMARY KEY,
	relation_mk VARCHAR(32) NOT NULL,
	relation_it VARCHAR(32) NOT NULL
);

CREATE TABLE Invitation(
	/*Uniquely identifies each row*/
	invitation_id VARCHAR(32) PRIMARY KEY,
	/*The ID used in the URL in the invitation email*/
	invitation_url_id VARCHAR(32) UNIQUE NOT NULL,
	/*States whether the invitation has been sent already.*/
	invitation_sent BOOLEAN DEFAULT FALSE,
	/*Date + time sent*/
	send_date TIMESTAMP,
	/*States whether the invitation link has been clicked already*/
	invitation_seen BOOLEAN DEFAULT FALSE,
	/*The most recent date the link has been clicked*/
	seen_date TIMESTAMP,
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

CREATE TABLE RSVP_Food(
	guest_id VARCHAR(32) Primary Key,
	vegan_selected BOOLEAN,
	vegetarian_selected BOOLEAN,
	halal_selected BOOLEAN,
	allergy_description TEXT,
	other_description TEXT,
	FOREIGN KEY (guest_id) REFERENCES Guest(guest_id)
);