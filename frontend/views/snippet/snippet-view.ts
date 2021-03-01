import {CrudView} from "../crud-view/crud-view";
import {customElement, html, property, unsafeCSS} from "lit-element";
import {Binder, field} from '@vaadin/form';
import SnippetDto from '../../generated/com/overwhale/colibri_so/frontend/dto/SnippetDto';
import SnippetDtoModel from '../../generated/com/overwhale/colibri_so/frontend/dto/SnippetDtoModel';
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
//import {until} from "lit-html/directives/until";
import SnippetType from "../../generated/com/overwhale/colibri_so/backend/entity/SnippetType";
import {EditMode} from "../utils/types";

const MAX_FAVOURITE_LEVEL = 4;
const FAVOURITE_COLORS = ['#cccccc', '#660000', '#aa0000', '#ff0000'];

@customElement('snippet-view')
export class ProjectView extends CrudView<SnippetDto>  implements BeforeEnterObserver {
    private binder = new Binder<SnippetDto, SnippetDtoModel>(this, SnippetDtoModel);
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

    protected createNewEntity(): SnippetDto {
        return {
            creatorId: store.sessionUser.id,
            snippetType: SnippetType.TEXT
        }
    }

    protected renderForm = (editMode: EditMode) => {
        if(editMode!==EditMode.CLOSE) {
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
        else {
            return html`
              <div></div>`;
        }
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="content" .renderer="${this.boundContentRenderer}"></vaadin-grid-sort-column>
        `;
    }

    protected allowInsert() {
        return false;
    }

    protected getEntity(id: any): Promise<SnippetDto | undefined> {
        return SnippetEndpoint.get(id);
    }

    protected updateEntity(entity: SnippetDto): Promise<SnippetDto> {
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

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<SnippetDto>> {
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

    private renderSnippetContent(snippet: SnippetDto) {
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
        const snippet = model.item as SnippetDto;
        const favouriteRawLevel = snippet.favouriteLevel ? snippet.favouriteLevel as number: 0;
        const favouriteLevel = favouriteRawLevel >=0 && favouriteRawLevel<MAX_FAVOURITE_LEVEL ? favouriteRawLevel : 0;
        const favouriteLevelCaption = favouriteLevel > 0 ? '(' + favouriteLevel + ')' : '';
        const favouriteLevelColor = 'color: ' + FAVOURITE_COLORS[favouriteLevel] + ';';
        const favouriteLevelTextStyle  = 'font-size: small; color: ' + FAVOURITE_COLORS[favouriteLevel] + ';';
        const formattedCreationTime = 'created: ' + moment(snippet.creationTime).format('MM/DD/YYYY hh:mm:ss');
        const formattedLastChangeTime = snippet.lastChangedTime ? 'modified:' + moment(snippet.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
          render(html`
                <vaadin-horizontal-layout theme="spacing-s" class="card">
                    <div style="display: flex; flex-direction: column;">
                    <iron-icon icon="vaadin:heart" style="${favouriteLevelColor}" @click="${this.toggleFavouriteLevel.bind(this, snippet.id)}"></iron-icon>
                    <span style="${favouriteLevelTextStyle}">${favouriteLevelCaption}</span>
                    </div>
                    <vaadin-vertical-layout>
                        <vaadin-horizontal-layout theme="spacing-s" class="header">
                            <span class="name">${snippet.description}</span>
                            <span class="date">${formattedCreationTime}</span>
                            <span class="date">${formattedLastChangeTime}</span>
                        </vaadin-horizontal-layout>
                        <span class="post">${this.renderSnippetContent(snippet)}</span>
                        <vaadin-horizontal-layout theme="spacing-s" class="actions">
                            <iron-icon icon="vaadin:archive"></iron-icon>
                            <span class="projects">
                                ${this.getProjects(snippet)}
                            </span>
                            <iron-icon icon="vaadin:automation"></iron-icon>
                            <span class="intents">
                                ${this.getIntents(snippet)}
                            </span>
                            <iron-icon icon="vaadin:bullets"></iron-icon>
                            <span class="tags">
                                ${this.getTags(snippet)}
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

/*

    <!--
    ${until(this.getProjectsAsync(snippet.id), html`<span>Loading...</span>`)}
    -->
    private getProjectsAsync(snippetId: string) {
        return SnippetEndpoint.listProjectsForSnippetId(snippetId, 0, 10000, []).then(
            projects => {
                if(projects.length==0) {
                    return '';
                }
                else if(projects.length==1) {
                    return "Project: " + projects[0].project;
                }
                else {
                    return "Projects: " + projects.map(prj => prj.project).join(', ');
                }
            }
        );
    }
*/
    private getProjects(snippet: SnippetDto) {
        if(!snippet.projects || snippet.projects.length==0) {
            return '';
        }
        else if(snippet.projects.length==1) {
            return "Project: " + snippet.projects[0].project;
        }
        else {
            return "Projects: " + snippet.projects.map(prj => prj.project).join(', ');
        }
    }

    private  getIntents(snippet: SnippetDto) {
        if(!snippet.intents || snippet.intents.length==0) {
            return '';
        }
        else if(snippet.intents.length==1) {
            return "Intent: " + snippet.intents[0].intent;
        }
        else {
            return "Intents: " + snippet.intents.map(i => i.intent).join(', ');
        }
    }

    private  getTags(snippet: SnippetDto) {
        if(!snippet.tags || snippet.tags.length==0) {
            return '';
        }
        else if(snippet.tags.length==1) {
            return "Tag: " + snippet.tags[0].tag;
        }
        else {
            return "Tags: " + snippet.tags.map(t => t.tag).join(', ');
        }
    }

    private async toggleFavouriteLevel(id: any) {
        const snippet = await SnippetEndpoint.get(id) as SnippetDto;
        if(snippet) {
            if(snippet.favouriteLevel && snippet.favouriteLevel >= 0) {
                snippet.favouriteLevel = snippet.favouriteLevel + 1;
                if(snippet.favouriteLevel >= MAX_FAVOURITE_LEVEL) {
                    snippet.favouriteLevel = 0;
                }
            }
            else {
                snippet.favouriteLevel = 1;
            }

        }
        SnippetEndpoint.update(snippet);
        this.clearForm();
        this.refreshGrid();
    }
}
