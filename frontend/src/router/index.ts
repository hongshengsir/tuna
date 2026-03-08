import { createRouter, createWebHistory } from 'vue-router'
import WechatDownloader from '@/components/WechatDownloader.vue'
import WebArticleDownloader from '@/components/WebArticleDownloader.vue'
import MarkdownViewer from '@/components/MarkdownViewer.vue'
import UserLogin from '@/components/UserLogin.vue'
import UserManagement from '@/components/UserManagement.vue'
import authGuard from './guard'

const routes = [
  {
    path: '/',
    name: 'WechatDownloader',
    component: WechatDownloader
  },
  {
    path: '/web',
    name: 'WebArticleDownloader',
    component: WebArticleDownloader
  },
  {
    path: '/markdown',
    name: 'MarkdownViewer',
    component: MarkdownViewer
  },
  {
    path: '/login',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/users',
    name: 'UserManagement',
    component: UserManagement,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 添加路由守卫
router.beforeEach(authGuard)

export default router