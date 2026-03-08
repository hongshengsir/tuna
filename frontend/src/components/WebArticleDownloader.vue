<template>
  <div class="web-article-downloader">
    <!-- 输入区域 -->
    <a-card title="网页文章下载" :bordered="false" style="margin-bottom: 24px">
      <a-space direction="vertical" style="width: 100%">
        <div>
          <a-textarea
            v-model:value="urlInput"
            placeholder="请输入网页文章链接，多个链接请用换行分隔"
            :rows="4"
            style="width: 100%"
          />
        </div>
        
        <div style="display: flex; gap: 8px; flex-wrap: wrap">
          <a-button type="primary" @click="addUrls" :loading="isAdding">
            <template #icon><PlusOutlined /></template>
            添加链接
          </a-button>
          
          <a-button @click="clearAll" :disabled="tasks.length === 0">
            <template #icon><ClearOutlined /></template>
            清空列表
          </a-button>
          
          <a-button @click="clearCompleted" :disabled="completedTasks.length === 0">
            <template #icon><DeleteOutlined /></template>
            清除已完成
          </a-button>
          
          <a-button type="primary" @click="startBatchDownload" :disabled="pendingTasks.length === 0" :loading="isBatchDownloading">
            <template #icon><DownloadOutlined /></template>
            批量下载 ({{ pendingTasks.length }})
          </a-button>
          
          <a-button type="dashed" @click="downloadZip" :disabled="completedTasks.length === 0">
            <template #icon><FileZipOutlined /></template>
            下载压缩包 ({{ completedTasks.length }})
          </a-button>
        </div>
      </a-space>
    </a-card>

    <!-- 下载进度 -->
    <a-card v-if="isBatchDownloading" title="批量下载进度" :bordered="false" style="margin-bottom: 24px">
      <a-progress :percent="batchProgress" :status="batchProgress === 100 ? 'success' : 'active'" />
      <div style="margin-top: 8px; text-align: center; color: #666">
        正在下载 {{ downloadingTasks.length }} 个文件，已完成 {{ completedTasks.length }} 个
      </div>
    </a-card>

    <!-- 任务列表 -->
    <a-card title="下载任务" :bordered="false">
      <a-list :data-source="tasks" :loading="isBatchDownloading">
        <template #renderItem="{ item: task }">
          <a-list-item>
            <template #actions>
              <a-space>
                <a-button 
                  v-if="task.status === 'pending'" 
                  type="link" 
                  size="small" 
                  @click="startSingleDownload(task.id)"
                >
                  开始下载
                </a-button>
                <a-button 
                  v-if="task.status === 'error'" 
                  type="link" 
                  size="small" 
                  @click="retryDownload(task.id)"
                >
                  重试
                </a-button>
                <a-button 
                  type="link" 
                  size="small" 
                  danger 
                  @click="removeTask(task.id)"
                >
                  删除
                </a-button>
              </a-space>
            </template>
            
            <a-list-item-meta>
              <template #title>
                <div style="display: flex; align-items: center; gap: 8px">
                  <span :style="{ color: getStatusColor(task.status) }">
                    {{ getStatusIcon(task.status) }}
                  </span>
                  <a-typography-text 
                    :ellipsis="{ tooltip: task.url }" 
                    style="max-width: 400px"
                  >
                    {{ task.url }}
                  </a-typography-text>
                </div>
              </template>
              
              <template #description>
                <div style="display: flex; align-items: center; gap: 16px; margin-top: 8px">
                  <a-progress 
                    v-if="task.status === 'downloading'" 
                    :percent="task.progress" 
                    size="small" 
                    style="width: 200px"
                  />
                  
                  <span v-if="task.status === 'pending'" style="color: #faad14">等待下载</span>
                  <span v-if="task.status === 'completed'" style="color: #52c41a">下载完成</span>
                  <span v-if="task.status === 'error'" style="color: #ff4d4f">{{ task.errorMessage }}</span>
                  
                  <span v-if="task.fileName" style="color: #666; font-size: 12px">
                    {{ task.fileName }}
                  </span>
                  
                  <span v-if="task.startTime" style="color: #999; font-size: 12px">
                    {{ formatTime(task.startTime) }}
                  </span>
                </div>
              </template>
            </a-list-item-meta>
          </a-list-item>
        </template>
        
        <template #empty>
          <a-empty description="暂无下载任务">
            <template #image>
              <FileTextOutlined style="font-size: 48px; color: #d9d9d9" />
            </template>
          </a-empty>
        </template>
      </a-list>
    </a-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { 
  PlusOutlined, 
  ClearOutlined, 
  DeleteOutlined, 
  DownloadOutlined,
  FileTextOutlined,
  FileZipOutlined 
} from '@ant-design/icons-vue'
import { useDownloadStore, type DownloadTask } from '@/stores/download'
import axios from 'axios'

const downloadStore = useDownloadStore()
const urlInput = ref('')
const isAdding = ref(false)
const isBatchDownloading = ref(false)

// 计算属性
const tasks = computed(() => downloadStore.webTasks)
const pendingTasks = computed(() => downloadStore.getWebPendingTasks())
const downloadingTasks = computed(() => downloadStore.getWebDownloadingTasks())
const completedTasks = computed(() => downloadStore.getWebCompletedTasks())
const batchProgress = computed(() => downloadStore.webBatchProgress)

// 状态图标和颜色
const getStatusIcon = (status: DownloadTask['status']) => {
  const icons = {
    pending: '⏳',
    downloading: '⬇️',
    completed: '✅',
    error: '❌'
  }
  return icons[status]
}

const getStatusColor = (status: DownloadTask['status']) => {
  const colors = {
    pending: '#faad14',
    downloading: '#1890ff',
    completed: '#52c41a',
    error: '#ff4d4f'
  }
  return colors[status]
}

// 验证网页URL格式
const isValidWebUrl = (url: string): boolean => {
  if (!url) return false
  
  // 基本的URL验证
  const webPatterns = [
    /^https?:\/\/[\w\-\.]+\.[a-z]{2,}/i,
    /^https?:\/\/[\w\-\.]+\.[a-z]{2,}\/.*/i,
  ]
  
  // 排除微信文章链接（避免重复）
  const wechatPatterns = [
    /^https?:\/\/mp\.weixin\.qq\.com\/.*/i,
    /^https?:\/\/.*weixin.*/i,
  ]
  
  // 检查是否是微信链接
  if (wechatPatterns.some(pattern => pattern.test(url))) {
    return false
  }
  
  // 检查是否是有效的网页链接
  return webPatterns.some(pattern => pattern.test(url))
}

// 添加URL
const addUrls = async () => {
  if (!urlInput.value.trim()) {
    message.warning('请输入网页文章链接')
    return
  }

  isAdding.value = true
  
  try {
    const urls = urlInput.value.split('\n')
      .map(url => url.trim())
      .filter(url => url && isValidWebUrl(url))
    
    if (urls.length === 0) {
      message.warning('请输入有效的网页文章链接')
      return
    }

    // 验证每个URL
    const validUrls: string[] = []
    for (const url of urls) {
      try {
        const response = await axios.post('/api/web/validate', { url })
        if (response.data.success && response.data.is_valid) {
          validUrls.push(url)
        }
      } catch (error) {
        console.warn(`URL验证失败: ${url}`, error)
      }
    }

    if (validUrls.length === 0) {
      message.warning('没有有效的网页链接')
      return
    }

    // 添加到下载任务
    downloadStore.addWebTasks(validUrls)
    
    message.success(`成功添加 ${validUrls.length} 个网页链接`)
    urlInput.value = ''
    
  } catch (error) {
    console.error('添加URL失败:', error)
    message.error('添加URL失败')
  } finally {
    isAdding.value = false
  }
}

// 清空所有任务
const clearAll = () => {
  downloadStore.clearWebTasks()
  message.info('已清空所有任务')
}

// 清除已完成任务
const clearCompleted = () => {
  downloadStore.clearWebCompletedTasks()
  message.info('已清除已完成任务')
}

// 开始批量下载
const startBatchDownload = async () => {
  if (pendingTasks.value.length === 0) {
    message.warning('没有待下载的任务')
    return
  }

  isBatchDownloading.value = true
  
  try {
    const urls = pendingTasks.value.map(task => task.url)
    
    const response = await axios.post('/api/web/download/batch', { urls })
    
    if (response.data.success) {
      message.success(`批量下载开始，共 ${response.data.total} 个任务`)
      
      // 更新任务状态
      downloadStore.updateWebBatchProgress(response.data)
      
      // 轮询检查进度
      pollBatchProgress(response.data.batch_id)
    } else {
      message.error(`批量下载失败: ${response.data.error}`)
    }
    
  } catch (error: any) {
    console.error('批量下载失败:', error)
    message.error(`批量下载失败: ${error.response?.data?.error || error.message}`)
  } finally {
    isBatchDownloading.value = false
  }
}

// 轮询检查批量下载进度
const pollBatchProgress = async (batchId: string) => {
  const interval = setInterval(async () => {
    try {
      // 获取所有任务状态
      const response = await axios.get('/api/tasks')
      
      if (response.data.success) {
        const batchTasks = response.data.tasks.filter((task: any) => 
          task.task_id.startsWith(batchId)
        )
        
        // 更新任务状态
        downloadStore.updateWebTasksFromBatch(batchTasks)
        
        // 检查是否全部完成
        const completedCount = batchTasks.filter((task: any) => 
          task.status === 'completed' || task.status === 'error'
        ).length
        
        if (completedCount === batchTasks.length) {
          clearInterval(interval)
          message.success('批量下载完成')
        }
      }
    } catch (error) {
      console.error('检查进度失败:', error)
      clearInterval(interval)
    }
  }, 2000)
}

// 开始单个下载
const startSingleDownload = async (taskId: string) => {
  const task = downloadStore.getWebTaskById(taskId)
  if (!task) return

  try {
    downloadStore.updateWebTaskStatus(taskId, 'downloading')
    
    const response = await axios.post('/api/web/download/single', { url: task.url })
    
    if (response.data.success) {
      downloadStore.updateWebTaskStatus(taskId, 'completed', response.data.result)
      message.success(`下载完成: ${task.url}`)
    } else {
      downloadStore.updateWebTaskStatus(taskId, 'error', null, response.data.error)
      message.error(`下载失败: ${response.data.error}`)
    }
    
  } catch (error: any) {
    console.error('下载失败:', error)
    downloadStore.updateWebTaskStatus(taskId, 'error', null, error.response?.data?.error || error.message)
    message.error(`下载失败: ${error.response?.data?.error || error.message}`)
  }
}

// 重试下载
const retryDownload = (taskId: string) => {
  downloadStore.updateWebTaskStatus(taskId, 'pending')
  startSingleDownload(taskId)
}

// 删除任务
const removeTask = (taskId: string) => {
  downloadStore.removeWebTask(taskId)
  message.info('任务已删除')
}

// 下载压缩包
const downloadZip = async () => {
  if (completedTasks.value.length === 0) {
    message.warning('没有已完成的任务可以打包')
    return
  }

  try {
    // 获取已完成任务的目录列表
    const directories = completedTasks.value
      .filter(task => task.result?.markdown_file)
      .map(task => {
        const path = task.result.markdown_file
        return path.substring(0, path.lastIndexOf('/'))
      })
    
    if (directories.length === 0) {
      message.warning('没有有效的下载文件可以打包')
      return
    }

    const response = await axios.post('/api/download/zip/batch', { directories })
    
    if (response.data.success) {
      // 创建下载链接
      const link = document.createElement('a')
      link.href = `/api/download/zip/batch`
      link.download = `web_articles_${Date.now()}.zip`
      link.click()
      
      message.success('压缩包下载开始')
    } else {
      message.error(`下载压缩包失败: ${response.data.error}`)
    }
    
  } catch (error: any) {
    console.error('下载压缩包失败:', error)
    message.error(`下载压缩包失败: ${error.response?.data?.error || error.message}`)
  }
}

// 格式化时间
const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleString()
}

onMounted(() => {
  // 初始化时加载已有的任务
  downloadStore.loadWebTasks()
})
</script>

<style scoped>
.web-article-downloader {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

:deep(.ant-card) {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

:deep(.ant-list-item) {
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

:deep(.ant-list-item:last-child) {
  border-bottom: none;
}
</style>