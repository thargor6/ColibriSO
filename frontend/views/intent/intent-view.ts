import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Intent from '../../generated/com/overwhale/colibri_so/domain/entity/Intent';
import IntentModel from '../../generated/com/overwhale/colibri_so/domain/entity/IntentModel';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";
import {EditMode} from "../utils/types";

@customElement('intent-view')
export class ProjectView extends CrudView<Intent> {
    private binder = new Binder<Intent, IntentModel>(this, IntentModel);

    constructor() {
        super('Intent', 'intent-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): Intent {
        return {
            creatorId: store.sessionUser.id,
            intent: ''
        };
    }

    protected renderForm = (editMode: EditMode) => {
        if(editMode!==EditMode.CLOSE) {
            return html`
                <vaadin-form-layout>
                    <vaadin-text-field
                            label="Intent"
                            id="intent"
                            ...="${field(this.binder.model.intent)}"
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
            <vaadin-grid-sort-column auto-width path="intent"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Intent | undefined> {
        return store.getIntent(id);
    }

    protected updateEntity(entity: Intent): Promise<Intent> {
        return store.updateIntent(entity);
    }

    protected countEntities(): Promise<number> {
        return store.countIntents();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Intent>> {
        return store.listIntents(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return store.deleteIntent(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Intent;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Intent;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
