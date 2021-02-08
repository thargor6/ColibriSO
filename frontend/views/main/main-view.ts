
import { CSSModule } from '@vaadin/flow-frontend/css-utils';
import { AppLayoutElement } from '@vaadin/vaadin-app-layout/src/vaadin-app-layout';
import '@vaadin/vaadin-app-layout/theme/lumo/vaadin-app-layout';
import '@vaadin/vaadin-app-layout/vaadin-drawer-toggle';
import '@vaadin/vaadin-tabs/theme/lumo/vaadin-tab';
import '@vaadin/vaadin-tabs/theme/lumo/vaadin-tabs';
import {css, customElement, html, property, query} from 'lit-element';
import { router } from '../../index';
import '@vaadin/vaadin-menu-bar';
import '@vaadin/vaadin-context-menu';
import {MenuBarElement} from "@vaadin/vaadin-menu-bar";
import {MobxLitElement} from "@adobe/lit-mobx";
import {store} from "../../store";
import {switchTheme} from "../utils/theme-utils";

interface MenuTab {
  route: string;
  name: string;
}

@customElement('main-view')
export class MainView extends MobxLitElement {
  @property({ type: Object }) location = router.location;


  @query('#main_menu')
  private mainMenu!: MenuBarElement;

  @query('#edit_projects_item')
  private editProjectsItem!: HTMLElement;

  @query('#user_menu_item')
  private userMenuItem!: HTMLElement;

  @query('#edit_tags_item')
  private editTagsItem!: HTMLElement;

  @query('#edit_intents_item')
  private editIntentsItem!: HTMLElement;

  @query('#edit_users_item')
  private editUsersItem!: HTMLElement;

  @query('#user_detail_item')
  private userDetailItem!: HTMLElement;

  @query('#logout_item')
  private logoutItem!: HTMLElement;

  @property({ type: Array }) baseMenuTabs: MenuTab[] = [
    { route: 'snippet', name: 'Snippets' },
  ];

  @property({ type: String }) projectName = '';

  static get styles() {
    return [
      CSSModule('lumo-typography'),
      CSSModule('lumo-color'),
      CSSModule('app-layout'),
      css`
        :host {
          display: block;
          height: 100%;
        }

        header {
          align-items: center;
          box-shadow: var(--lumo-box-shadow-s);
          display: flex;
          height: var(--lumo-size-xl);
          width: 100%;
        }

        header h1 {
          font-size: var(--lumo-font-size-l);
          margin: 0;
        }

        header img {
          border-radius: 50%;
          height: var(--lumo-size-s);
          margin-left: auto;
          margin-right: var(--lumo-space-m);
          overflow: hidden;
          background-color: var(--lumo-contrast);
        }

        vaadin-app-layout[dir='rtl'] header img {
          margin-left: var(--lumo-space-m);
          margin-right: auto;
        }

        #logo {
          align-items: center;
          box-sizing: border-box;
          display: flex;
          padding: var(--lumo-space-s) var(--lumo-space-m);
        }

        #logo img {
          height: calc(var(--lumo-size-l) * 2.5);
        }

        #logo span {
          font-size: var(--lumo-font-size-xl);
          font-weight: 600;
          margin: 0 var(--lumo-space-s);
        }

        vaadin-tab {
          font-size: var(--lumo-font-size-s);
          height: var(--lumo-size-l);
          font-weight: 600;
          color: var(--lumo-body-text-color);
        }

        vaadin-tab:hover {
          background-color: var(--lumo-contrast-5pct);
          text-decoration: none;
        }

        vaadin-tab[selected] {
          background-color: var(--lumo-primary-color-10pct);
          color: var(--lumo-primary-text-color);
        }

        hr {
          margin: 0;
        }
      `,
    ];
  }

  render() {
    return html`
      <vaadin-app-layout primary-section="drawer">
        <header slot="navbar" theme="dark">
          <vaadin-drawer-toggle></vaadin-drawer-toggle>
          <h1>${this.getSelectedTabName(this.getMenuTabs())} / ${store.projects.length}</h1>
          <vaadin-menu-bar id="main_menu"></vaadin-menu-bar>
          <div style="display: none";>
            <vaadin-item id="user_menu_item"><iron-icon style="width: 18px; color:${this.getAvatarColor()};" icon="${this.getAvatar()}"></iron-icon><span style="padding-left: 0.35em;">${this.getUsername()}</span></vaadin-item>

            <vaadin-item @click="${this.editProjects}" id="edit_projects_item">Projects</vaadin-item>
            <vaadin-item @click="${this.editTags}" id="edit_tags_item">Tags</vaadin-item>
            <vaadin-item @click="${this.editIntents}" id="edit_intents_item">Intents</vaadin-item>
            <vaadin-item @click="${this.editUsers}" id="edit_users_item">Edit Users</vaadin-item>
            <vaadin-item @click="${this.editUserDetail}" id="user_detail_item">User Settings</vaadin-item>
            <vaadin-item @click="${this.logout}" id="logout_item">Logout</vaadin-item>
          </div>
        </header>

        <div slot="drawer">
          <div id="logo">
            <img src="images/colibri.svg" alt="${this.projectName} logo" />
          </div>
          <hr />
          <vaadin-tabs orientation="vertical" theme="minimal" id="tabs" .selected="${this.getIndexOfSelectedTab()}">
            ${this.getMenuTabs().map(
              (menuTab) => html`
                <vaadin-tab>
                  <a href="${router.urlForPath(menuTab.route)}" tabindex="-1">${menuTab.name}</a>
                </vaadin-tab>
              `
            )}
          </vaadin-tabs>
        </div>
        <slot></slot>
      </vaadin-app-layout>
    `;
  }

  private _routerLocationChanged() {
    AppLayoutElement.dispatchCloseOverlayDrawerEvent();
  }

  async connectedCallback() {
    super.connectedCallback();
    window.addEventListener('vaadin-router-location-changed', this._routerLocationChanged);
    this.projectName = 'ColibriSO';
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    window.removeEventListener('vaadin-router-location-changed', this._routerLocationChanged);
  }


  private isCurrentLocation(route: string): boolean {
    return router.urlForPath(route) === this.location.getUrl();
  }

  private getIndexOfSelectedTab(): number {
    const index = this.getMenuTabs().findIndex((menuTab) => this.isCurrentLocation(menuTab.route));

    // Select first tab if there is no tab for home in the menu
    if (index === -1 && this.isCurrentLocation('')) {
      return 0;
    }

    return index;
  }

  private getSelectedTabName(menuTabs: MenuTab[]): string {
    const currentTab = menuTabs.find((menuTab) => this.isCurrentLocation(menuTab.route));
    let tabName = '';
    if (currentTab) {
      tabName = currentTab.name;
    } else {
      tabName = 'Users';
    }
    return tabName;
  }

  menuItemClicked(e: Event) {
    console.log('Clicked: ' + (e.target as Element).textContent!);
  }

  menuItemSelected(e:any) {
 //   const item = e.target;
    console.log('Selected: '+e);
  }


  firstUpdated() {
    let menuItems = [
      {
        text: 'Edit',
        children: [
          {component: this.editProjectsItem},
          {component: this.editTagsItem},
          {component: this.editIntentsItem}
        ]
      },
      {
        text: 'Administration',
        children: [
          {component: this.editUsersItem},
        ]
      },
      {
        component: this.userMenuItem,
        children: [
          {component: this.userDetailItem},
          {component: this.logoutItem},
        ]
      },
    ];
    this.mainMenu.items = menuItems;
    const userDetail = store.sessionUserDetail;
    if(userDetail && userDetail.uiTheme) {
      switchTheme(userDetail.uiTheme);
    }
  }

  private editProjects() {
    window.location.assign('/project');
  }

  private editTags() {
    window.location.assign('/tag');
  }

  private editIntents() {
    window.location.assign('/intent');
  }

  private editUsers() {
    window.location.assign('/user');
  }

  private editUserDetail() {
    window.location.assign('/user-detail');
  }

  private logout() {
    window.location.assign('/logout');
  }

  private getAvatarColor() {
    if(store.sessionUserDetail && store.sessionUserDetail!.avatarColor) {
      return store.sessionUserDetail!.avatarColor;
    }
    else {
      return '#ffffff';
    }
  }

  private getAvatar() {
    if(store.sessionUserDetail && store.sessionUserDetail!.avatarColor) {
      return 'vaadin:'+store.sessionUserDetail!.avatar;
    }
    else {
      return 'vaadin:circle';
    }
  }


  private getUsername() {
    if(store.sessionUser && store.sessionUser!.username) {
      return store.sessionUser!.username;
    }
    else {
      return "";
    }
  }

  private getMenuTabs() {
    const newMenuTabs: MenuTab[] = [...this.baseMenuTabs];

    store.projects.map( item => {
      newMenuTabs.push( { name: item.project,
        // todo encode URL
        route: "/snippet?project="+item.project }  ) });

    return newMenuTabs;
  }
}
