import {CrudView} from "../crud-view/crud-view";
import {customElement, html, property, unsafeCSS} from "lit-element";
import {Binder, field} from '@vaadin/form';
import Snippet from '../../generated/com/overwhale/colibri_so/domain/entity/Snippet';
import SnippetModel from '../../generated/com/overwhale/colibri_so/domain/entity/SnippetModel';
import * as SnippetEndpoint from '../../generated/SnippetEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import * as moment from "moment";
import {render} from "lit-html";
import {store} from "../../store";
import {Router, RouterLocation, PreventAndRedirectCommands, BeforeEnterObserver} from "@vaadin/router";
import styles from './snippet-view.css';
import base_styles from '../crud-view/crud-view.css';
import {CSSModule} from '@vaadin/flow-frontend/css-utils';

@customElement('snippet-view')
export class ProjectView extends CrudView<Snippet>  implements BeforeEnterObserver {
    private binder = new Binder<Snippet, SnippetModel>(this, SnippetModel);
    @property({type: String}) projectId = '';

    constructor() {
        super('Snippet', 'snippet-view');
    }

    static get styles() {
        return [CSSModule('lumo-typography'), unsafeCSS(base_styles), unsafeCSS(styles)];

    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): Snippet {
        return {
            creatorId: store.sessionUser.id
        }
    }

    protected renderForm = () => {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="Content"
                        id="content"
                        ...="${field(this.binder.model.content)}"
                ></vaadin-text-field>
                <vaadin-text-field
                        label="Description"
                        id="description"
                        ...="${field(this.binder.model.description)}"
                ></vaadin-text-field>
            </vaadin-form-layout>`;
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="content" .renderer="${this.contentRenderer.bind(this)}"></vaadin-grid-sort-column>
        <!--    
            <vaadin-grid-sort-column auto-width path="content"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>
        -->
        `;
    }

    protected getEntity(id: any): Promise<Snippet | undefined> {
        return SnippetEndpoint.get(id);
    }

    protected updateEntity(entity: Snippet): Promise<Snippet> {
        return SnippetEndpoint.update(entity).then(entity => {
            store.refreshMenuTabs();
            return entity;
        });
    }

    protected countEntities(): Promise<number> {
        if(this.projectId) {
            return SnippetEndpoint.countForProjectId(this.projectId);
        }
        else {
            return SnippetEndpoint.count();
        }
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Snippet>> {
        if(this.projectId) {
            return SnippetEndpoint.listForProjectId(this.projectId, offset, limit, sortOrder);
        }
        else {
            return SnippetEndpoint.list(offset, limit, sortOrder);
        }
    }

    protected deleteEntity(id: any): Promise<void> {
        return SnippetEndpoint.delete(id).then(()=> {
          store.refreshMenuTabs();
        })
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const snippet = model.item as Snippet;
        const formattedTime = moment(snippet.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const snippet = model.item as Snippet;
        const formattedTime = snippet.lastChangedTime ?  moment(snippet.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }

    private contentRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const snippet = model.item as Snippet;
        const formattedCreationTime = 'created: ' + moment(snippet.creationTime).format('MM/DD/YYYY hh:mm:ss');
        const formattedLastChangeTime = snippet.lastChangedTime ? 'modified:' + moment(snippet.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        const boundGetTags = this.getTags.bind(this, snippet.id);
        const boundGetProjects = this.getProjects.bind(this, snippet.id);
        const boundGetIntents = this.getIntents.bind(this, snippet.id);
          render(html`
                <vaadin-horizontal-layout theme="spacing-s" class="card">
                    <iron-icon icon="vaadin:heart"></iron-icon>
                    <vaadin-vertical-layout>
                        <vaadin-horizontal-layout theme="spacing-s" class="header">
                            <span class="name">${snippet.description}</span>
                            <span class="date">${formattedCreationTime}</span>
                            <span class="date">${formattedLastChangeTime}</span>
                        </vaadin-horizontal-layout>
                        <span class="post">${snippet.content}</span>
                        <vaadin-horizontal-layout theme="spacing-s" class="actions">
                            <iron-icon icon="vaadin:heart"></iron-icon>
                            <span class="projects">${boundGetProjects()}</span>
                            <iron-icon icon="vaadin:comment"></iron-icon>
                            <span class="intents">${boundGetIntents()}</span>
                            <iron-icon icon="vaadin:connect"></iron-icon>
                            <span class="tags">${boundGetTags()}</span>
                        </vaadin-horizontal-layout> 
                        
                    </vaadin-vertical-layout>
                </vaadin-horizontal-layout>

        `, root);
    }




    protected _routerLocationChanged() {
        console.log(window.location.search);
    }

    onBeforeEnter(
        _location: RouterLocation,
        _commands: PreventAndRedirectCommands,
        _router: Router) {
        const projectName = _location.params['project'] as string;
        if(projectName) {
           const project = store.projectByName(projectName);
           if(project) {
               this.projectId = project.id;
           }
           else {
               this.projectId = '';
           }
        }
        else {
            this.projectId = '';
        }
    }


    private getProjects(snippetId: string) {
        return SnippetEndpoint.listProjectsForSnippetId(snippetId, 0, 10000, []).then(
            projects => {
                return 'Prj:' + projects.length
            }
        );
    }

    private  getIntents(snippetId: string) {
        return  SnippetEndpoint.listIntentsForSnippetId(snippetId, 0, 10000, []);
    }

    private  getTags(snippetId: string) {
        return  SnippetEndpoint.listTagsForSnippetId(snippetId, 0, 10000, []);
    }
}
