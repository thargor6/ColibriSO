import {makeAutoObservable} from 'mobx';
import Project from "./generated/com/overwhale/colibri_so/domain/entity/Project";
import User from "./generated/com/overwhale/colibri_so/domain/entity/User";
import * as ProjectEndpoint from './generated/ProjectEndpoint';
import * as UserEndpoint from './generated/UserEndpoint';
import * as UserDetailEndpoint from './generated/UserDetailEndpoint';
import {getSessionUserId} from "./auth";
import UserDetail from "./generated/com/overwhale/colibri_so/domain/entity/UserDetail";

class Store {
    private static _instance:Store = new Store();

    private _projects: Project[] = [];
    private _sessionUser: User = {
        creationTime: undefined,
        enabled: false,
        id: undefined,
        passwordHash: "",
        username: ""
    };
    private _sessionUserDetail: UserDetail = {creationTime: undefined, userId: undefined};

    constructor() {
        if(Store._instance){
            throw new Error("Error: Instantiation failed: Use Store.getInstance() instead of new.");
        }
        Store._instance = this;

        makeAutoObservable(this);
        this.init();
    }

    public static getInstance():Store
    {
        return Store._instance;
    }

    async init() {
      this.projects = await ProjectEndpoint.list(0, 10000, []);
      const userId = getSessionUserId();
      if(userId) {
          const sessionUser = await UserEndpoint.get(userId);
          if(sessionUser) {
              this.sessionUser = sessionUser;
          }
          const sessionUserDetail = await UserDetailEndpoint.get(userId);
          if(sessionUserDetail) {
              this.sessionUserDetail = sessionUserDetail;
          }
      }
    }

    get projects() {
        return this._projects;
    }

    set projects(newProjects: Project[]) {
        this._projects = newProjects;
    }

    get sessionUser() {
            return this._sessionUser;
    }

    set sessionUser(newUser: User) {
        this._sessionUser = newUser;
    }

    set sessionUserDetail(newUserDetail: UserDetail) {
        this._sessionUserDetail = newUserDetail;
    }

    get sessionUserDetail() {
            return this._sessionUserDetail;
    }

    clearSessionData() {
        this.sessionUser = {creationTime: undefined, enabled: false, id: undefined, passwordHash: "", username: ""};
        this.sessionUserDetail = {creationTime: undefined, userId: undefined};
    }
}

export const store = Store.getInstance();