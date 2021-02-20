
import { CSSModule } from '@vaadin/flow-frontend/css-utils';
import { AppLayoutElement } from '@vaadin/vaadin-app-layout/src/vaadin-app-layout';
import '@vaadin/vaadin-app-layout/theme/lumo/vaadin-app-layout';
import '@vaadin/vaadin-app-layout/vaadin-drawer-toggle';
import '@vaadin/vaadin-tabs/theme/lumo/vaadin-tab';
import '@vaadin/vaadin-tabs/theme/lumo/vaadin-tabs';
import { customElement, html, property, query} from 'lit-element';
import { router } from '../../index';
import '@vaadin/vaadin-menu-bar';
import '@vaadin/vaadin-context-menu';
import {MenuBarElement} from "@vaadin/vaadin-menu-bar";
import {MobxLitElement} from "@adobe/lit-mobx";
import {store, MenuTab} from "../../store";
import {switchTheme} from "../utils/theme-utils";
import {Router} from "@vaadin/router";
import styles from './main-view.css'
import '../snippet/new-snippet-dialog'
import {NewSnippetDialog} from "../snippet/new-snippet-dialog";
import * as SnippetEndpoint from '../../generated/SnippetEndpoint';


@customElement('main-view')
export class MainView extends MobxLitElement {
  @property({ type: Object }) location = router.location;

  @query('#new_snippet_dlg')
  private newSnippetDialog!: NewSnippetDialog;

  @query('#main_menu')
  private mainMenu!: MenuBarElement;

  @query('#new_snippet_item')
  private newSnippetItem!: HTMLElement;

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

  baseMenuTabs: MenuTab[] = [
    { route: 'snippet', name: 'Snippets' },
  ];

  @property({ type: Array }) menuTabs2: MenuTab[] = [];

  private allNamedRoutes: MenuTab[] = [
    { route: 'snippet', name: 'Snippets' },
    { route: '', name: 'Snippets' },
    { route: 'user', name: 'Users' },
    { route: 'user-detail', name: 'User Settings' },
    { route: 'tag', name: 'Tags' },
    { route: 'intent', name: 'Intent' },
    { route: 'project', name: 'Projects' }
  ];


  @property({ type: String }) projectName = '';

  static get styles() {
    return [
      CSSModule('lumo-typography'),
      CSSModule('lumo-color'),
      CSSModule('app-layout'),
      styles
    ];
  }

  render() {
    return html`
      <new-snippet-dialog id="new_snippet_dlg"></new-snippet-dialog>
      <vaadin-app-layout primary-section="drawer">
        <header slot="navbar" theme="dark">
          <vaadin-drawer-toggle></vaadin-drawer-toggle>
          <h1><div style="padding-right: 0.8em;">${this.getSelectedTabName(this.allNamedRoutes)}</div></h1>
          <vaadin-menu-bar id="main_menu"></vaadin-menu-bar>
          <div style="display: none";>
            <vaadin-item id="user_menu_item"><iron-icon style="width: 18px; color:${this.getAvatarColor()};" icon="${this.getAvatar()}"></iron-icon><span style="padding-left: 0.35em;">${this.getUsername()}</span></vaadin-item>
            <vaadin-item @click="${this.newSnippet}" id="new_snippet_item"><iron-icon style="padding-right: 1em;" icon="vaadin:plus-circle"></iron-icon>New</vaadin-item>
            <vaadin-item @click="${this.editProjects}" id="edit_projects_item"><iron-icon style="padding-right: 1em;" icon="vaadin:archive"></iron-icon>Projects</vaadin-item>
            <vaadin-item @click="${this.editTags}" id="edit_tags_item"><iron-icon style="padding-right: 1em;" icon="vaadin:bullets"></iron-icon>Tags</vaadin-item>
            <vaadin-item @click="${this.editIntents}" id="edit_intents_item"><iron-icon style="padding-right: 1em;" icon="vaadin:automation"></iron-icon>Intents</vaadin-item>
            <vaadin-item @click="${this.editUsers}" id="edit_users_item"><iron-icon style="padding-right: 1em;" icon="vaadin:female"></iron-icon>Edit Users</vaadin-item>
            <vaadin-item @click="${this.editUserDetail}" id="user_detail_item"><iron-icon style="padding-right: 1em;" icon="vaadin:tools"></iron-icon>User Settings</vaadin-item>
            <vaadin-item @click="${this.logout}" id="logout_item"><iron-icon style="padding-right: 1em;" icon="vaadin:exit"></iron-icon>Logout</vaadin-item>
          </div>
        </header>

        <div slot="drawer">
          <div id="logo" style="cursor: pointer;" @click="${this.mainLogoClicked}">
            <img src="images/colibri.svg" alt="${this.projectName} logo" />
          </div>
          <hr />
          <vaadin-tabs orientation="vertical" theme="minimal" id="tabs" .selected="${this.getIndexOfSelectedTab()}">
            ${store.menuTabs.map(
              (menuTab) => {
                return html`
                <vaadin-tab>
                  <a href="${router.urlForPath(menuTab.route, menuTab.params)}" tabindex="-1">${menuTab.name}</a>
                </vaadin-tab>
              ` }
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
    const index = this.allNamedRoutes.findIndex((menuTab) => this.isCurrentLocation(menuTab.route));

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
      tabName = '';
    }
    return tabName;
  }

  async firstUpdated() {
    let menuItems = [
      {
        component: this.newSnippetItem
      },
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
    this.menuTabs2 = await this.recalcMenuTabs();
  }

  private editProjects() {
    Router.go('/project');
  }

  private editTags() {
    Router.go('/tag');
  }

  private editIntents() {
    Router.go('/intent');
  }

  private editUsers() {
    Router.go('/user');
  }

  private editUserDetail() {
    Router.go('/user-detail');
  }

  private logout() {
    Router.go('/logout');
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

  private async recalcMenuTabs() {
    const newMenuTabs: MenuTab[] = [...this.baseMenuTabs];

    const promises = new Array<Promise<void>>();
    const counts = new Map();

    const promise = SnippetEndpoint.count().then(c => {
      counts.set('', c);
    });
    promises.push(promise);

    store.projects.map( item => {
      const projectId = store.projectByName(item.project);
      if(projectId) {
        const promise = SnippetEndpoint.countForProjectId(projectId.id).then(c => {
          counts.set(item.project, c);
        });
        promises.push(promise);
      }
    });
    await Promise.all(promises);

    const count = counts.get('');
    newMenuTabs[0].name = 'Snippets' +  (count && count>0 ? ' ['+count+']' : '');

    store.projects.map( item => {
       const count = counts.get(item.project);
       newMenuTabs.push( {
        name: item.project + (count && count>0 ? ' ['+count+']' : ''),
        route: "/snippet/:project",
        params: {'project': item.project}
      }  ) });

    return newMenuTabs;
  }

  private execSavedNewSnippet() {
    // nothing to do
  }

  private newSnippet() {
    this.newSnippetDialog.showDialog(this.execSavedNewSnippet.bind(this));
  }

  private mainLogoClicked() {
    Router.go('/');
  }
}
