DELETE FROM test.contact_types;

INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (1, 'Yes', 'Person 1');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (2, 'Y', 'Person 2');

INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (3, 'by-mail', 'Person 3');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (4, 'no-mail', 'Person 4');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (5, 'No', 'Person 5');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (6, 'N', 'Person 6');

INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (7, 'by-text', 'Person 7');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (8, 'text-only', 'Person 8');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (9, 'No-Text', 'Person 9');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (10, 'mail-only', 'Person 10');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (11, 'unknown', 'Person 11');
	
INSERT INTO test.contact_types(id, emailsubscribed_raw, name)
	VALUES (12, 'other', 'Person 12');