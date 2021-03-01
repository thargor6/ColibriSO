# ColibriSO
Colibri Snippet Organizer

## Description
ColibriSO is a tool for organizing information-bits of all kinds. The application is based on Spring Boot and Vaadin Fusion.

Currently, it is work-in-progress and not much more than a playground.

### What is implemented so far
 + basic CRUD for Projects, Tags and Intents
 + basic editing of snippets
 + basic snippet display (table)
 + basic user handling
 + basic user settings  
 + spring security (jdbc implementation)  
 + both in-memory state (e.g. for projects) and paging larger data (e.g. snippets)  
 + MobX for state management
 + flat Project-"tree" (only one hierarchy)
 + "self-contained" examples (informations and tutorials for Vaadin Fusion and LitElement)
### TODO's
 + fine-tune dto's for editing and validation, and entities for the backend, clean up annotations (json, jpa)
 + inline display of pdf documents
 + implements intents (e.g. reminders)
 + search function
 + upload documents
 + user registration (email)
 + roles and permissions
 + ...
## Project

The project is a standard Maven project, so you can import it to your IDE of choice. 
You'll need to have Java 8+ and Node.js 10+ installed.

To run from the command line, use `mvn` and open [http://localhost:8080](http://localhost:8080) in your browser.

### Project structure

| Directory                                  | Description                                                                                                                 |
| :----------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `frontend/`                                | Client-side source directory                                                                                                |
| &nbsp;&nbsp;&nbsp;&nbsp;`index.html`       | HTML template                                                                                                               |
| &nbsp;&nbsp;&nbsp;&nbsp;`index.ts`         | Frontend entrypoint, contains the client-side routing setup using [Vaadin Router](https://vaadin.com/router)                |
| &nbsp;&nbsp;&nbsp;&nbsp;`main-layout.ts`   | Main layout Web Component, contains the navigation menu, uses [App Layout](https://vaadin.com/components/vaadin-app-layout) |
| &nbsp;&nbsp;&nbsp;&nbsp;`views/`           | UI views Web Components (TypeScript)                                                                                        |
| &nbsp;&nbsp;&nbsp;&nbsp;`styles/`          | Styles directory (CSS)                                                                                                      |
| `src/main/java/<groupId>/`                 | Server-side source directory, contains the server-side Java views                                                           |
| &nbsp;&nbsp;&nbsp;&nbsp;`Application.java` | Server entrypoint                                                                                                           |
