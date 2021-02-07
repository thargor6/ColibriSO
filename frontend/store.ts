import {makeAutoObservable} from 'mobx';
import Project from "./generated/com/overwhale/colibri_so/domain/entity/Project";
import User from "./generated/com/overwhale/colibri_so/domain/entity/User";
import * as ProjectEndpoint from './generated/ProjectEndpoint';
import * as UserEndpoint from './generated/UserEndpoint';
import * as UserDetailEndpoint from './generated/UserDetailEndpoint';
import {getSessionUserId} from "./auth";
import UserDetail from "./generated/com/overwhale/colibri_so/domain/entity/UserDetail";

export class Store {
    private static _instance:Store = new Store();

    private _projects: Project[] = [];
    private _sessionUser: User | undefined;
    private _sessionUserDetail: UserDetail | undefined;

    constructor() {
        if(Store._instance){
            throw new Error("Error: Instantiation failed: Use Store.getInstance() instead of new.");
        }
        Store._instance = this;
        console.log('STORE construct');
        makeAutoObservable(this);
        this.init();
    }

    public static getInstance():Store
    {
        return Store._instance;
    }

    async init() {
        console.log('STORE INIT');
      this.projects = await ProjectEndpoint.list(0, 10000, []);
      const userId = getSessionUserId();
      if(userId) {

          this.sessionUser = await UserEndpoint.get(userId)!;
          console.log('LOADED USER '+this.sessionUser);
          this.sessionUserDetail = await UserDetailEndpoint.get(userId);
          console.log('LOADED USER DEATAIL '+this.sessionUserDetail);
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

    set sessionUser(newUser: User | undefined) {
        this._sessionUser = newUser;
    }

    set sessionUserDetail(newUserDetail: UserDetail | undefined) {
        this._sessionUserDetail = newUserDetail;
    }

    get sessionUserDetail() {
            return this._sessionUserDetail;
    }

    clearSessionData() {
        console.log('CLEAR SESSION DATA')
        this.sessionUser = undefined;
        this.sessionUserDetail = undefined;
    }
}