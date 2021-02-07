import { Flow } from '@vaadin/flow-frontend/Flow';
import { isLoggedIn, logout } from './auth';
import { Router, Context, Commands } from '@vaadin/router';

const { serverSideRoutes } = new Flow({
  imports: () => import('../target/frontend/generated-flow-imports'),
});

export const routes = [
  // for client-side, place routes below (more info https://vaadin.com/docs/v18/flow/typescript/creating-routes.html)
  {
    path: '/login',
    component: 'login-view',
    action: async () => {
      await import ('./views/login/login-view');
    },
  },
  // Logging out is handled by Spring Security: it handles HTTP GET requests to
  // /logout and redirects to /login?logout in response.
  // For that a "Logout" button should be an regular <a> tag (see main-layout.ts):
  //    `<a href="/logout" router-ignore>Log out</a>`
  //
  // In order to implement logging out on the client-side (e.g. in order to avoid
  // a full page reload), it would require a `/logout` route like the one below.
  // In that case a "Logout" button should an in-app link like
  //    `<a href="/logout">Log out</a>`
  {
    path: '/logout',
    action: async (_: Context, commands: Commands) => {
      await logout();
      return commands.redirect('/');
    }
  },
  {
    path: '/',
    component: 'main-view',

    action: async (_: Router.Context, commands: Router.Commands) => {
      await import('./views/main/main-view');
      if (!isLoggedIn()) {
        return commands.redirect('/login');
      }
      return undefined;
    },
    children: [
      {
        path: '',
        component: 'snippet-view',
        action: async () => {
          await import('./views/snippet/snippet-view');
        },
      },
      {
        path: 'user',
        component: 'user-view',
        action: async () => {
          await import('./views/user/user-view');
        },
      },
      {
        path: 'user-detail',
        component: 'user-detail-view',
        action: async () => {
          await import('./views/user/user-detail-view');
        },
      },
      {
        path: 'tag',
        component: 'tag-view',
        action: async () => {
          await import('./views/tag/tag-view');
        },
      },
      {
        path: 'intent',
        component: 'intent-view',
        action: async () => {
          await import('./views/intent/intent-view');
        },
      },
      {
        path: 'snippet',
        component: 'snippet-view',
        action: async () => {
          await import('./views/snippet/snippet-view');
        },
      },
      {
        path: 'project',
        component: 'project-view',
        action: async () => {
          await import('./views/project/project-view');
        },
      },
      // for server-side, the next magic line sends all unmatched routes:
      ...serverSideRoutes, // IMPORTANT: this must be the last entry in the array
    ],
  },
];
