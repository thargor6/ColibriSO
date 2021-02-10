import {customElement, html, LitElement, property} from 'lit-element';
import {render} from 'lit-html';
import '@vaadin/vaadin-button/vaadin-button.js';
import '@vaadin/vaadin-date-picker/vaadin-date-picker.js';
import '@vaadin/vaadin-dialog/vaadin-dialog.js';
import {CallbackFunction} from '../utils/types';
import {Binder, field} from '@vaadin/form';
import Snippet from '../../generated/com/overwhale/colibri_so/domain/entity/Snippet';
import SnippetModel from '../../generated/com/overwhale/colibri_so/domain/entity/SnippetModel';
import {store} from "../../store";
import {showNotification} from '@vaadin/flow-frontend/a-notification';
import {EndpointError} from '@vaadin/flow-frontend/Connect';
import * as SnippetEndpoint from "../../generated/SnippetEndpoint";

@customElement('new-snippet-dialog')
export class NewSnippetDialog extends LitElement {
    @property({type: Boolean}) opened = false;

    public cbSave!: CallbackFunction;
    public cbCancel!: CallbackFunction;

    private _boundDialogRenderer = this._dialogRenderer.bind(this);

    private binder = new Binder<Snippet, SnippetModel>(this, SnippetModel);

    render() {
        return html`
            <vaadin-dialog
                    .opened=${this.opened}
                    .renderer=${this._boundDialogRenderer}
                    modeless
                    resizable
                    draggable
                    @opened-changed="${this._onOpenedChanged}"
            ></vaadin-dialog>
        `;
    }


    _dialogRenderer(root: HTMLElement) {
        render(
            html`
                <h2>Insert new snippet</h2>
                <vaadin-form-layout>
                    <vaadin-text-field
                            label="Content"
                            id="content"
                            ...="${field(this.binder.model.content)}"
                    ></vaadin-text-field>
                    <vaadin-text-field
                            label="Description"
                            id="description"
                            ...="${field(this.binder.model.description)}"
                    ></vaadin-text-field>
                </vaadin-form-layout>
                
                <vaadin-button @click=${this._saveClicked} theme="primary">Save</vaadin-button>
                <vaadin-button @click=${this._cancelClicked}>Cancel</vaadin-button>
            `,
            root,
            {eventContext: this} // bind event listener properly
        );
    }

    _onOpenedChanged(e: CustomEvent) {
        // upward property binding
        this.opened = e.detail.value;
    }

    _saveClicked() {
        this.save()
        this.opened = false;
        if (this.cbSave) {
            this.cbSave();
        }
    }

    _cancelClicked() {
        this.opened = false;
        if (this.cbCancel) {
            this.cbCancel();
        }
    }

    public showDialog(cb: () => void) {
        this.cbSave = cb;
        this.binder.read(this.createNewEntity());
        this.opened = true;
    }

    protected createNewEntity(): Snippet {
        return {
            creatorId: store.sessionUser.id
        }
    }

    private async save() {
        try {
            await this.binder.submitTo(SnippetEndpoint.update);
            showNotification(`Snippet stored succesfully.`, {position: 'bottom-start'});
        } catch (error) {
            if (error instanceof EndpointError) {
                showNotification('Server error. ' + error.message, {position: 'bottom-start'});
            } else {
                throw error;
            }
        }
    }
}
