import {customElement, html, LitElement, property} from 'lit-element';
import {render} from 'lit-html';
import '@vaadin/vaadin-button/vaadin-button.js';
import '@vaadin/vaadin-date-picker/vaadin-date-picker.js';
import '@vaadin/vaadin-dialog/vaadin-dialog.js';
import {CallbackFunction} from '../utils/types';

@customElement('confirmation-dialog')
export class ConfirmationDialogElement extends LitElement {
    @property({type: Boolean}) opened = false;

    public message: string = '';
    public cbYes!: CallbackFunction;
    public cbNo!: CallbackFunction;

    private _boundDialogRenderer = this._dialogRenderer.bind(this);

    render() {
        return html`
            <vaadin-dialog
                    .opened=${this.opened}
                    .renderer=${this._boundDialogRenderer}
                    modeless
                    @opened-changed="${this._onOpenedChanged}"
            ></vaadin-dialog>
        `;
    }


    _dialogRenderer(root: HTMLElement) {
        render(
            html`
                <h3>${this.message}</h3>
                <vaadin-button @click=${this._yesClicked} theme="primary">Yes</vaadin-button>
                <vaadin-button @click=${this._noClicked} theme="primary">No</vaadin-button>
            `,
            root,
            {eventContext: this} // bind event listener properly
        );
    }

    _onOpenedChanged(e: CustomEvent) {
        // upward property binding
        this.opened = e.detail.value;
    }

    _yesClicked() {
        this.opened = false;
        if (this.cbYes) {
            this.cbYes();
        }
    }

    _noClicked() {
        this.opened = false;
        if (this.cbNo) {
            this.cbNo();
        }
    }

    public showDialog(cb: () => void) {
        this.cbYes = cb;
        this.opened = true;
    }
}
