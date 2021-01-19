import '@polymer/iron-icon';
import {showNotification} from '@vaadin/flow-frontend/a-notification';
import {EndpointError} from '@vaadin/flow-frontend/Connect';
import {CSSModule} from '@vaadin/flow-frontend/css-utils';
import {Binder, field} from '@vaadin/form';
import '@vaadin/vaadin-button/vaadin-button';
import '@vaadin/vaadin-date-picker';
import '@vaadin/vaadin-form-layout/vaadin-form-layout';
import '@vaadin/vaadin-grid';
import {GridDataProviderCallback, GridDataProviderParams, GridElement} from '@vaadin/vaadin-grid/vaadin-grid';
import '@vaadin/vaadin-grid/vaadin-grid-sort-column';
import '@vaadin/vaadin-icons';
import '@vaadin/vaadin-ordered-layout/vaadin-horizontal-layout';
import '@vaadin/vaadin-split-layout/vaadin-split-layout';
import '@vaadin/vaadin-text-field';
import '@vaadin/vaadin-upload';
import '@vaadin/vaadin-dialog';
import '../components/confirmation-dialog';
import {selectElementFromComponent} from '../utils/document-utils';

import {customElement, html, LitElement, property, query, unsafeCSS} from 'lit-element';
import User from '../../generated/com/overwhale/colibri_so/domain/entity/User';
import UserModel from '../../generated/com/overwhale/colibri_so/domain/entity/UserModel';
import * as UserEndpoint from '../../generated/UserEndpoint';
import styles from './user-view.css';
//import { v4 as uuidv4 } from 'uuid';
import {ConfirmationDialogElement} from "../components/confirmation-dialog";

@customElement('user-view')
export class UserView extends LitElement {
    @query('#grid')
    private grid!: GridElement;
    @property({type: Number})
    private gridSize = 0;
    private gridDataProvider = this.getGridData.bind(this);
    private binder = new Binder<User, UserModel>(this, UserModel);

    static get styles() {
        return [CSSModule('lumo-typography'), unsafeCSS(styles)];
    }

    render() {
        return html`
            <confirmation-dialog id="confirm_dlg"></confirmation-dialog>

            <vaadin-split-layout class="full-size">
                <div class="grid-wrapper">
                    <vaadin-grid
                            id="grid"
                            class="full-size"
                            theme="no-border"
                            .size="${this.gridSize}"
                            .dataProvider="${this.gridDataProvider}"
                            @active-item-changed=${this.itemSelected}
                    >
                        <vaadin-grid-sort-column auto-width path="username"></vaadin-grid-sort-column>
                        <vaadin-grid-sort-column auto-width path="email"></vaadin-grid-sort-column>
                    </vaadin-grid>
                </div>
                <div id="editor-layout">
                    <div id="editor">
                        <vaadin-form-layout>
                            <vaadin-text-field
                                    label="User name"
                                    id="username"
                                    ...="${field(this.binder.model.username)}"
                            ></vaadin-text-field
                            >
                            <vaadin-text-field label="Email" id="email"
                                               ...="${field(this.binder.model.email)}"></vaadin-text-field
                            >
                        </vaadin-form-layout
                        >
                    </div>

                    <vaadin-horizontal-layout id="button-layout" theme="spacing">
                        <vaadin-button theme="primary" @click="${this.save}">Save</vaadin-button>
                        <vaadin-button theme="tertiary" @click="${this.cancel}">Cancel</vaadin-button>
                        <vaadin-button theme="tertiary" @click="${this.delete}">Delete</vaadin-button>
                        <vaadin-button @click="${this.create}">Create new user</vaadin-button>
                    </vaadin-horizontal-layout>
                </div>
            </vaadin-split-layout>
        `;
    }

    async connectedCallback() {
        super.connectedCallback();
        this.gridSize = await UserEndpoint.count();
    }

    private async getGridData(params: GridDataProviderParams, callback: GridDataProviderCallback) {
        const index = params.page * params.pageSize;
        const data = await UserEndpoint.list(index, params.pageSize, params.sortOrders as any);
        callback(data);
    }

    private async itemSelected(event: CustomEvent) {
        const item: User = event.detail.value as User;
        this.grid.selectedItems = item ? [item] : [];

        if (item) {
            const fromBackend = await UserEndpoint.get(item.id);
            fromBackend ? this.binder.read(fromBackend) : this.refreshGrid();
        } else {
            this.clearForm();
        }
    }

    private async save() {
        try {
            await this.binder.submitTo(UserEndpoint.update);
            if (!this.binder.value.id) {
                // We added a new item
                this.gridSize++;
            }
            this.clearForm();
            this.refreshGrid();
            showNotification('Person details stored.', {position: 'bottom-start'});
        } catch (error) {
            if (error instanceof EndpointError) {
                showNotification('Server error. ' + error.message, {position: 'bottom-start'});
            } else {
                throw error;
            }
        }
    }

    private cancel() {
        this.grid.activeItem = undefined;
    }

    private create() {
      const newUser: User = {
          id: '',
          creationTime: '',
          lastChangedTime: '',
          username: '',
          email: '',
      }
      this.binder.read(newUser);
    }

    private delete() {
        const dialog: ConfirmationDialogElement = selectElementFromComponent('user-view', '#confirm_dlg') as ConfirmationDialogElement;
        dialog.message = 'Do you really want to delete this user?';
        dialog.showDialog(this.execDelete.bind(this));
    }

    private async execDelete() {
        try {
        if (this.binder.value.id) {
          await UserEndpoint.delete(this.binder.value.id);

          if (!this.binder.value.id) {
            // We removed a item
            this.gridSize--;
          }
          this.clearForm();
          this.refreshGrid();
          showNotification('User was removed.', {position: 'bottom-start'});
        }
      } catch (error) {
        if (error instanceof EndpointError) {
          showNotification('Server error. ' + error.message, {position: 'bottom-start'});
        } else {
          throw error;
        }
      }
    }

    private clearForm() {
        this.binder.clear();
    }

    private refreshGrid() {
        this.grid.selectedItems = [];
        this.grid.clearCache();
    }
}
