import {computed, observable} from 'mobx';
import Project from "./generated/com/overwhale/colibri_so/domain/entity/Project";
import User from "./generated/com/overwhale/colibri_so/domain/entity/User";
import * as ProjectEndpoint from './generated/ProjectEndpoint';
import * as IntentEndpoint from './generated/IntentEndpoint';
import * as TagEndpoint from './generated/TagEndpoint';
import * as UserEndpoint from './generated/UserEndpoint';
import * as UserDetailEndpoint from './generated/UserDetailEndpoint';
import {getSessionUserId} from "./auth";
import UserDetail from "./generated/com/overwhale/colibri_so/domain/entity/UserDetail";
import Intent from "./generated/com/overwhale/colibri_so/domain/entity/Intent";
import Tag from "./generated/com/overwhale/colibri_so/domain/entity/Tag";

class Store {
    private static _instance:Store = new Store();

    @observable
    private _projects: Project[] = [];

    @observable
    private _intents: Intent[] = [];

    @observable
    private _tags: Tag[] = [];

    @observable
    private _sessionUser: User = {
        creationTime: undefined,
        enabled: false,
        id: undefined,
        passwordHash: "",
        username: ""
    };

    @observable
    private _sessionUserDetail: UserDetail = {creationTime: undefined, userId: undefined};

    constructor() {
        if(Store._instance){
            throw new Error("Error: Instantiation failed: Use Store.getInstance() instead of new.");
        }
        Store._instance = this;

       // makeAutoObservable(this);
        this.init();
    }

    public static getInstance():Store
    {
        return Store._instance;
    }

    async init() {
      this.projects = await ProjectEndpoint.list(0, 10000, []);
      this.intents = await IntentEndpoint.list(0, 10000, []);
      this.tags = await TagEndpoint.list(0, 10000, []);

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

    get projectNames() {
        return this.projects.map(p => p.project);
    }

    projectByName(projectName: string) {
        const p = this.projects.filter( p => p.project === projectName);
        return p && p.length > 0 ? p[0] : undefined;
    }

    set projects(newProjects: Project[]) {
        this._projects = newProjects;
    }

    @computed
    get intents() {
        return this._intents;
    }

    @computed
    get intentNames() {
        return this.intents.map(i => i.intent);
    }

    intentByName(intentName: string) {
        const p = this.intents.filter( p => p.intent === intentName);
        return p && p.length>0 ? p[0] : undefined;
    }

    set intents(newIntents: Intent[]) {
        this._intents = newIntents;
    }

    get tags() {
        return this._tags;
    }

    get tagNames() {
        return this.tags.map(t => t.tag);
    }

    tagByName(tagName: string) {
        const p = this.tags.filter( p => p.tag === tagName);
        return p && p.length>0 ? p[0] : undefined;
    }

    set tags(newTags: Tag[]) {
        this._tags = newTags;
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