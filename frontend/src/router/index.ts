import { createRouter, createWebHistory } from 'vue-router'
import WechatDownloader from '@/components/WechatDownloader.vue'
import MarkdownViewer from '@/components/MarkdownViewer.vue'

const routes = [
  {
    path: '/',
    name: 'WechatDownloader',
    component: WechatDownloader
  },
  {
    path: '/markdown',
    name: 'MarkdownViewer',
    component: MarkdownViewer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router