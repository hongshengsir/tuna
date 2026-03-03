<template>
  <div class="markdown-viewer">
    <!-- 文件列表侧边栏 -->
    <div class="sidebar">
      <a-card title="Markdown文件" :bordered="false" style="height: 100%">
        <div class="sidebar-header">
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索文件..."
            @search="handleSearch"
            style="margin-bottom: 16px"
          />
          <a-button type="link" @click="refreshFileList" :loading="loadingFiles">
            <template #icon><ReloadOutlined /></template>
            刷新
          </a-button>
        </div>
        
        <a-list
          :data-source="filteredFiles"
          :loading="loadingFiles"
          size="small"
          style="height: calc(100vh - 200px); overflow-y: auto"
        >
          <template #renderItem="{ item: file }">
            <a-list-item 
              :class="{ 'active': activeFile?.path === file.path }"
              @click="selectFile(file)"
            >
              <a-list-item-meta>
                <template #title>
                  <div style="display: flex; align-items: center; gap: 8px">
                    <FileTextOutlined style="color: #1890ff" />
                    <span style="font-size: 12px">{{ file.name }}</span>
                  </div>
                </template>
                <template #description>
                  <div style="font-size: 10px; color: #999">
                    <div>{{ file.relative_path }}</div>
                    <div>大小: {{ formatFileSize(file.size) }} • 修改: {{ formatTime(file.modified_time) }}</div>
                  </div>
                </template>
              </a-list-item-meta>
            </a-list-item>
          </template>
          
          <template #empty>
            <a-empty description="暂无Markdown文件" :image="simpleImage" />
          </template>
        </a-list>
      </a-card>
    </div>

    <!-- 内容区域 -->
    <div class="content">
      <a-card :title="activeFile ? activeFile.name : 'Markdown查看器'" :bordered="false" style="height: 100%">
        <template #extra>
          <a-space>
            <a-button @click="copyContent" :disabled="!activeFile">
              <template #icon><CopyOutlined /></template>
              复制
            </a-button>
            <a-button @click="downloadFile" :disabled="!activeFile">
              <template #icon><DownloadOutlined /></template>
              下载
            </a-button>
          </a-space>
        </template>
        
        <div v-if="loadingContent" class="loading-container">
          <a-spin size="large" />
          <div style="margin-top: 16px">正在加载文件内容...</div>
        </div>
        
        <div v-else-if="activeFile && markdownContent" class="markdown-content">
          <div class="markdown-rendered" v-html="renderedContent"></div>
        </div>
        
        <div v-else class="empty-container">
          <a-empty description="请从左侧选择文件查看内容">
            <template #image>
              <FileTextOutlined style="font-size: 64px; color: #d9d9d9" />
            </template>
          </a-empty>
        </div>
      </a-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { marked } from 'marked'
import { useClipboard } from '@vueuse/core'
import { 
  FileTextOutlined, 
  ReloadOutlined, 
  CopyOutlined, 
  DownloadOutlined 
} from '@ant-design/icons-vue'

// 类型定义
interface MarkdownFile {
  name: string
  path: string
  relative_path: string
  size: number
  modified_time: number
  directory: string
}

// 响应式数据
const searchKeyword = ref('')
const loadingFiles = ref(false)
const loadingContent = ref(false)
const files = ref<MarkdownFile[]>([])
const activeFile = ref<MarkdownFile | null>(null)
const markdownContent = ref('')
const { copy } = useClipboard()

// 计算属性
const filteredFiles = computed(() => {
  if (!searchKeyword.value) return files.value
  return files.value.filter(file => 
    file.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
    file.relative_path.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

const renderedContent = computed(() => {
  if (!markdownContent.value) return ''
  return marked.parse(markdownContent.value)
})

// 方法
const loadFileList = async () => {
  loadingFiles.value = true
  try {
    const response = await fetch('http://localhost:5000/api/markdown/files')
    const result = await response.json()
    
    if (result.success) {
      files.value = result.files
    } else {
      message.error('获取文件列表失败')
    }
  } catch (error) {
    message.error('网络错误，请检查API服务器是否运行')
  } finally {
    loadingFiles.value = false
  }
}

const selectFile = async (file: MarkdownFile) => {
  activeFile.value = file
  loadingContent.value = true
  
  try {
    const response = await fetch(`http://localhost:5000/api/markdown/read/${encodeURIComponent(file.path)}`)
    const result = await response.json()
    
    if (result.success) {
      markdownContent.value = result.content
    } else {
      message.error('读取文件失败')
      markdownContent.value = ''
    }
  } catch (error) {
    message.error('网络错误，请检查API服务器是否运行')
    markdownContent.value = ''
  } finally {
    loadingContent.value = false
  }
}

const refreshFileList = () => {
  loadFileList()
}

const handleSearch = () => {
  // 搜索逻辑已在计算属性中处理
}

const copyContent = async () => {
  if (markdownContent.value) {
    await copy(markdownContent.value)
    message.success('内容已复制到剪贴板')
  }
}

const downloadFile = () => {
  if (!activeFile.value || !markdownContent.value) return
  
  const blob = new Blob([markdownContent.value], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = activeFile.value.name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  message.success('文件下载成功')
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatTime = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleString('zh-CN')
}

// 生命周期
onMounted(() => {
  loadFileList()
})

// 空状态图片
const simpleImage = '<svg width="64" height="41" viewBox="0 0 64 41" xmlns="http://www.w3.org/2000/svg"><g transform="translate(0 1)" fill="none" fill-rule="evenodd"><ellipse fill="#f5f5f5" cx="32" cy="33" rx="32" ry="7"></ellipse><g fill-rule="nonzero" stroke="#d9d9d9"><path d="M55 12.76L44.854 1.258C44.367.474 43.656 0 42.907 0H21.093c-.749 0-1.46.474-1.947 1.257L9 12.761V22h46v-9.24z"></path><path d="M41.613 15.931c0-1.605.994-2.93 2.227-2.931H55v18.137C55 33.26 53.68 35 52.05 35h-40.1C10.32 35 9 33.259 9 31.137V13h11.16c1.233 0 2.227 1.323 2.227 2.928v.022c0 1.605 1.005 2.901 2.237 2.901h14.752c1.232 0 2.237-1.308 2.237-2.913v-.007z" fill="#fafafa"></path></g></g></svg>'
</script>

<style scoped>
.markdown-viewer {
  display: flex;
  height: 100vh;
  background: #f0f2f5;
}

.sidebar {
  width: 400px;
  min-width: 300px;
  background: white;
  border-right: 1px solid #f0f0f0;
}

.content {
  flex: 1;
  min-width: 0;
  background: white;
}

.sidebar-header {
  display: flex;
  gap: 8px;
  align-items: center;
}

:deep(.ant-list-item) {
  cursor: pointer;
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  transition: all 0.3s;
}

:deep(.ant-list-item:hover) {
  background: #f5f5f5;
}

:deep(.ant-list-item.active) {
  background: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.empty-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 400px;
}

.markdown-content {
  height: calc(100vh - 120px);
  overflow-y: auto;
  padding: 16px;
}

.markdown-rendered {
  line-height: 1.6;
  color: #333;
}

.markdown-rendered h1,
.markdown-rendered h2,
.markdown-rendered h3,
.markdown-rendered h4,
.markdown-rendered h5,
.markdown-rendered h6 {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.25;
}

.markdown-rendered h1 {
  font-size: 2em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-rendered h2 {
  font-size: 1.5em;
  border-bottom: 1px solid #eaecef;
  padding-bottom: 0.3em;
}

.markdown-rendered p {
  margin-bottom: 16px;
}

.markdown-rendered ul,
.markdown-rendered ol {
  margin-bottom: 16px;
  padding-left: 2em;
}

.markdown-rendered code {
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.markdown-rendered pre {
  background: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  margin-bottom: 16px;
}

.markdown-rendered blockquote {
  border-left: 4px solid #dfe2e5;
  padding-left: 16px;
  margin-left: 0;
  color: #6a737d;
  margin-bottom: 16px;
}

.markdown-rendered table {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 16px;
}

.markdown-rendered th,
.markdown-rendered td {
  border: 1px solid #dfe2e5;
  padding: 6px 13px;
  text-align: left;
}

.markdown-rendered th {
  background: #f6f8fa;
  font-weight: 600;
}
</style>