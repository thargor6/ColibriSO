/* user "admin" with password "colibri42" */
INSERT INTO USERS (ID, USERNAME, ENABLED, PASSWORD_HASH, CREATION_TIME)
  values ('f2642591-312a-414a-80ab-e13e59b610f9', 'admin', 1,
          '$2y$12$sE1zfriusl2MWpVsqcvR7ewUiJ2xqS0776AZS4oGFUQ6sCSgH5Mgu',
          parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'));

insert INTO USER_DETAILS (USER_ID, AVATAR, AVATAR_COLOR, CREATION_TIME, EMAIL, FULL_NAME, UI_THEME)
values ('f2642591-312a-414a-80ab-e13e59b610f9', 'cubes', '#c21807',
        parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'admin@colibriso.com', 'Admin', 'dark');

INSERT INTO AUTHORITIES (ID, AUTHORITY)
  values ('00030e6c-8daf-40c7-9793-875c17db93c5', 'ADMIN');

INSERT INTO AUTHORITIES (ID, AUTHORITY)
  values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', 'USER');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
  values ('00030e6c-8daf-40c7-9793-875c17db93c5', 'f2642591-312a-414a-80ab-e13e59b610f9');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
  values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', 'f2642591-312a-414a-80ab-e13e59b610f9');

/* user "user" with password "colibri42" */
INSERT INTO USERS (ID, USERNAME, ENABLED, PASSWORD_HASH, CREATION_TIME)
values ('43471800-10cd-41ce-9c1e-26fe60814e26', 'user', 1,
        '$2y$12$Aa7VN/csWw/Doqv4k9Nh0ezZmfaw843kabQv/M5Xtnit9s1vor.TK',
        parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'));

insert INTO USER_DETAILS (USER_ID, AVATAR, AVATAR_COLOR, CREATION_TIME, EMAIL, FULL_NAME, UI_THEME)
values ('43471800-10cd-41ce-9c1e-26fe60814e26', 'academy-cap', '#57a0d2',
        parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'user@colibriso.com', 'Some User', 'light');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', '43471800-10cd-41ce-9c1e-26fe60814e26');

/* Some default intents */

INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('ebb5ad46-a012-46a1-8c60-f6723f0e515b', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
       'Link', 'An link to some external resource');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Text', 'Some small text snippet');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('16825535-2ef7-4bda-a827-400570316cc4', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'PDF', 'A pdf document');

/* Some default tags */
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('72263db0-d6e7-46b2-b136-9237fe745540', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Scientific Paper');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('38a1d9b6-e3a4-47a9-82d3-e8eaf486ddf1', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Book');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('305901ba-8bb7-4e38-9bec-2fe81dd87234', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Article');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('20e5571f-81e6-4f4e-ba0e-cd0e47b2e0ba', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Recipe');


/* Some default projects */
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('2e0643dd-9150-4510-9a92-e3288a96561c', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Software');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('d5c2bb9e-b2cd-4f33-a25b-f0b997fe524d', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Cooking');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('fafe3a1c-6a06-42de-8174-bec06a7e1227', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Sports');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('9df1f06a-5468-40ab-abd9-d5b720a7639a', parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'),
        'Household');

