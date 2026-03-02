<template>
  <div class="wechat-downloader">
    <!-- 输入区域 -->
    <a-card title="微信文章下载" :bordered="false" style="margin-bottom: 24px">
      <a-space direction="vertical" style="width: 100%">
        <div>
          <a-textarea
            v-model:value="urlInput"
            placeholder="请输入微信文章链接，多个链接请用换行分隔"
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

const downloadStore = useDownloadStore()
const urlInput = ref('')
const isAdding = ref(false)

// 计算属性
const tasks = computed(() => downloadStore.tasks)
const pendingTasks = computed(() => downloadStore.getPendingTasks())
const downloadingTasks = computed(() => downloadStore.getDownloadingTasks())
const completedTasks = computed(() => downloadStore.getCompletedTasks())
const isBatchDownloading = computed(() => downloadStore.isBatchDownloading)
const batchProgress = computed(() => downloadStore.batchProgress)

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

// 添加URL
const addUrls = async () => {
  if (!urlInput.value.trim()) {
    message.warning('请输入微信文章链接')
    return
  }

  isAdding.value = true
  
  try {
    const urls = urlInput.value.split('\n')
      .map(url => url.trim())
      .filter(url => url && isValidWechatUrl(url))
    
    if (urls.length === 0) {
      message.warning('请输入有效的微信文章链接')
      return
    }
    
    urls.forEach(url => {
      downloadStore.addTask(url)
    })
    
    message.success(`成功添加 ${urls.length} 个下载任务`)
    urlInput.value = ''
  } catch (error) {
    message.error('添加任务失败')
  } finally {
    isAdding.value = false
  }
}

// 验证微信链接
const isValidWechatUrl = (url: string): boolean => {
  const wechatPatterns = [
    /^https?:\/\/mp\.weixin\.qq\.com\/s\/[\w-]+/,
    /^https?:\/\/mp\.weixin\.qq\.com\/s\?/,
    /^https?:\/\/mp\.weixin\.qq\.com\/s\/.*/,
    /^https?:\/\/mp\.weixin\.qq\.com\/.*/,
    /^https?:\/\/.*weixin.*/i
  ]
  
  return wechatPatterns.some(pattern => pattern.test(url))
}

// 批量下载
const startBatchDownload = async () => {
  if (pendingTasks.value.length === 0) {
    message.warning('没有待下载的任务')
    return
  }

  // 检查API服务是否可用
  const isApiHealthy = await downloadStore.healthCheck()
  if (!isApiHealthy) {
    message.error('后端API服务不可用，请确保Python服务器已启动')
    return
  }

  downloadStore.startBatchDownload()
  
  try {
    // 调用后端API批量下载
    const taskIds = pendingTasks.value.map(task => task.id)
    await downloadStore.downloadBatchArticles(taskIds)
    
    downloadStore.endBatchDownload()
    message.success('批量下载完成')
  } catch (error) {
    downloadStore.endBatchDownload()
    message.error('批量下载失败')
  }
}

// 单个下载
const startSingleDownload = async (taskId: string) => {
  downloadStore.updateTaskStatus(taskId, 'downloading', 0)
  
  try {
    // 检查API服务是否可用
    const isApiHealthy = await downloadStore.healthCheck()
    if (!isApiHealthy) {
      throw new Error('后端API服务不可用')
    }
    
    // 调用后端API下载
    await downloadStore.downloadSingleArticle(taskId)
    
  } catch (error) {
    downloadStore.updateTaskStatus(taskId, 'error', 0, error instanceof Error ? error.message : '下载失败')
  }
}

// 重试下载
const retryDownload = (taskId: string) => {
  downloadStore.updateTaskStatus(taskId, 'pending', 0)
  startSingleDownload(taskId)
}

// 删除任务
const removeTask = (taskId: string) => {
  downloadStore.removeTask(taskId)
  message.success('任务已删除')
}

// 清空所有任务
const clearAll = () => {
  downloadStore.tasks.length = 0
  message.success('已清空所有任务')
}

// 清除已完成任务
const clearCompleted = () => {
  downloadStore.clearCompletedTasks()
  message.success('已清除已完成任务')
}

// 下载压缩包
const downloadZip = async () => {
  if (completedTasks.value.length === 0) {
    message.warning('没有已完成的下载任务')
    return
  }

  // 检查API服务是否可用
  const isApiHealthy = await downloadStore.healthCheck()
  if (!isApiHealthy) {
    message.error('后端API服务不可用，请确保Python服务器已启动')
    return
  }

  try {
    // 获取已下载文章的目录路径
    const directoryPaths = completedTasks.value.map(task => {
      // 根据文件名推断目录路径
      if (task.fileName) {
        const fileName = task.fileName.replace('.md', '')
        return `./${fileName}`
      }
      return null
    }).filter(Boolean) as string[]

    if (directoryPaths.length === 0) {
      message.warning('无法获取下载文件的目录信息')
      return
    }

    // 如果只有一个目录，下载单个压缩包；多个目录则下载批量压缩包
    if (directoryPaths.length === 1) {
      await downloadStore.downloadDirectoryZip(directoryPaths[0])
    } else {
      await downloadStore.downloadBatchZip(directoryPaths)
    }
    
    message.success('压缩包下载成功')
  } catch (error) {
    console.error('压缩包下载失败:', error)
    message.error('压缩包下载失败，请检查后端服务状态')
  }
}

// 格式化时间
const formatTime = (date: Date) => {
  return new Date(date).toLocaleTimeString('zh-CN')
}

onMounted(() => {
  // 可以在这里添加一些示例URL
  urlInput.value = 'https://mp.weixin.qq.com/s/example1\nhttps://mp.weixin.qq.com/s/example2'
})
</script>

<style scoped>
.wechat-downloader {
  max-width: 1200px;
  margin: 0 auto;
}

:deep(.ant-list-item) {
  padding: 16px 0;
}

:deep(.ant-list-item-meta-title) {
  margin-bottom: 4px;
}

:deep(.ant-progress) {
  margin: 0;
}
</style>