import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";
import {Binder, field} from '@vaadin/form';
import User from '../../generated/com/overwhale/colibri_so/domain/entity/User';
import UserModel from '../../generated/com/overwhale/colibri_so/domain/entity/UserModel';
import * as UserEndpoint from '../../generated/UserEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import '@vaadin/vaadin-text-field'
import '@vaadin/vaadin-checkbox'
import {GridColumnElement} from "@vaadin/vaadin-grid/vaadin-grid-column";
import {GridItemModel} from "@vaadin/vaadin-grid";
import {render} from "lit-html";
import * as moment from 'moment';
import {EditMode} from "../utils/types";

@customElement('user-view')
export class ProjectView extends CrudView<User> {
    private binder = new Binder<User, UserModel>(this, UserModel);

    constructor() {
        super('User', 'user-view');
    }

    protected getBinder() {
        return this.binder;
    }

    protected createNewEntity(): User {
        return {
            id: '',
            creationTime: '',
            lastChangedTime: '',
            username: '',
            enabled: true,
            passwordHash: '',
        }
    }

    protected renderForm = (editMode: EditMode) => {
        if(editMode!==EditMode.CLOSE) {
            return html`
                <vaadin-form-layout>
                    <vaadin-text-field
                            label="User name"
                            id="username"
                            ...="${field(this.binder.model.username)}"
                    ></vaadin-text-field>
                    <vaadin-checkbox
                            label="Enabled"
                            id="enabled"
                            ...="${field(this.binder.model.enabled)}"
                    ></vaadin-checkbox>
                </vaadin-form-layout>`;
        }
        else {
            return html`
              <div></div>`;
        }
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="username"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="enabled"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime" .renderer="${this.creationTimeRenderer}"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime" .renderer="${this.lastChangedTimeRenderer}"></vaadin-grid-sort-column>`;
    }

    protected getEntity(id: any): Promise<User | undefined> {
        return UserEndpoint.get(id);
    }

    protected updateEntity(entity: User): Promise<User> {
        return UserEndpoint.update(entity);
    }

    protected countEntities(): Promise<number> {
        return UserEndpoint.count();
    }

    protected listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<User>> {
        return UserEndpoint.list(offset, limit, sortOrder);
    }

    protected deleteEntity(id: any): Promise<void> {
        return UserEndpoint.delete(id);
    }

    private creationTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as User;
        const formattedTime = moment(user.creationTime).format('MM/DD/YYYY hh:mm:ss');
        render(html`<div>${formattedTime}</div>`, root);
    }

    private lastChangedTimeRenderer(root: HTMLElement, _column: GridColumnElement, model: GridItemModel) {
        const user = model.item as User;
        const formattedTime = user.lastChangedTime ?  moment(user.lastChangedTime).format('MM/DD/YYYY hh:mm:ss') : '';
        render(html`<div>${formattedTime}</div>`, root);
    }
}
