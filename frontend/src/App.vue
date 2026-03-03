<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #fff; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
        <div style="display: flex; align-items: center; justify-content: space-between; height: 64px">
          <h1 style="margin: 0; color: #1890ff; font-size: 24px">
            🐟 微信文章下载工具
          </h1>
          
          <a-menu v-model:selectedKeys="currentRoute" mode="horizontal" style="border: none">
            <a-menu-item key="/" @click="navigateTo('/')">
              <template #icon><DownloadOutlined /></template>
              文章下载
            </a-menu-item>
            <a-menu-item key="/markdown" @click="navigateTo('/markdown')">
              <template #icon><FileTextOutlined /></template>
              Markdown查看器
            </a-menu-item>
          </a-menu>
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
import { ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { DownloadOutlined, FileTextOutlined } from '@ant-design/icons-vue'

const router = useRouter()
const route = useRoute()
const currentRoute = ref([route.path])

const navigateTo = (path: string) => {
  router.push(path)
}

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