import {makeAutoObservable} from 'mobx';
import Project from "./generated/com/overwhale/colibri_so/domain/entity/Project";
import * as ProjectEndpoint from './generated/ProjectEndpoint';

class Store {
    private _projects: Project[] = [];

    constructor() {
        makeAutoObservable(this);
        this.init();
    }

    async init() {
      this.projects = await ProjectEndpoint.list(0, 10000, []);
    }

    set projects(newProjects: Project[]) {
        this._projects = newProjects;
    }

    get projects() {
        return this._projects;
    }
}

export const store = new Store();