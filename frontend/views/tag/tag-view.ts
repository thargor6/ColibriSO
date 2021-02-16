import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import Tag from '../../generated/com/overwhale/colibri_so/domain/entity/Tag';
import TagModel from '../../generated/com/overwhale/colibri_so/domain/entity/TagModel';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";

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
            creatorId: store.sessionUser.id,
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
            <vaadin-grid-sort-column auto-width path="tag"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<Tag | undefined> {
        return store.getTag(id);
    }

    protected updateEntity(entity: Tag): Promise<Tag> {
        return store.updateTag(entity);
    }

    protected countEntities(): Promise<number> {
        return store.countTags();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<Tag>> {
        return store.listTags(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return store.deleteTag(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Tag;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as Tag;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
