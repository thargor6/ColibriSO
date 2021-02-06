INSERT INTO USERS (ID, USERNAME, ENABLED, PASSWORD_HASH, CREATION_TIME)
  values ('f2642591-312a-414a-80ab-e13e59b610f9', 'admin', 1,
          '$2y$12$PGO..za3LBKShGQ2gQ2QcOaVHrBqB5kBe2eIkJnohGS9NyQqf2PQ6',
          parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'));

INSERT INTO AUTHORITIES (ID, AUTHORITY)
  values ('00030e6c-8daf-40c7-9793-875c17db93c5', 'ADMIN');

INSERT INTO AUTHORITIES (ID, AUTHORITY)
  values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', 'USER');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
  values ('00030e6c-8daf-40c7-9793-875c17db93c5', 'f2642591-312a-414a-80ab-e13e59b610f9');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
  values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', 'f2642591-312a-414a-80ab-e13e59b610f9');

INSERT INTO USERS (ID, USERNAME, ENABLED, PASSWORD_HASH, CREATION_TIME)
values ('43471800-10cd-41ce-9c1e-26fe60814e26', 'user', 1,
        '$2y$12$o3coSv41C4QXMAUpDyWErOY2nZN95HPoMdjgOPMaD0uda7JaFoJ2a',
        parsedatetime('06-02-2021 18:00:00.00', 'dd-MM-yyyy hh:mm:ss.SS'));

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', '43471800-10cd-41ce-9c1e-26fe60814e26');

// password is always "password"


ebb5ad46-a012-46a1-8c60-f6723f0e515b
4ffcd7b6-190a-4631-ad52-c7d63cd1b789
16825535-2ef7-4bda-a827-400570316cc4