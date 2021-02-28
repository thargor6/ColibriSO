import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import IntentDto from '../../generated/com/overwhale/colibri_so/frontend/dto/IntentDto';
import IntentDtoModel from '../../generated/com/overwhale/colibri_so/frontend/dto/IntentDtoModel';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";
import {EditMode} from "../utils/types";

@customElement('intent-view')
export class ProjectView extends CrudView<IntentDto> {
    private binder = new Binder<IntentDto, IntentDtoModel>(this, IntentDtoModel);

    constructor() {
        super('Intent', 'intent-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): IntentDto {
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

    protected getEntity(id: any): Promise<IntentDto | undefined> {
        return store.getIntent(id);
    }

    protected updateEntity(entity: IntentDto): Promise<IntentDto> {
        return store.updateIntent(entity);
    }

    protected countEntities(): Promise<number> {
        return store.countIntents();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<IntentDto>> {
        return store.listIntents(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return store.deleteIntent(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as IntentDto;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as IntentDto;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
