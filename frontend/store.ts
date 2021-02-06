import {makeAutoObservable} from 'mobx';
import Project from "./generated/com/overwhale/colibri_so/domain/entity/Project";
import User from "./generated/com/overwhale/colibri_so/domain/entity/User";
import * as ProjectEndpoint from './generated/ProjectEndpoint';
import * as UserEndpoint from './generated/UserEndpoint';
import {getSessionUserId} from "./auth";

class Store {
    private _projects: Project[] = [];
    private _sessionUser: User | undefined;
    private defaultUser: User = {creationTime: undefined, enabled: true, id: undefined, passwordHash: "", username: "undefined"};

    constructor() {
        makeAutoObservable(this);
        this.init();
    }

    async init() {
      this.projects = await ProjectEndpoint.list(0, 10000, []);
      const userId = getSessionUserId();
      if(userId) {
          this.sessionUser = await UserEndpoint.get(userId)!;
      }
    }

    get projects() {
        return this._projects;
    }

    set projects(newProjects: Project[]) {
        this._projects = newProjects;
    }

    get sessionUser() {
        if(this._sessionUser) {
            return this._sessionUser;
        }
        else {
            const userId = getSessionUserId();
            if(userId) {
                UserEndpoint.get(userId).then( user => this.sessionUser = user );
            }
            return this.defaultUser;
        }
    }

    set sessionUser(newUser: User | undefined) {
        this._sessionUser = newUser;
    }

    clearSessionData() {
        this.sessionUser = undefined;
    }
}

export const store = new Store();