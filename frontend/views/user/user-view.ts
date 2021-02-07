import {CrudView} from "../crud-view/crud-view";
import {customElement, html} from "lit-element";

import {Binder, field} from '@vaadin/form';
import User from '../../generated/com/overwhale/colibri_so/domain/entity/User';
import UserModel from '../../generated/com/overwhale/colibri_so/domain/entity/UserModel';
import * as UserEndpoint from '../../generated/UserEndpoint';
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";

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

    protected renderForm = () => {
        return html`
            <vaadin-form-layout>
                <vaadin-text-field
                        label="User name"
                        id="username"
                        ...="${field(this.binder.model.username)}"
                ></vaadin-text-field
                >
            </vaadin-form-layout>`;
    }

    protected renderColumns = () => {
        return html`
            <vaadin-grid-sort-column auto-width path="username"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="email"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="creationTime"></vaadin-grid-sort-column>
            <vaadin-grid-sort-column auto-width path="lastChangedTime"></vaadin-grid-sort-column>`;
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
}
