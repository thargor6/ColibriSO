import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Intent from '../../generated/com/overwhale/colibri_so/domain/entity/Intent';
import IntentModel from '../../generated/com/overwhale/colibri_so/domain/entity/IntentModel';
import * as IntentEndpoint from '../../generated/IntentEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";

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
            creationTime: '',
            creatorId: '',
            id: '',
            lastChangedTime: '',
            intent: '',
            description: ''
        };
    }

    protected renderForm = () => {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="Intent"
                        id="intent"
                        ...="${field(this.binder.model.intent)}"
                ></vaadin-text-field
                >
            </vaadin-form-layout>`;
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="intent"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Intent | undefined> {
        return IntentEndpoint.get(id);
    }

    protected updateEntity(entity: Intent): Promise<Intent> {
        return IntentEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
        return IntentEndpoint.count();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Intent>> {
        return IntentEndpoint.list(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return IntentEndpoint.delete(id);
    }
}
