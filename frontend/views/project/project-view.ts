import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";
import {Binder, field} from '@vaadin/form';
import ProjectDto from '../../generated/com/overwhale/colibri_so/frontend/dto/ProjectDto';
import ProjectDtoModel from '../../generated/com/overwhale/colibri_so/frontend/dto/ProjectDtoModel';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";
import {EditMode} from "../utils/types";
import '@vaadin/vaadin-combo-box';

@customElement('project-view')
export class ProjectView extends CrudView<ProjectDto> {
  private binder = new Binder<ProjectDto, ProjectDtoModel>(this, ProjectDtoModel);

  constructor() {
      super('Project', 'project-view');
  }

  protected getBinder() {
      return this.binder;
  }

  protected createNewEntity(): ProjectDto {
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
                  <vaadin-text-field 
                                    id="parentProjectId" 
                                     hidden
                                    readonly
                                    ...="${field(this.binder.model.parentProjectId)}"
                  ></vaadin-text-field>
                  <vaadin-text-field label="Parent"
                                     id="parentProjectCaption"
                                     readonly
                                     value="${this._boundRenderParentProjectCaption()}"
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
            <vaadin-grid-sort-column auto-width path="parentProjectId" .renderer="${this.parentProjectRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<ProjectDto | undefined> {
      return store.getProject(id);
    }

    protected updateEntity(entity: ProjectDto): Promise<ProjectDto> {
      if(entity.parentProjectId && entity.parentProjectId.hasOwnProperty('id')) {
          // workaround: the binder put the wohle object into this property, not just the key
          // correct this
          entity.parentProjectId = entity.parentProjectId.id;
      }
      return store.updateProject(entity);
    }

    protected countEntities(): Promise<number> {
        return store.countProjects();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<ProjectDto>> {
        return store.listProjects(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return store.deleteProject(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as ProjectDto;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    _boundRenderParentProjectCaption = this.renderParentProjectCaption.bind(this);

    private renderParentProjectCaption() {
        const project = this.getBinder().value as ProjectDto;
        return project?.parentProjectId ? store.projectById(project?.parentProjectId)!.project : '';
    }

    private parentProjectRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const project = model.item as ProjectDto;
        const caption = project?.parentProjectId ? store.projectById(project?.parentProjectId)!.project : '';
        render(html`<div>${caption}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as ProjectDto;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }

    protected renderButtons(editMode: EditMode) {
        if(editMode===EditMode.EDIT) {
            return html`
                ${super.renderButtons(editMode)}
                <vaadin-button @click="${this.createNewSubProject}">Create new Sub-Project</vaadin-button>
            `;
        }
        else {
            return super.renderButtons(editMode);
        }
    }

    private createNewSubProject() {
        const dto = this.createNewEntity();
        const parent = this.getBinder().value;
        dto.parentProjectId = parent.id;
        this.getBinder().read(dto);
        this.editCaption = 'New sub-project';
        this.editMode = EditMode.NEW;
    }
}
