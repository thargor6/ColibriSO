import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Project from '../../generated/com/overwhale/colibri_so/domain/entity/Project';
import ProjectModel from '../../generated/com/overwhale/colibri_so/domain/entity/ProjectModel';
//import * as ProjectEndpoint from '../../generated/ProjectEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";
import {EditMode} from "../utils/types";

@customElement('project-view')
export class ProjectView extends CrudView<Project> {
  private binder = new Binder<Project, ProjectModel>(this, ProjectModel);

  constructor() {
      super('Project', 'project-view');
  }

  protected getBinder() {
      return this.binder;
  }

  protected createNewEntity(): Project {
      return {
          creatorId: store.sessionUser.id,
          project: ''
      }
  }

    protected renderForm = (editMode: EditMode)=> {
        if(editMode!==EditMode.CLOSE) {
          return html`
              <vaadin-form-layout>
                  <vaadin-text-field
                          label="Project"
                          id="project"
                          ...="${field(this.binder.model.project)}"
                  ></vaadin-text-field>
                  <vaadin-text-field
                          label="Description"
                          id="description"
                          ...="${field(this.binder.model.description)}"
                  ></vaadin-text-field>
              </vaadin-form-layout>`;
      }
      else {
          return html`
              <div></div>`;
      }
    }

  protected renderColumns = ()=> {
        return html`
            <vaadin-grid-sort-column auto-width path="project"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Project | undefined> {
      return store.getProject(id);
      //return ProjectEndpoint.get(id);
    }

    protected updateEntity(entity: Project): Promise<Project> {
      return store.updateProject(entity);
      //return ProjectEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
      //return ProjectEndpoint.count();
        return store.countProjects();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Project>> {
      //return ProjectEndpoint.list(offset, limit, sortOrder);
        return store.listProjects(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
      //return ProjectEndpoint.delete(id);
        return store.deleteProject(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Project;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Project;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
