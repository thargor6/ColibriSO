import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Snippet from '../../generated/com/overwhale/colibri_so/domain/entity/Snippet';
import SnippetModel from '../../generated/com/overwhale/colibri_so/domain/entity/SnippetModel';
import * as SnippetEndpoint from '../../generated/SnippetEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";

@customElement('snippet-view')
export class ProjectView extends CrudView<Snippet> {
    private binder = new Binder<Snippet, SnippetModel>(this, SnippetModel);

    constructor() {
        super('Snippet', 'snippet-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): Snippet {
        return {
            creationTime: '',
            creatorId: '',
            id: '',
            lastChangedTime: '',
            content: '',
            description: ''
        }
    }

    protected renderForm = () => {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="Content"
                        id="content"
                        ...="${field(this.binder.model.content)}"
                ></vaadin-text-field
                >
            </vaadin-form-layout>`;
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="content"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime"></vaadin-grid-sort-column>`;
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
}
