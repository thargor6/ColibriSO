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
values ('43471800-10cd-41ce-9c1e-26fe60814e26', 'academy-cap', '#fce205',
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
INSERT INTO INTENTS (ID, CREATION_TIME, INTENT, DESCRIPTION)
values ('5ed6c8ca-ffc2-482d-b8e2-82cee910067f', '2021-02-22 01:26:17.857762',
        'Documentation', 'Some official documentation');

/* Some default tags */
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('a1586bc2-31f4-4687-89ad-f2b74855af8a', '2021-02-20 01:26:17.857762',
        'Vaadin Fusion');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('fb38878c-7679-4d4a-b445-93b8754de1ab', '2021-02-20 01:26:17.857762',
        'LitElement');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('99857555-7338-438d-a905-0908675237ad', '2021-02-21 01:26:17.857762',
        'Hot peppers');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('324d0cf2-7c3c-4df1-aedd-37bf79ac14a1', '2021-02-21 01:26:17.857762',
        'Weightlifting');
INSERT INTO TAGS (ID, CREATION_TIME, TAG)
values ('b3ab9836-e3ed-4f1b-a624-49cfa8c01e9c', '2021-02-21 01:26:17.857762',
        'Iaido');


/* Some default projects */
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('2e0643dd-9150-4510-9a92-e3288a96561c', '2021-02-20 01:26:17.857762',
        'Software');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('d5c2bb9e-b2cd-4f33-a25b-f0b997fe524d', '2021-02-20 01:26:17.857762',
        'Cool stuff');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('fafe3a1c-6a06-42de-8174-bec06a7e1227', '2021-02-20 01:26:17.857762',
        'Sports');
INSERT INTO PROJECTS (ID, CREATION_TIME, PROJECT)
values ('9df1f06a-5468-40ab-abd9-d5b720a7639a', '2021-02-20 01:26:17.857762',
        'Hobbies');

/* Some Vaadin Fusion related informations */
/* Vaadin Router demos */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('7643bf59-cf3c-4924-a72f-2faeefd4bfa7', 'https://vaadin.github.io/vaadin-router/vaadin-router/demo/#vaadin-router-getting-started-demos', '2021-02-20 01:26:17.857762', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Router demos', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('7643bf59-cf3c-4924-a72f-2faeefd4bfa7', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '7643bf59-cf3c-4924-a72f-2faeefd4bfa7');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('0c2751b2-e892-47ba-a65e-5468382075c7', '7643bf59-cf3c-4924-a72f-2faeefd4bfa7');
/* Online UUID Generator */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('675d33fe-217a-47ec-8658-a05b8abd6050', 'https://www.uuidgenerator.net/', '2021-02-20 01:44:28.873906', 'f2642591-312a-414a-80ab-e13e59b610f9', 'Online UUID Generator', null, null, 'LINK', 1);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('675d33fe-217a-47ec-8658-a05b8abd6050', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '675d33fe-217a-47ec-8658-a05b8abd6050');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('542e443f-95f5-4734-b6e5-74497c9c6026', '675d33fe-217a-47ec-8658-a05b8abd6050');
/* TypeScript Vaadin examples */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('00fe386e-83bc-4627-84b0-b46814fd1911', 'https://vaadin-ts-examples.herokuapp.com/chart-configuration', '2021-02-20 01:55:42.856712', 'f2642591-312a-414a-80ab-e13e59b610f9', ' TypeScript Vaadin examples', null, null, 'LINK', 2);
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
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', '5cf09f3a-ffc5-4917-9af1-e48e6903a43e');
/* Vaadin TypeScript CRM Demo */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('23fd6687-81d3-4c7d-9df7-8e5480d5ee93', 'https://github.com/vaadin-learning-center/crm-tutorial-typescript', '2021-02-20 23:02:25.954225', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Vaadin TypeScript CRM Demo', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('23fd6687-81d3-4c7d-9df7-8e5480d5ee93', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('23fd6687-81d3-4c7d-9df7-8e5480d5ee93', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '23fd6687-81d3-4c7d-9df7-8e5480d5ee93');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('cf8a1901-cb95-430c-83fc-c564e3ca7511', '23fd6687-81d3-4c7d-9df7-8e5480d5ee93');
/* Routing Management with LitElement and TypeScript */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('83a16308-8e3c-4da9-ab35-c0f6a07883c2', 'https://labs.thisdot.co/blog/routing-management-with-litelement', '2021-02-20 23:03:30.629363', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Routing Management with LitElement and TypeScript', null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('83a16308-8e3c-4da9-ab35-c0f6a07883c2', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('83a16308-8e3c-4da9-ab35-c0f6a07883c2', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '83a16308-8e3c-4da9-ab35-c0f6a07883c2');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', '83a16308-8e3c-4da9-ab35-c0f6a07883c2');
/* Colibri SO Repo */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('37a17143-772c-45d2-bee3-d9f854c2bf9e', 'https://github.com/thargor6/ColibriSO', '2021-02-20 23:04:58.868556', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Colibri SO Repo', null, null, 'LINK', 2);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('37a17143-772c-45d2-bee3-d9f854c2bf9e', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('37a17143-772c-45d2-bee3-d9f854c2bf9e', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '37a17143-772c-45d2-bee3-d9f854c2bf9e');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('cf8a1901-cb95-430c-83fc-c564e3ca7511', '37a17143-772c-45d2-bee3-d9f854c2bf9e');
/* Creating forms in LitElement using Vaadin Fusion forms and TypeScript */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('70d15841-c27e-4264-a892-b3681f158abd', 'https://www.youtube.com/watch?v=BAb_awF6xTg&ab_channel=vaadinofficial', '2021-02-20 23:22:03.770879', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Creating forms in LitElement using Vaadin Fusion forms and TypeScript', null, null, 'YOUTUBE');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('70d15841-c27e-4264-a892-b3681f158abd', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('70d15841-c27e-4264-a892-b3681f158abd', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '70d15841-c27e-4264-a892-b3681f158abd');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', '70d15841-c27e-4264-a892-b3681f158abd');
/* HTML properties vs attributes */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('dd16120d-0d44-4060-8659-4314c120f35f', 'https://stackoverflow.com/questions/61490521/litelement-dot-with-html-elements-attribute-property', '2021-02-20 23:22:49.729802', '43471800-10cd-41ce-9c1e-26fe60814e26', 'HTML properties vs attributes', null, null, 'TEXT', 1);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('dd16120d-0d44-4060-8659-4314c120f35f', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', 'dd16120d-0d44-4060-8659-4314c120f35f');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', 'dd16120d-0d44-4060-8659-4314c120f35f');
/* Introducing Vaadin Flow and Fusion */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('328e1649-602a-4bf3-9613-52c50e5e6327', 'https://vaadin.com/blog/reintroducing-vaadin-flow-and-fusion', '2021-02-20 23:23:28.147202', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Introducing Vaadin Flow and Fusion', null, null, 'LINK', 2);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('328e1649-602a-4bf3-9613-52c50e5e6327', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('328e1649-602a-4bf3-9613-52c50e5e6327', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '328e1649-602a-4bf3-9613-52c50e5e6327');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', '328e1649-602a-4bf3-9613-52c50e5e6327');
/* 7 Pot Club */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('b8ec3100-5f8f-4c52-b961-e0e7d7d7db3b', 'https://www.youtube.com/channel/UCMKH_yo-lhyCdj4fJlQnYjQ', '2021-02-21 00:17:36.756369', '43471800-10cd-41ce-9c1e-26fe60814e26', '7 Pot Club', null, null, null, 'LINK', 3);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('b8ec3100-5f8f-4c52-b961-e0e7d7d7db3b', '99857555-7338-438d-a905-0908675237ad');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('d5c2bb9e-b2cd-4f33-a25b-f0b997fe524d', 'b8ec3100-5f8f-4c52-b961-e0e7d7d7db3b');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', 'b8ec3100-5f8f-4c52-b961-e0e7d7d7db3b');
/* Strength Level */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE, FAVOURITE_LEVEL)
VALUES ('12b06c6c-965a-437e-8415-96a000e8187b', 'https://strengthlevel.com/', '2021-02-21 00:18:17.680300', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Strength Level', null, null, null, 'LINK', 1);
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('12b06c6c-965a-437e-8415-96a000e8187b', '324d0cf2-7c3c-4df1-aedd-37bf79ac14a1');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('fafe3a1c-6a06-42de-8174-bec06a7e1227', '12b06c6c-965a-437e-8415-96a000e8187b');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('542e443f-95f5-4734-b6e5-74497c9c6026', '12b06c6c-965a-437e-8415-96a000e8187b');
/* Iaido Katas (German) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, FAVOURITE_LEVEL, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('48d7d546-5786-4302-bbda-7216845827e0', 'https://www.shoushikai.de/iaido/die-formen/', '2021-02-21 00:19:19.977471', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Iaido Katas (German)', null, null, null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('48d7d546-5786-4302-bbda-7216845827e0', 'b3ab9836-e3ed-4f1b-a624-49cfa8c01e9c');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('fafe3a1c-6a06-42de-8174-bec06a7e1227', '48d7d546-5786-4302-bbda-7216845827e0');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', '48d7d546-5786-4302-bbda-7216845827e0');
/* Drone pilot's license (German) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, FAVOURITE_LEVEL, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('164b0a66-6ac8-4a58-bf19-37443e58c712', 'https://lba-openuav.de/', '2021-02-21 00:23:14.252395', '43471800-10cd-41ce-9c1e-26fe60814e26', 'Drone pilot''s license (German)', null, null, null, null, 'LINK');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('9df1f06a-5468-40ab-abd9-d5b720a7639a', '164b0a66-6ac8-4a58-bf19-37443e58c712');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('4ffcd7b6-190a-4631-ad52-c7d63cd1b789', '164b0a66-6ac8-4a58-bf19-37443e58c712');
/* Vaadin Fusion Docs (Beta) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, FAVOURITE_LEVEL, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('288c3f3b-3f12-4fbe-8a44-10624fdc5359', 'https://vaadin.com/docs-beta/latest/fusion/overview/', '2021-02-22 21:32:28.743720', 'f2642591-312a-414a-80ab-e13e59b610f9', 'Vaadin Fusion Docs (Beta)', null, null, null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('288c3f3b-3f12-4fbe-8a44-10624fdc5359', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '288c3f3b-3f12-4fbe-8a44-10624fdc5359');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5ed6c8ca-ffc2-482d-b8e2-82cee910067f', '288c3f3b-3f12-4fbe-8a44-10624fdc5359');
/* LitElement documentation */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, FAVOURITE_LEVEL, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('76c4cc8b-7101-4af4-b7d9-9512e7f949b8', 'https://lit-element.polymer-project.org/guide', '2021-02-22 21:35:16.669947', 'f2642591-312a-414a-80ab-e13e59b610f9', 'LitElement documentation', null, null, null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('76c4cc8b-7101-4af4-b7d9-9512e7f949b8', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '76c4cc8b-7101-4af4-b7d9-9512e7f949b8');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5ed6c8ca-ffc2-482d-b8e2-82cee910067f', '76c4cc8b-7101-4af4-b7d9-9512e7f949b8');
/* lit-translate (i18n) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, FAVOURITE_LEVEL, ICON, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('3774f5b1-d9f2-4db8-b5dd-311ce66785b3', 'https://github.com/andreasbm/lit-translate', '2021-02-22 21:35:54.268255', 'f2642591-312a-414a-80ab-e13e59b610f9', 'lit-translate (i18n)', null, null, null, null, 'LINK');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('3774f5b1-d9f2-4db8-b5dd-311ce66785b3', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', '3774f5b1-d9f2-4db8-b5dd-311ce66785b3');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('cf8a1901-cb95-430c-83fc-c564e3ca7511', '3774f5b1-d9f2-4db8-b5dd-311ce66785b3');
/* Type-safe server access from TypeScript to Java (REST made easy) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('f3f534af-5aab-48ce-acb0-c6f1774b242f', 'https://www.youtube.com/watch?v=l8tw9F728tg&ab_channel=vaadinofficial', '2021-02-22 02:01:48.680601', 'f2642591-312a-414a-80ab-e13e59b610f9', 'Type-safe server access from TypeScript to Java (REST made easy)', null, null, 'YOUTUBE');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('f3f534af-5aab-48ce-acb0-c6f1774b242f', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('f3f534af-5aab-48ce-acb0-c6f1774b242f', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', 'f3f534af-5aab-48ce-acb0-c6f1774b242f');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', 'f3f534af-5aab-48ce-acb0-c6f1774b242f');
/* Type-safe server access from TypeScript to Java (REST made easy) */
INSERT INTO SNIPPETS (ID, CONTENT, CREATION_TIME, CREATOR_ID, DESCRIPTION, LAST_CHANGED_TIME, MIMETYPE, SNIPPET_TYPE)
VALUES ('c1ebe0d3-a876-4dbf-b439-ee659fa093eb', 'https://www.youtube.com/watch?v=F3y5E9YVtsk&ab_channel=vaadinofficial', '2021-03-01 20:01:48.680601', 'f2642591-312a-414a-80ab-e13e59b610f9', 'LitElement 3.0 & lit-html 2.0, what''s new and exciting?', null, null, 'YOUTUBE');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('c1ebe0d3-a876-4dbf-b439-ee659fa093eb', 'a1586bc2-31f4-4687-89ad-f2b74855af8a');
INSERT INTO SNIPPET_TAGS (SNIPPET_ID, TAG_ID) VALUES ('c1ebe0d3-a876-4dbf-b439-ee659fa093eb', 'fb38878c-7679-4d4a-b445-93b8754de1ab');
INSERT INTO SNIPPET_PROJECTS (PROJECT_ID, SNIPPET_ID) VALUES ('2e0643dd-9150-4510-9a92-e3288a96561c', 'c1ebe0d3-a876-4dbf-b439-ee659fa093eb');
INSERT INTO SNIPPET_INTENTS (INTENT_ID, SNIPPET_ID) VALUES ('5d00a2ef-7382-43a6-ac73-626f80b4902b', 'c1ebe0d3-a876-4dbf-b439-ee659fa093eb');


