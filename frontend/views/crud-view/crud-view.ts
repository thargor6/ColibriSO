import '@polymer/iron-icon';
import {showNotification} from '@vaadin/flow-frontend/a-notification';
import {EndpointError} from '@vaadin/flow-frontend/Connect';
import {CSSModule} from '@vaadin/flow-frontend/css-utils';
import {Binder} from '@vaadin/form';
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

import {html, property, query, TemplateResult, unsafeCSS} from 'lit-element';
import styles from './crud-view.css';
import {ConfirmationDialogElement} from "../components/confirmation-dialog";
import GridSorter from "../../generated/org/vaadin/artur/helpers/GridSorter";
import {AbstractModel} from "@vaadin/form";
import {MobxLitElement} from "@adobe/lit-mobx";

interface BaseEntity {
    id?: string;
}

export abstract class CrudView<EntityType extends BaseEntity> extends MobxLitElement {
    @query('#grid')
    private grid!: GridElement;
    @property({type: Number})
    private gridSize = 0;
    private gridDataProvider = this.getGridData.bind(this);

    constructor(private objectName: string, private componentName: string) {
        super();
    }

    static get styles() {
        return [CSSModule('lumo-typography'), unsafeCSS(styles)];
    }

    protected abstract getBinder(): Binder<EntityType, AbstractModel<EntityType>>;

    protected abstract renderColumns: ()=> TemplateResult;

    protected abstract renderForm: ()=> TemplateResult;

    protected abstract createNewEntity(): EntityType;

    protected abstract getEntity(id: any): Promise<EntityType | undefined>;

    protected abstract updateEntity(entity: EntityType): Promise<EntityType>;

    protected abstract countEntities(): Promise<number>;

    protected abstract listEntities(offset: number, limit: number, sortOrder: Array<GridSorter>): Promise<Array<EntityType>>;

    protected abstract  deleteEntity(id: any): Promise<void>;

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
                        ${this.renderColumns()}
                    </vaadin-grid>
                </div>
                <div id="editor-layout">
                    <div id="editor">
                      ${this.renderForm()}
                    </div>

                    <vaadin-horizontal-layout id="button-layout" theme="spacing">
                        <vaadin-button theme="primary" @click="${this.save}">Save</vaadin-button>
                        <vaadin-button theme="tertiary" @click="${this.cancel}">Cancel</vaadin-button>
                        <vaadin-button theme="tertiary" @click="${this.delete}">Delete</vaadin-button>
                        <vaadin-button @click="${this.create}">Create new ${this.objectName}</vaadin-button>
                    </vaadin-horizontal-layout>
                </div>
            </vaadin-split-layout>
        `;
    }

    async connectedCallback() {
        super.connectedCallback();
        this.gridSize = await this.countEntities();
    }

    private async getGridData(params: GridDataProviderParams, callback: GridDataProviderCallback) {
        const index = params.page * params.pageSize;
        const data = await this.listEntities(index, params.pageSize, params.sortOrders as any);
        callback(data);
    }

    private async itemSelected(event: CustomEvent) {
        const item: EntityType = event.detail.value as EntityType;
        this.grid.selectedItems = item ? [item] : [];

        if (item) {
            const fromBackend = await this.getEntity(item.id);
            fromBackend ? this.getBinder().read(fromBackend) : this.refreshGrid();
        } else {
            this.clearForm();
        }
    }

    private async save() {
        try {
            const entityId = this.getBinder().value.id;
            await this.getBinder().submitTo(this.updateEntity);
            if (!entityId) {
                // We added a new item
                this.gridSize++;
            }
            this.clearForm();
            this.refreshGrid();
            showNotification(`${this.objectName} details stored.`, {position: 'bottom-start'});
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
        this.getBinder().read(this.createNewEntity());
    }

    private delete() {
        const dialog: ConfirmationDialogElement = selectElementFromComponent(this.componentName, '#confirm_dlg') as ConfirmationDialogElement;
        dialog.message = `Do you really want to delete this ${this.objectName}?`;
        dialog.showDialog(this.execDelete.bind(this));
    }

    private async execDelete() {
        try {
            const entity = this.getBinder().value;
            if (entity.id) {
                await this.deleteEntity(entity.id);
                if(!entity.id) {
                    this.gridSize--;
                }
                this.clearForm();
                this.refreshGrid();
                showNotification(`${this.objectName} was removed.`, {position: 'bottom-start'});
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
        this.getBinder().clear();
    }

    private refreshGrid() {
        this.grid.selectedItems = [];
        this.grid.clearCache();
    }
}
