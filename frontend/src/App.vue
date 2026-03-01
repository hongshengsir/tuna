<template>
  <div id="app">
    <a-layout style="min-height: 100vh">
      <a-layout-header style="background: #fff; padding: 0 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.1)">
        <div style="display: flex; align-items: center; height: 64px">
          <h1 style="margin: 0; color: #1890ff; font-size: 24px">
            🐟 微信文章下载工具
          </h1>
        </div>
      </a-layout-header>
      
      <a-layout-content style="padding: 24px">
        <WechatDownloader />
      </a-layout-content>
      
      <a-layout-footer style="text-align: center; padding: 16px">
        © 2024 微信文章下载工具 - 基于Vue 3 + TypeScript + Ant Design Vue
      </a-layout-footer>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import WechatDownloader from './components/WechatDownloader.vue'
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