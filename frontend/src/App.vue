<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #fff; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
        <div style="display: flex; align-items: center; justify-content: space-between; height: 64px">
          <h1 style="margin: 0; color: #1890ff; font-size: 24px">
            🐟 微信文章下载工具
          </h1>
          
          <div style="display: flex; align-items: center; gap: 24px">
            <a-menu v-model:selectedKeys="currentRoute" mode="horizontal" style="border: none">
              <a-menu-item key="/" @click="navigateTo('/')">
                <template #icon><DownloadOutlined /></template>
                文章下载
              </a-menu-item>
              <a-menu-item key="/markdown" @click="navigateTo('/markdown')">
                <template #icon><FileTextOutlined /></template>
                Markdown查看器
              </a-menu-item>
              <a-menu-item v-if="userStore.isAuthenticated" key="/users" @click="navigateTo('/users')">
                <template #icon><UserOutlined /></template>
                用户管理
              </a-menu-item>
            </a-menu>
            
            <!-- 用户状态显示 -->
            <div v-if="userStore.isAuthenticated && userStore.currentUser" style="display: flex; align-items: center; gap: 12px">
              <a-avatar style="background-color: #1890ff">
                {{ userStore.currentUser.username.charAt(0).toUpperCase() }}
              </a-avatar>
              <span style="color: #666">欢迎，{{ userStore.currentUser.username }}</span>
              <a-button type="link" @click="handleLogout" size="small">
                退出登录
              </a-button>
            </div>
            <div v-else style="display: flex; align-items: center; gap: 12px">
              <a-button type="primary" @click="navigateTo('/login')" size="small">
                登录
              </a-button>
              <a-button @click="navigateTo('/login')" size="small">
                注册
              </a-button>
            </div>
          </div>
        </div>
      </a-layout-header>
      
      <a-layout-content style="padding: 24px">
        <router-view />
      </a-layout-content>
      
      <a-layout-footer style="text-align: center; padding: 16px">
        © 2024 微信文章下载工具 - 基于Vue 3 + TypeScript + Ant Design Vue
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { DownloadOutlined, FileTextOutlined, UserOutlined } from '@ant-design/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const currentRoute = ref([route.path])

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  userStore.logout()
  message.success('退出登录成功')
  navigateTo('/')
}

// 页面加载时检查登录状态
onMounted(async () => {
  await userStore.checkAuth()
})

watch(() => route.path, (newPath) => {
  currentRoute.value = [newPath]
})
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

body {
  margin: 0;
  background-color: #f5f5f5;
}
</style>