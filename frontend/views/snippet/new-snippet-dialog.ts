import {customElement, html, LitElement, property} from 'lit-element';
import {render} from 'lit-html';
import '@vaadin/vaadin-button/vaadin-button.js';
import '@vaadin/vaadin-date-picker/vaadin-date-picker.js';
import '@vaadin/vaadin-dialog/vaadin-dialog.js';
import '@vaadin/vaadin-combo-box';
import '@vaadin/vaadin-text-field/vaadin-text-area'
import {CallbackFunction} from '../utils/types';
import {Binder, field} from '@vaadin/form';
import Snippet from '../../generated/com/overwhale/colibri_so/domain/entity/Snippet';
import SnippetModel from '../../generated/com/overwhale/colibri_so/domain/entity/SnippetModel';
import {store} from "../../store";
import {showNotification} from '@vaadin/flow-frontend/a-notification';
import {EndpointError} from '@vaadin/flow-frontend/Connect';
import * as SnippetEndpoint from "../../generated/SnippetEndpoint";
import * as SnippetProjectEndpoint from "../../generated/SnippetProjectEndpoint";
import * as SnippetIntentEndpoint from "../../generated/SnippetIntentEndpoint";
import * as SnippetTagEndpoint from "../../generated/SnippetTagEndpoint";
import SnippetProject from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetProject";
import SnippetProjectModel from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetProjectModel";
import SnippetIntent from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetIntent";
import SnippetIntentModel from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetIntentModel";
import SnippetTag from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetTag";
import SnippetTagModel from "../../generated/com/overwhale/colibri_so/domain/entity/SnippetTagModel";

@customElement('new-snippet-dialog')
export class NewSnippetDialog extends LitElement {
    @property({type: Boolean}) opened = false;

    public cbSave!: CallbackFunction;
    public cbCancel!: CallbackFunction;

    private _boundDialogRenderer = this._dialogRenderer.bind(this);

    private snippetBinder = new Binder<Snippet, SnippetModel>(this, SnippetModel);
    private snippetProjectBinder = new Binder<SnippetProject, SnippetProjectModel>(this, SnippetProjectModel);
    private snippetIntentBinder = new Binder<SnippetIntent, SnippetIntentModel>(this, SnippetIntentModel);
    private snippetTagBinder1 = new Binder<SnippetTag, SnippetTagModel>(this, SnippetTagModel);
    private snippetTagBinder2 = new Binder<SnippetTag, SnippetTagModel>(this, SnippetTagModel);
    private snippetTagBinder3 = new Binder<SnippetTag, SnippetTagModel>(this, SnippetTagModel);


    render() {
        return html`
            <vaadin-dialog
                    .opened=${this.opened}
                    .renderer=${this._boundDialogRenderer}
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
                <div style="display: flex; flex-direction: row;">
                    <div style="flex-grow: 1; width: 50%; margin-right: 1.0em; display: flex; flex-direction: column;">
                        <vaadin-text-field
                                label="Description"
                                id="description"
                                ...="${field(this.snippetBinder.model.description)}"
                        ></vaadin-text-field>
                        <vaadin-text-area 
                                style="width: 100%; height: 80%;"
                                label="Content"
                                id="content"
                                ...="${field(this.snippetBinder.model.content)}"
                        ></vaadin-text-area>
                    </div>
                    <div style="flex-grow: 1; width: 25%;">
                        <vaadin-form-layout>
                            <vaadin-combo-box
                                    label="Project"
                                    id="project"
                                    ...="${field(this.snippetProjectBinder.model.projectId)}"
                                    .items="${store.projectNames}"
                            ></vaadin-combo-box>
                            <vaadin-combo-box
                                    label="Intent"
                                    id="intent"
                                    ...="${field(this.snippetIntentBinder.model.intentId)}"
                                    .items="${store.intentNames}"
                            ></vaadin-combo-box>

                            <vaadin-combo-box
                                    label="Tag 1"
                                    id="tag1"
                                    .items="${store.tagNames}"
                                    ...="${field(this.snippetTagBinder1.model.tagId)}"
                            ></vaadin-combo-box>


                            <vaadin-combo-box
                                    label="Tag 2"
                                    id="tag2"
                                    .items="${store.tagNames}"
                                    ...="${field(this.snippetTagBinder2.model.tagId)}"
                            ></vaadin-combo-box>

                            <vaadin-combo-box
                                    label="Tag 3"
                                    id="tag3"
                                    .items="${store.tagNames}"
                                    ...="${field(this.snippetTagBinder3.model.tagId)}"
                            ></vaadin-combo-box>
                            
                        </vaadin-form-layout>
                    </div>
                </div>
          
                
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

    async _saveClicked() {
        await this.save()
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
        this.snippetBinder.read({
            creatorId: store.sessionUser.id
        });
        this.snippetProjectBinder.read({});
        this.snippetIntentBinder.read({});
        this.snippetTagBinder1.read({});
        this.snippetTagBinder2.read({});
        this.snippetTagBinder3.read({});
        this.opened = true;
    }

    private async save() {
        try {
            const snippet: Snippet = await this.snippetBinder.submitTo(SnippetEndpoint.update) as Snippet;
            await this.snippetProjectBinder.submitTo( entity => {
                // hack: because object-comboboxes seem not to work yet, we must map the
                // caption to the id:
                if(entity.projectId) {
                    const project = store.projectByName(entity.projectId);
                    if(project) {
                        entity.projectId = project.id;
                        entity.snippetId = snippet.id;
                        SnippetProjectEndpoint.update(entity);
                    }
                }
                return new Promise((resolve) => { resolve(entity); });
            } );

            await this.snippetIntentBinder.submitTo( entity => {
                // hack: because object-comboboxes seem not to work yet, we must map the
                // caption to the id:
                if(entity.intentId) {
                    const intent = store.intentByName(entity.intentId);
                    if(intent) {
                        entity.intentId = intent.id;
                        entity.snippetId = snippet.id;
                        SnippetIntentEndpoint.update(entity);
                    }
                }
                return new Promise((resolve) => { resolve(entity); });
            } );

            await this.snippetTagBinder1.submitTo( entity => {
                // hack: because object-comboboxes seem not to work yet, we must map the
                // caption to the id:
                if(entity.tagId) {
                    const tag = store.tagByName(entity.tagId);
                    if(tag) {
                        entity.tagId = tag.id;
                        entity.snippetId = snippet.id;
                        SnippetTagEndpoint.update(entity);
                    }
                }
                return new Promise((resolve) => { resolve(entity); });
            } );

            await this.snippetTagBinder2.submitTo( entity => {
                // hack: because object-comboboxes seem not to work yet, we must map the
                // caption to the id:
                if(entity.tagId) {
                    const tag = store.tagByName(entity.tagId);
                    if(tag) {
                        entity.tagId = tag.id;
                        entity.snippetId = snippet.id;
                        SnippetTagEndpoint.update(entity);
                    }
                }
                return new Promise((resolve) => { resolve(entity); });
            } );

            await this.snippetTagBinder3.submitTo( entity => {
                // hack: because object-comboboxes seem not to work yet, we must map the
                // caption to the id:
                if(entity.tagId) {
                    const tag = store.tagByName(entity.tagId);
                    if(tag) {
                        entity.tagId = tag.id;
                        entity.snippetId = snippet.id;
                        SnippetTagEndpoint.update(entity);
                    }
                }
                return new Promise((resolve) => { resolve(entity); });
            } );
            store.refreshMenuTabs();
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
