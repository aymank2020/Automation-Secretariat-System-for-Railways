import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/pages/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('@/pages/Home.vue'),
    meta: { requiresAuth: true }
  },
  // Dashboard (الصفحة القديمة)
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard-home',
        component: () => import('@/pages/Dashboard.vue')
      },
      {
        path: 'documents',
        name: 'documents',
        component: () => import('@/pages/DocumentsList.vue')
      },
      {
        path: 'documents/new',
        name: 'document-new',
        component: () => import('@/pages/DocumentForm.vue')
      },
      {
        path: 'documents/:id/edit',
        name: 'document-edit',
        component: () => import('@/pages/DocumentForm.vue')
      },
      {
        path: 'documents/:id',
        name: 'document-detail',
        component: () => import('@/pages/DocumentDetails.vue')
      },
      {
        path: 'users',
        name: 'users',
        component: () => import('@/pages/UsersList.vue'),
        meta: { requiresAdmin: true }
      }
    ]
  },
  // الوارد
  {
    path: '/warid/new',
    name: 'warid-new',
    component: () => import('@/pages/WaridForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/warid/:id/edit',
    name: 'warid-edit',
    component: () => import('@/pages/WaridForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/warid/search',
    name: 'warid-search',
    component: () => import('@/pages/WaridSearch.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/warid/query',
    name: 'warid-query',
    component: () => import('@/pages/WaridQuery.vue'),
    meta: { requiresAuth: true }
  },
  // الصادر
  {
    path: '/sadir/new',
    name: 'sadir-new',
    component: () => import('@/pages/SadirForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sadir/:id/edit',
    name: 'sadir-edit',
    component: () => import('@/pages/SadirForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sadir/search',
    name: 'sadir-search',
    component: () => import('@/pages/SadirSearch.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/sadir/query',
    name: 'sadir-query',
    component: () => import('@/pages/SadirQuery.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = authStore.token

  if (to.meta.guest && token) {
    next('/home')
  } else if (to.meta.requiresAdmin && authStore.user?.seclevel !== 'admin') {
    next('/home')
  } else if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
