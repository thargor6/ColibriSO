import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import TagDto from '../../generated/com/overwhale/colibri_so/frontend/dto/TagDto';
import TagDtoModel from '../../generated/com/overwhale/colibri_so/frontend/dto/TagDtoModel';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {render} from "lit-html";
import * as moment from 'moment';
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {store} from "../../store";
import {EditMode} from "../utils/types";

@customElement('tag-view')
export class ProjectView extends CrudView<TagDto> {
    private binder = new Binder<TagDto, TagDtoModel>(this, TagDtoModel);

    constructor() {
        super('Tag', 'tag-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): TagDto {
        return {
            creatorId: store.sessionUser.id,
            tag: ''
        };
    }

    protected renderForm = (editMode: EditMode) => {
        if(editMode!==EditMode.CLOSE) {
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
        else {
            return html`
              <div></div>`;
        }
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="tag"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="description"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<TagDto | undefined> {
        return store.getTag(id);
    }

    protected updateEntity(entity: TagDto): Promise<TagDto> {
        return store.updateTag(entity);
    }

    protected countEntities(): Promise<number> {
        return store.countTags();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<TagDto>> {
        return store.listTags(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return store.deleteTag(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as TagDto;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as TagDto;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
