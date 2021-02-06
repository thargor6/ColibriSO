import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Project from '../../generated/com/overwhale/colibri_so/domain/entity/Project';
import ProjectModel from '../../generated/com/overwhale/colibri_so/domain/entity/ProjectModel';
import * as ProjectEndpoint from '../../generated/ProjectEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";

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
          creationTime: '',
          creatorId: '',
          id: '',
          lastChangedTime: '',
          project: '',
          description: ''
      }
  }

    protected renderForm = ()=> {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="Project"
                        id="project"
                        ...="${field(this.binder.model.project)}"
                ></vaadin-text-field
                >
            </vaadin-form-layout>`;
    }

  protected renderColumns = ()=> {
        return html`
            <vaadin-grid-sort-column auto-width path="project"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Project | undefined> {
      return ProjectEndpoint.get(id);
    }

    protected updateEntity(entity: Project): Promise<Project> {
      return ProjectEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
      return ProjectEndpoint.count();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Project>> {
      return ProjectEndpoint.list(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
      return ProjectEndpoint.delete(id);
    }
}
