import {makeAutoObservable} from 'mobx';
import ProjectDto from "./generated/com/overwhale/colibri_so/frontend/dto/ProjectDto";
import UserDto from "./generated/com/overwhale/colibri_so/frontend/dto/UserDto";
import * as ProjectEndpoint from './generated/ProjectEndpoint';
import * as IntentEndpoint from './generated/IntentEndpoint';
import * as TagEndpoint from './generated/TagEndpoint';
import * as UserEndpoint from './generated/UserEndpoint';
import * as UserDetailEndpoint from './generated/UserDetailEndpoint';
import {getSessionUserId} from "./auth";
import UserDetailDto from "./generated/com/overwhale/colibri_so/frontend/dto/UserDetailDto";
import IntentDto from "./generated/com/overwhale/colibri_so/frontend/dto/IntentDto";
import TagDto from "./generated/com/overwhale/colibri_so/frontend/dto/TagDto";
import GridSorter from "./generated/org/vaadin/artur/helpers/GridSorter";
import {Params} from "@vaadin/router";
import * as SnippetEndpoint from "./generated/SnippetEndpoint";

export interface MenuTab {
    route: string;
    name: string;
    params?: Params
}

const baseMenuTabs: MenuTab[] = [
    { route: 'snippet', name: 'Snippets' },
];

class Store {
    private static _instance:Store = new Store();
    private _projects: ProjectDto[] = [];
    private _intents: IntentDto[] = [];
    private _tags: TagDto[] = [];
    private _sessionUser: UserDto = {
        creationTime: undefined,
        enabled: false,
        id: undefined,
        passwordHash: "",
        username: ""
    };
    private _menuTabs: MenuTab[] = [];

    private _sessionUserDetail: UserDetailDto = {
        creationTime: undefined, userId: undefined, asyncTableRefresh: false};

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
      this.intents = await IntentEndpoint.list(0, 10000, []);
      this.tags = await TagEndpoint.list(0, 10000, []);
      this.menuTabs = await this.updateMenuTabs();
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

    private addMenuItems(newMenuTabs: MenuTab[], level: number, parentId: any, counts: Map<string, number>) {
        if(level>10) {
            console.log('Recursion level overflow')
            return;
        }
        var prefix = '';
        for(var i=0;i<level;i++) {
            prefix = '.  ' + prefix;
        }
        store.projects.filter(p => p.parentProjectId === parentId).map( item => {
            const count = counts.get(item.project);
            newMenuTabs.push( {
                name: prefix + item.project + (count && count>0 ? ' ['+count+']' : ''),
                route: "/snippet/:project",
                params: {'project': item.project}
            }  );
            this.addMenuItems(newMenuTabs, level + 1, item.id, counts);
        });

    }

    private async updateMenuTabs() {
        const newMenuTabs: MenuTab[] = [...baseMenuTabs];

        const promises = new Array<Promise<void>>();
        const counts = new Map();

        const promise = SnippetEndpoint.count().then(c => {
            counts.set('', c);
        });
        promises.push(promise);

        store.projects.map( item => {
            const projectId = store.projectByName(item.project);
            if(projectId) {
                const promise = SnippetEndpoint.countForProjectId(projectId.id).then(c => {
                    counts.set(item.project, c);
                });
                promises.push(promise);
            }
        });
        await Promise.all(promises);

        const count = counts.get('');
        newMenuTabs[0].name = 'All Snippets' +  (count && count>0 ? ' ['+count+']' : '');

        newMenuTabs.push( {
            name: '............................',
            route: "/snippet/",
            params: {'project': ''}
        }  );

        this.addMenuItems(newMenuTabs, 1, null, counts);
/*
        store.projects.map( item => {
            const count = counts.get(item.project);
            newMenuTabs.push( {
                name: item.project + (count && count>0 ? ' ['+count+']' : ''),
                route: "/snippet/:project",
                params: {'project': item.project}
            }  ) });
*/
        return newMenuTabs;
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

    projectById(projectId: string) {
        const p = this.projects.filter( p => p.id === projectId);
        return p && p.length > 0 ? p[0] : undefined;
    }

    refreshMenuTabs() {
        this.updateMenuTabs().then( newMenuTabs => {
            this.menuTabs = newMenuTabs;
        });
    }

    set projects(newProjects: ProjectDto[]) {
        this._projects = newProjects;
        this.refreshMenuTabs();
    }

    get intents() {
        return this._intents;
    }

    get intentNames() {
        return this.intents.map(i => i.intent);
    }

    intentByName(intentName: string) {
        const p = this.intents.filter( p => p.intent === intentName);
        return p && p.length>0 ? p[0] : undefined;
    }

    set intents(newIntents: IntentDto[]) {
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

    set tags(newTags: TagDto[]) {
        this._tags = newTags;
    }

    get sessionUser() {
            return this._sessionUser;
    }

    set sessionUser(newUser: UserDto) {
        this._sessionUser = newUser;
    }

    set sessionUserDetail(newUserDetail: UserDetailDto) {
        this._sessionUserDetail = newUserDetail;
    }

    get sessionUserDetail() {
            return this._sessionUserDetail;
    }

    clearSessionData() {
        this.sessionUser = {creationTime: undefined, enabled: false, id: undefined, passwordHash: "", username: ""};
        this.sessionUserDetail = {creationTime: undefined, userId: undefined, asyncTableRefresh: false};
    }

    set menuTabs(newMenuTabs: MenuTab[]) {
        this._menuTabs = newMenuTabs;
    }

    get menuTabs() {
        return this._menuTabs;
    }

    public getProject(id: string): Promise<ProjectDto | undefined> {
        const that = this;
        return new Promise( resolve => {
            setTimeout( ()=> {
              resolve(that.projects.find( p => p.id === id ));
            });
        } );
    }

    public getTag(id: string): Promise<TagDto | undefined> {
        const that = this;
        return new Promise( resolve => {
            setTimeout( ()=> {
                resolve(that.tags.find( p => p.id === id ));
            });
        } );
    }

    public getIntent(id: string): Promise<IntentDto | undefined> {
        const that = this;
        return new Promise( resolve => {
            setTimeout( ()=> {
                resolve(that.intents.find( p => p.id === id ));
            });
        } );
    }

    public updateProject(entity: ProjectDto) {
        const that = this;
        return ProjectEndpoint.update(entity).then(
             project => {
                 const newProjects: ProjectDto[] = [];
                 that.projects.map(t => newProjects.push(t.id === project.id ? project : t));
                 if(!entity.id) {
                     newProjects.push(entity);
                 }
                 entity.id = project.id;
                 entity.creationTime = project.creationTime;
                 entity.lastChangedTime = project.lastChangedTime;
                 that.projects = newProjects;

                 return entity;
             }
         );
    }

    public updateTag(entity: TagDto) {
        const that = this;
        return TagEndpoint.update(entity).then(
            tag => {
                const newTags: TagDto[] = [];
                that.tags.map(t => newTags.push(t.id === tag.id ? tag : t));
                if(!entity.id) {
                    newTags.push(entity);
                }
                entity.id = tag.id;
                entity.creationTime = tag.creationTime;
                entity.lastChangedTime = tag.lastChangedTime;
                that.tags = newTags;
                return entity;
            }
        );
    }

    public updateIntent(entity: IntentDto) {
        const that = this;
        return IntentEndpoint.update(entity).then(
            intent => {
                const newIntents: IntentDto[] = [];
                that.intents.map(t => newIntents.push(t.id === intent.id ? intent : t));
                if(!entity.id) {
                    newIntents.push(entity);
                }
                entity.id = intent.id;
                entity.creationTime = intent.creationTime;
                entity.lastChangedTime = intent.lastChangedTime;
                that.intents = newIntents;
                return entity;
            }
        );
    }

    public countProjects(): Promise<number> {
        const that = this;
        return new Promise(resolve => {
            setTimeout( () => {
                resolve(that.projects.length);
            } );
        });
    }

    public countTags(): Promise<number> {
        const that = this;
        return new Promise(resolve => {
            setTimeout( () => {
                resolve(that.tags.length);
            } );
        });
    }

    public countIntents(): Promise<number> {
        const that = this;
        return new Promise(resolve => {
            setTimeout( () => {
                resolve(that.intents.length);
            } );
        });
    }

    public listProjects(_offset: number, _limit: number, _sortOrder: Array<GridSorter>): Promise<Array<ProjectDto>> {
       const that = this;
       return new Promise(resolve => {
           setTimeout(() => {
               resolve([...that.projects]);
           })
       })
    }

    public listTags(_offset: number, _limit: number, _sortOrder: Array<GridSorter>): Promise<Array<TagDto>> {
        const that = this;
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([...that.tags]);
            })
        })
    }

    public listIntents(_offset: number, _limit: number, _sortOrder: Array<GridSorter>): Promise<Array<IntentDto>> {
        const that = this;
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([...that.intents]);
            })
        })
    }

    public deleteProject(id: string): Promise<void> {
        const that = this;
        return ProjectEndpoint.delete(id).then(() => {
            const newProjects: ProjectDto[] = [];
            that.projects.map(t => (t.id !== id ? newProjects.push(t) : t.id = undefined));
            that.projects = newProjects;
            return;
        });
    }

    public deleteTag(id: string): Promise<void> {
        const that = this;
        return TagEndpoint.delete(id).then(() => {
            const newTags: TagDto[] = [];
            that.tags.map(t => (t.id !== id ? newTags.push(t) : t.id = undefined));
            that.tags = newTags;
            return;
        });
    }

    public deleteIntent(id: string): Promise<void> {
        const that = this;
        return IntentEndpoint.delete(id).then(() => {
            const newIntents: IntentDto[] = [];
            that.intents.map(t => (t.id !== id ? newIntents.push(t) : t.id = undefined));
            that.intents = newIntents;
            return;
        });
    }
}

export const store = Store.getInstance();