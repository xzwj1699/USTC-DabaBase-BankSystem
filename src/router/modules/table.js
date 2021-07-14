/** When your routing table is too long, you can split it into small modules **/

import Layout from '@/layout'

const tableRouter = {
  path: '/table',
  component: Layout,
  redirect: '/table/guest',
  name: 'Table',
  meta: {
    title: 'Table',
    icon: 'table'
  },
  children: [
    {
      path: 'guest',
      component: () => import('@/views/table/guest'),
      name: 'Guest',
      meta: { title: 'Guest' }
    },
    {
      path: 'account',
      component: () => import('@/views/table/account'),
      name: 'Account',
      meta: { title: 'Account' }
    },
    {
      path: 'loan',
      component: () => import('@/views/table/loan'),
      name: 'Loan',
      meta: { title: 'Loan' }
    },
    {
      path: 'statistics',
      component: () => import('@/views/table/statistics'),
      name: 'Statistics',
      meta: { title: 'Statistics' }
    }
  ]
}
export default tableRouter
