import '@polymer/iron-icon';

import {CSSModule} from '@vaadin/flow-frontend/css-utils';
import '@vaadin/vaadin-button/vaadin-button';
import '@vaadin/vaadin-form-layout/vaadin-form-layout';
import '@vaadin/vaadin-grid/vaadin-grid-sort-column';
import '@vaadin/vaadin-icons';
import '@vaadin/vaadin-ordered-layout/vaadin-horizontal-layout';
import '@vaadin/vaadin-split-layout/vaadin-split-layout';
import '@vaadin/vaadin-text-field';
import '@vaadin/vaadin-combo-box';
import '@vaadin/vaadin-text-field/vaadin-email-field';
import '@vaadin/vaadin-icons';
import '@vaadin/vaadin-checkbox';
import {Binder, field} from '@vaadin/form';
import UserDetailDto from '../../generated/com/overwhale/colibri_so/frontend/dto/UserDetailDto';
import UserDetailDtoModel from '../../generated/com/overwhale/colibri_so/frontend/dto/UserDetailDtoModel';
import * as UserDetailEndpoint from '../../generated/UserDetailEndpoint';
import styles from './user-detail-view.css';

import {customElement, html, property} from 'lit-element';
import {ComboBoxElement, ComboBoxItemModel} from "@vaadin/vaadin-combo-box";

import {showNotification} from '@vaadin/flow-frontend/a-notification';
import {EndpointError} from '@vaadin/flow-frontend/Connect';
import {store} from "../../store";
import {switchTheme} from "../utils/theme-utils";
import {MobxLitElement} from "@adobe/lit-mobx";

enum EditMode {EDIT, INSERT};

const DFLT_SELECTED_COLOR = '#ffffff';

@customElement('user-detail-view')
export class UserDetailView extends MobxLitElement {
    private binder = new Binder<UserDetailDto, UserDetailDtoModel>(this, UserDetailDtoModel);

    @property({type: Array})
    private uiThemeItems: string[] = ['light', 'dark'];

    @property({type: Array})
    private avatarComboItems: string[] = [];

    @property({type: Array})
    private avatarColorItems: string[] = ['#c21807', '#e0115f', '#c64b8c', '#b660cd', '#ec5578', '#f64a8a', '#81007f', '#8d4585', '#7987c5', '#fd6a02',
    '#fce205', '#eb9605', '#effd5f', '#98fb98', '#2e8b57', '#4f7942', '#29ab87', '#808588', '#4682b4', '#0080fe', '#57a0d2', '#1c2951', '#4b3619', '#4b382a'];



    @property({type: String})
    private selectedColor = DFLT_SELECTED_COLOR;

    private editMode = EditMode.INSERT;
    private currUserId: string = '';

    static get styles() {
        return [CSSModule('lumo-typography'), styles];
    }

    render() {
        return html`
            <vaadin-split-layout class="full-size">
                <div id="editor-layout">
                    <div id="editor">
                        <vaadin-form-layout>
                            <vaadin-email-field
                                    label="Email"
                                    id="email"
                                    ...="${field(this.binder.model.email)}"
                            ></vaadin-email-field>
                            <vaadin-text-field
                                    label="Full name"
                                    id="fullName"
                                    ...="${field(this.binder.model.fullName)}"
                            ></vaadin-text-field>

                            <vaadin-combo-box label="Avatar" .items="${this.avatarComboItems}" 
                                              .renderer="${this.avatarItemRenderer}"
                                              id="avatar"
                                              .color="${this.selectedColor}"
                                              ...="${field(this.binder.model.avatar)}"
                                              ></vaadin-combo-box>
                            <vaadin-combo-box label="Avatar color" .items="${this.avatarColorItems}"
                                              .renderer="${this.avatarColorItemRenderer}"
                                              id="avatarColor"
                                              @change="${this.avatarColorChanged}"
                                              ...="${field(this.binder.model.avatarColor)}"
                            ></vaadin-combo-box>
                            <vaadin-combo-box label="UI Theme" .items="${this.uiThemeItems}"
                                              id="uiTheme"
                                              @change="${this.uiThemeValueChanged}"
                                              ...="${field(this.binder.model.uiTheme)}"    
                            ></vaadin-combo-box>
                            <vaadin-checkbox
                                    label="Async table refresh" 
                                    id="asyncTableRefresh"
                                    ...="${field(this.binder.model.asyncTableRefresh)}"
                            >Async table refresh
                            </vaadin-checkbox>

                            
                        </vaadin-form-layout>
                    </div>

                    <vaadin-horizontal-layout id="button-layout" theme="spacing">
                        <vaadin-button theme="primary" @click="${this.save}">Save</vaadin-button>
                        <vaadin-button theme="tertiary" @click="${this.cancel}">Cancel</vaadin-button>
                    </vaadin-horizontal-layout>
                </div>
            </vaadin-split-layout>
        `;
    }

    private async save() {
        try {
            const userDetail = await this.binder.submitTo(this.updateEntity);
            if(userDetail) {
                this.publishChangedUserDetails(userDetail);
            }
            showNotification(`User Settings stored.`, {position: 'bottom-start'});
        } catch (error) {
            if (error instanceof EndpointError) {
                showNotification('Server error. ' + error.message, {position: 'bottom-start'});
            } else {
                throw error;
            }
        }
    }

    protected updateEntity(entity: UserDetailDto): Promise<UserDetailDto> {
        if(this.editMode==EditMode.INSERT) {
            entity.userId = this.currUserId;
            entity.creationTime = new Date().toISOString();
        }
        else {
            entity.lastChangedTime =new Date().toISOString();
        }
        return UserDetailEndpoint.update(entity);
    }

    private async publishChangedUserDetails(entity: UserDetailDto) {
        store.sessionUserDetail = entity;
        if(entity && entity.uiTheme) {
            switchTheme(entity.uiTheme);
        }
    }

    private async cancel() {
      this.refreshUserDetail();
    }

    private async refreshUserDetail() {
        const userInfo = store.sessionUserDetail;
        if(userInfo) {
            this.binder.read(userInfo);
            if(userInfo.avatarColor) {
                this.selectedColor = userInfo.avatarColor;
            }
            else {
                this.selectedColor = DFLT_SELECTED_COLOR;
            }
            this.editMode = EditMode.EDIT;
        }
        else {
            this.binder.clear();
            this.editMode = EditMode.INSERT;
            this.selectedColor = DFLT_SELECTED_COLOR;
        }
    }

    async connectedCallback() {
        super.connectedCallback();
        this.refreshUserDetail();

        // read names of all available vaadin-icons
        document.head
            .querySelector('iron-iconset-svg[name="vaadin"]')!
            .querySelector('svg')!.querySelector("defs")!
            .querySelectorAll("g")!
            .forEach((icon) => {
                this.avatarComboItems.push( icon.id );
            });
    }

    avatarItemRenderer = (root: HTMLElement, _comboBox: ComboBoxElement, model: ComboBoxItemModel) => {
        const iconName = model.item as string;
        const iconId = 'vaadin:'+iconName;
        root.innerHTML = `<div style="display: flex;">
                        <iron-icon style="width: 18px; color:${this.selectedColor};" icon="${iconId}"></iron-icon>
                        <div style="margin-left: 0.5em;">
                        ${iconName}</div>
                       </div>`;
    }

    avatarColorItemRenderer = (root: HTMLElement, _comboBox: ComboBoxElement, model: ComboBoxItemModel) => {
        const color = model.item as string;
        root.innerHTML = `<div style="display: flex;">
                        <iron-icon style="width: 18px; color:${color};" icon="vaadin:circle"></iron-icon>
                        <div style="margin-left: 0.5em;">
                        ${color}</div>
                       </div>`;
    }

    uiThemeValueChanged = (e: Event) => {
        const newValue = (e.target as HTMLInputElement).value;
        if(newValue) {
            switchTheme(newValue);
        }
    }

    avatarColorChanged = (e: Event) => {
        const newValue = (e.target as HTMLInputElement).value;
        if (newValue) {
            this.selectedColor = newValue;
        }
    }
}


