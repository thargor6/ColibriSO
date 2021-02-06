import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Tag from '../../generated/com/overwhale/colibri_so/domain/entity/Tag';
import TagModel from '../../generated/com/overwhale/colibri_so/domain/entity/TagModel';
import * as TagEndpoint from '../../generated/TagEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";

@customElement('tag-view')
export class ProjectView extends CrudView<Tag> {
    private binder = new Binder<Tag, TagModel>(this, TagModel);

    constructor() {
        super('Tag', 'tag-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): Tag {
        return {
            creationTime: '',
            creatorId: '',
            id: '',
            lastChangedTime: '',
            tag: ''
        };
    }

    protected renderForm = () => {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="Tag"
                        id="tag"
                        ...="${field(this.binder.model.tag)}"
                ></vaadin-text-field
                >
            </vaadin-form-layout>`;
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="tag"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Tag | undefined> {
        return TagEndpoint.get(id);
    }

    protected updateEntity(entity: Tag): Promise<Tag> {
        return TagEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
        return TagEndpoint.count();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Tag>> {
        return TagEndpoint.list(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return TagEndpoint.delete(id);
    }
}
