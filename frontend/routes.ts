import { Flow } from '@vaadin/flow-frontend/Flow';

const { serverSideRoutes } = new Flow({
  imports: () => import('../target/frontend/generated-flow-imports'),
});

export const routes = [
  // for client-side, place routes below (more info https://vaadin.com/docs/v18/flow/typescript/creating-routes.html)
  {
    path: '',
    component: 'main-view',
    action: async () => {
      await import('./views/main/main-view');
    },
    children: [
      {
        path: '',
        component: 'user-view',
        action: async () => {
          await import('./views/user/user-view');
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
