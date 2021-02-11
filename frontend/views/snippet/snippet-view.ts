import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

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

@customElement('snippet-view')
export class ProjectView extends CrudView<Snippet>  implements BeforeEnterObserver {
    private binder = new Binder<Snippet, SnippetModel>(this, SnippetModel);

    constructor() {
        super('Snippet', 'snippet-view');
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
            <vaadin-grid-sort-column auto-width path="content"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Snippet | undefined> {
        return SnippetEndpoint.get(id);
    }

    protected updateEntity(entity: Snippet): Promise<Snippet> {
        return SnippetEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
        return SnippetEndpoint.count();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Snippet>> {
        return SnippetEndpoint.list(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return SnippetEndpoint.delete(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Snippet;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Snippet;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }

    protected _routerLocationChanged() {
        console.log(window.location.search);
    }

    onBeforeEnter(
        _location: RouterLocation,
        _commands: PreventAndRedirectCommands,
        _router: Router) {
        console.log(_location.params);
    }
}
