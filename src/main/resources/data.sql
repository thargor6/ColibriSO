/* user "admin" with password "colibri42" */
INSERT INTO USERS (ID, USERNAME, ENABLED, PASSWORD_HASH, CREATION_TIME)
  values ('f2642591-312a-414a-80ab-e13e59b610f9', 'admin', 1,
          '$2y$12$sE1zfriusl2MWpVsqcvR7ewUiJ2xqS0776AZS4oGFUQ6sCSgH5Mgu',
          '2021-02-20 01:26:17.857762');

insert INTO USER_DETAILS (USER_ID, AVATAR, AVATAR_COLOR, CREATION_TIME, EMAIL, FULL_NAME, UI_THEME)
values ('f2642591-312a-414a-80ab-e13e59b610f9', 'cubes', '#c21807',
        '2021-02-20 01:26:17.857762',
        'admin@colibriso.com', 'Admin', 'light');

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
        '2021-02-20 01:26:17.857762');

insert INTO USER_DETAILS (USER_ID, AVATAR, AVATAR_COLOR, CREATION_TIME, EMAIL, FULL_NAME, UI_THEME)
values ('43471800-10cd-41ce-9c1e-26fe60814e26', 'academy-cap', '#57a0d2',
        '2021-02-20 01:26:17.857762',
        'user@colibriso.com', 'Some User', 'light');

INSERT INTO USER_AUTHORITIES (AUTHORITY_ID, USER_ID)
values ('bbd7b226-d1d3-4f00-afbe-d9979871417e', '43471800-10cd-41ce-9c1e-26fe60814e26');

/* Some default intents */

INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('ebb5ad46-a012-46a1-8c60-f6723f0e515b', '2021-02-20 01:26:17.857762',
       'Reminder', 'A little reminder');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', '2021-02-20 01:26:17.857762',
        'Information', 'Some bit of information');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('16825535-2ef7-4bda-a827-400570316cc4', '2021-02-20 01:26:17.857762',
        'Note', 'A small note');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('0c2751b2-e892-47ba-a65e-5468382075c7', '2021-02-20 01:26:17.857762',
        'Example', 'An example');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('cf8a1901-cb95-430c-83fc-c564e3ca7511', '2021-02-20 01:26:17.857762',
        'Github Repo', 'An external repo');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('542e443f-95f5-4734-b6e5-74497c9c6026', '2021-02-20 01:26:17.857762',
        'Tool', 'Some useful tool');
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('5d00a2ef-7382-43a6-ac73-626f80b4902b', '2021-02-20 01:26:17.857762',
        'Tutorial', 'Some tutorial');

/* Some default tags */
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('a1586bc2-31f4-4687-89ad-f2b74855af8a', '2021-02-20 01:26:17.857762',
        'Vaadin Fusion');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('fb38878c-7679-4d4a-b445-93b8754de1ab', '2021-02-20 01:26:17.857762',
        'LitElement');

/* Some default projects */
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('2e0643dd-9150-4510-9a92-e3288a96561c', '2021-02-20 01:26:17.857762',
        'Software');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('d5c2bb9e-b2cd-4f33-a25b-f0b997fe524d', '2021-02-20 01:26:17.857762',
        'Cooking');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('fafe3a1c-6a06-42de-8174-bec06a7e1227', '2021-02-20 01:26:17.857762',
        'Sports');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('9df1f06a-5468-40ab-abd9-d5b720a7639a', '2021-02-20 01:26:17.857762',
        'Household');

/* Some Vaadin Fusion related informations */
/* Vaadin Router demos */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('7643bf59-cf3c-4924-a72f-2faeefd4bfa7', 'https://vaadin.github.io/vaadin-router/vaadin-router/demo/#vaadin-router-getting-started-demos', '2021-02-20 01:26:17.857762', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Router demos', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('7643bf59-cf3c-4924-a72f-2faeefd4bfa7', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '7643bf59-cf3c-4924-a72f-2faeefd4bfa7');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('0c2751b2-e892-47ba-a65e-5468382075c7', '7643bf59-cf3c-4924-a72f-2faeefd4bfa7');
/* Online UUID Generator */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('675d33fe-217a-47ec-8658-a05b8abd6050', 'https://www.uuidgenerator.net/', '2021-02-20 01:44:28.873906', 'f2642591-312a-414a-80ab-e13e59b610f9', 'Online UUID Generator', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('675d33fe-217a-47ec-8658-a05b8abd6050', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '675d33fe-217a-47ec-8658-a05b8abd6050');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('542e443f-95f5-4734-b6e5-74497c9c6026', '675d33fe-217a-47ec-8658-a05b8abd6050');
/* TypeScript Vaadin examples */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('00fe386e-83bc-4627-84b0-b46814fd1911', 'https://vaadin-ts-examples.herokuapp.com/chart-configuration', '2021-02-20 01:55:42.856712', 'f2642591-312a-414a-80ab-e13e59b610f9', ' TypeScript Vaadin examples', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('00fe386e-83bc-4627-84b0-b46814fd1911', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('00fe386e-83bc-4627-84b0-b46814fd1911', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '00fe386e-83bc-4627-84b0-b46814fd1911');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('0c2751b2-e892-47ba-a65e-5468382075c7', '00fe386e-83bc-4627-84b0-b46814fd1911');
/* LitElement state management with MobX in a Vaadin Fusion project */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('5cf09f3a-ffc5-4917-9af1-e48e6903a43e', 'https://www.youtube.com/watch?v=MNxnZ8pzSBo&ab_channel=vaadinofficial', '2021-02-20 02:01:48.680601', 'f2642591-312a-414a-80ab-e13e59b610f9', 'LitElement state management with MobX in a Vaadin Fusion project', null, null, 'YOUTUBE');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('5cf09f3a-ffc5-4917-9af1-e48e6903a43e', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('5cf09f3a-ffc5-4917-9af1-e48e6903a43e', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '5cf09f3a-ffc5-4917-9af1-e48e6903a43e');
INSERT INTO PUBLIC.SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', '5cf09f3a-ffc5-4917-9af1-e48e6903a43e');

