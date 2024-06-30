import React from 'react';

const Configs = React.lazy(() => import('./pages/Configs/Configs'));

const routes = [
  {
    path: "/",
    exact: true,
    name: "",
  },
  {
      path: '/configs',
      name: 'Мои конфигурации',
      component: Configs
  },
];

export default routes;
