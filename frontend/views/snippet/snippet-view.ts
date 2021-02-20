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
import {BeforeEnterObserver, PreventAndRedirectCommands, Router, RouterLocation} from "@vaadin/router";
import styles from './snippet-view.css';
import base_styles from '../crud-view/crud-view.css';
import {CSSModule} from '@vaadin/flow-frontend/css-utils';
import {until} from "lit-html/directives/until";
import SnippetType from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetType";

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
            creatorId: store.sessionUser.id,
            snippetType: SnippetType.TEXT
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
            <vaadin-grid-sort-column auto-width path="content" .renderer="${this.boundContentRenderer}"></vaadin-grid-sort-column>
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

    boundContentRenderer = this.contentRenderer.bind(this);


    private parseYoutubeUrl(url: string) {
        var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
        var match = url.match(regExp);
        return (match&&match[7].length==11)? match[7] : '';
    }

    private renderSnippetContent(snippet: Snippet) {
        if(SnippetType.YOUTUBE === snippet.snippetType) {

            let videoCode = '';
            if(snippet.content) {
              videoCode = this.parseYoutubeUrl(snippet.content);
              if(videoCode === '' && !snippet.content.includes('/')) {
                  videoCode = snippet.content;
              }
            }
            if(videoCode!=='') {
                return html`
                    <div>
                        <iframe width="420" height="315" 
                                src="https://www.youtube.com/embed/${videoCode}"
                        ></iframe>
                    </div>
                  `;
            }
            else {
                return html`
                    <div></div>
                  `;
            }
        }
        else if(SnippetType.LINK === snippet.snippetType) {
            return html`
                        <a href="${snippet.content}" target="_blank">${snippet.content}</a>
        `;
        }
        else {
            return html`
                        <div>${snippet.content}</div>
        `;
        }
    }

    private contentRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const snippet = model.item as Snippet;
        const formattedCreationTime = 'created: ' + moment(snippet.creationTime).format('MM/DD/YYYY hh:mm:ss');
        const formattedLastChangeTime = snippet.lastChangedTime ? 'modified:' + moment(snippet.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
          render(html`
                <vaadin-horizontal-layout theme="spacing-s" class="card">
                    <iron-icon icon="vaadin:heart"></iron-icon>
                    <vaadin-vertical-layout>
                        <vaadin-horizontal-layout theme="spacing-s" class="header">
                            <span class="name">${snippet.description}</span>
                            <span class="date">${formattedCreationTime}</span>
                            <span class="date">${formattedLastChangeTime}</span>
                        </vaadin-horizontal-layout>
                        <span class="post">${this.renderSnippetContent(snippet)}</span>
                        <vaadin-horizontal-layout theme="spacing-s" class="actions">
                            <iron-icon icon="vaadin:heart"></iron-icon>
                            <span class="projects">
                                ${until(this.getProjects(snippet.id), html`<span>Loading...</span>`)}
                            </span>
                            <iron-icon icon="vaadin:comment"></iron-icon>
                            <span class="intents">
                                ${until(this.getIntents(snippet.id), html`<span>Loading...</span>`)}
                            </span>
                            <iron-icon icon="vaadin:connect"></iron-icon>
                            <span class="tags">
                                ${until(this.getTags(snippet.id), html`<span>Loading...</span>`)}
                            </span>
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
                if(projects.length==0) {
                    return '';
                }
                else if(projects.length==1) {
                    return "Project: " + projects[0].project;
                }
                else {
                    return "Projects: " + projects.map(prj => prj.project).join(',');
                }
            }
        );
    }

    private  getIntents(snippetId: string) {
        return  SnippetEndpoint.listIntentsForSnippetId(snippetId, 0, 10000, []).then(
            intents => {
                if(intents.length==0) {
                    return '';
                }
                else if(intents.length==1) {
                    return "Intent: " + intents[0].intent;
                }
                else {
                    return "Intents: " + intents.map(prj => prj.intent).join(',');
                }
            }
        )
    }

    private  getTags(snippetId: string) {
        return  SnippetEndpoint.listTagsForSnippetId(snippetId, 0, 10000, []).then(
            tags => {
                if(tags.length==0) {
                    return '';
                }
                else if(tags.length==1) {
                    return "Tag: " + tags[0].tag;
                }
                else {
                    return "Tags: " + tags.map(prj => prj.tag).join(',');
                }
            }
        );
    }
}
