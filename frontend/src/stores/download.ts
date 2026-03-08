import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

// API配置
const API_BASE_URL = 'http://localhost:5000/api'

export interface DownloadTask {
  id: string
  url: string
  status: 'pending' | 'downloading' | 'completed' | 'error'
  progress: number
  errorMessage?: string
  fileName?: string
  startTime?: Date
  endTime?: Date
  apiTaskId?: string // 后端API任务ID
}

export const useDownloadStore = defineStore('download', () => {
  // 微信文章下载任务
  const tasks = ref<DownloadTask[]>([])
  const isBatchDownloading = ref(false)
  const batchProgress = ref(0)
  
  // 网页文章下载任务
  const webTasks = ref<DownloadTask[]>([])
  const isWebBatchDownloading = ref(false)
  const webBatchProgress = ref(0)

  // API调用函数
  const apiRequest = async (endpoint: string, options: RequestInit = {}) => {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API请求失败:', error)
      throw error
    }
  }

  const addTask = (url: string) => {
    const task: DownloadTask = {
      id: Date.now().toString(),
      url: url.trim(),
      status: 'pending',
      progress: 0
    }
    tasks.value.push(task)
    return task.id
  }

  const updateTaskStatus = (id: string, status: DownloadTask['status'], progress?: number, errorMessage?: string) => {
    const task = tasks.value.find(t => t.id === id)
    if (task) {
      task.status = status
      if (progress !== undefined) {
        task.progress = progress
      }
      if (errorMessage) {
        task.errorMessage = errorMessage
      }
      if (status === 'downloading' && !task.startTime) {
        task.startTime = new Date()
      }
      if (status === 'completed' || status === 'error') {
        task.endTime = new Date()
      }
    }
  }

  const removeTask = (id: string) => {
    const index = tasks.value.findIndex(t => t.id === id)
    if (index !== -1) {
      tasks.value.splice(index, 1)
    }
  }

  const clearCompletedTasks = () => {
    tasks.value = tasks.value.filter(task => task.status !== 'completed' && task.status !== 'error')
  }

  const startBatchDownload = () => {
    isBatchDownloading.value = true
    batchProgress.value = 0
  }

  const updateBatchProgress = (progress: number) => {
    batchProgress.value = progress
  }

  const endBatchDownload = () => {
    isBatchDownloading.value = false
  }

  const getPendingTasks = () => {
    return tasks.value.filter(task => task.status === 'pending')
  }

  const getDownloadingTasks = () => {
    return tasks.value.filter(task => task.status === 'downloading')
  }

  const getCompletedTasks = () => {
    return tasks.value.filter(task => task.status === 'completed')
  }

  const getErrorTasks = () => {
    return tasks.value.filter(task => task.status === 'error')
  }

  // 调用后端API下载单个文章
  const downloadSingleArticle = async (taskId: string) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (!task) {
      throw new Error('任务不存在')
    }

    try {
      // 调用后端API
      const response = await apiRequest('/download/single', {
        method: 'POST',
        body: JSON.stringify({ url: task.url })
      })

      if (response.success) {
        task.status = 'completed'
        task.progress = 100
        task.apiTaskId = response.task_id
        
        // 设置文件名
        if (response.result && response.result.markdown_file) {
          const filePath = response.result.markdown_file
          task.fileName = filePath.split('/').pop() || 'article.md'
        }
      } else {
        task.status = 'error'
        task.errorMessage = response.error || '下载失败'
      }
    } catch (error) {
      task.status = 'error'
      task.errorMessage = error instanceof Error ? error.message : '网络请求失败'
    }
  }

  // 调用后端API批量下载文章
  const downloadBatchArticles = async (taskIds: string[]) => {
    const pendingTasks = taskIds.map(id => tasks.value.find(t => t.id === id)).filter(Boolean)
    
    if (pendingTasks.length === 0) {
      throw new Error('没有待下载的任务')
    }

    try {
      const urls = pendingTasks.map(task => task!.url)
      
      // 调用后端批量下载API
      const response = await apiRequest('/download/batch', {
        method: 'POST',
        body: JSON.stringify({ urls })
      })

      if (response.success) {
        // 更新任务状态
        pendingTasks.forEach((task, index) => {
          if (task) {
            task.status = 'completed'
            task.progress = 100
            task.apiTaskId = `${response.batch_id}_${index}`
            
            // 设置文件名
            if (response.results && response.results[index] && response.results[index].markdown_file) {
              const filePath = response.results[index].markdown_file
              task.fileName = filePath.split('/').pop() || 'article.md'
            }
          }
        })
      } else {
        // 批量下载失败
        pendingTasks.forEach(task => {
          if (task) {
            task.status = 'error'
            task.errorMessage = response.error || '批量下载失败'
          }
        })
      }
    } catch (error) {
      pendingTasks.forEach(task => {
        if (task) {
          task.status = 'error'
          task.errorMessage = error instanceof Error ? error.message : '网络请求失败'
        }
      })
    }
  }

  // 检查任务状态
  const checkTaskStatus = async (taskId: string) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (!task || !task.apiTaskId) {
      return
    }

    try {
      const response = await apiRequest(`/tasks/${task.apiTaskId}`)
      if (response.success) {
        const apiTask = response.task
        task.status = apiTask.status
        task.progress = apiTask.progress
        
        if (apiTask.status === 'error') {
          task.errorMessage = apiTask.error_message
        }
      }
    } catch (error) {
      console.error('检查任务状态失败:', error)
    }
  }

  // 健康检查
  const healthCheck = async () => {
    try {
      const response = await apiRequest('/health')
      return response.status === 'ok'
    } catch (error) {
      console.error('API健康检查失败:', error)
      return false
    }
  }

  // 下载单个目录的压缩包
  const downloadDirectoryZip = async (directoryPath: string) => {
    try {
      // 调用后端API下载ZIP文件
      const response = await fetch(`${API_BASE_URL}/download/zip/${encodeURIComponent(directoryPath)}`)
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      // 获取文件名
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'download.zip'
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="(.+)"/)
        if (match) {
          filename = match[1]
        }
      }
      
      // 创建Blob并下载
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      return true
    } catch (error) {
      console.error('下载压缩包失败:', error)
      throw error
    }
  }

  // 下载多个目录的批量压缩包
  const downloadBatchZip = async (directoryPaths: string[]) => {
    try {
      // 调用后端API下载批量ZIP文件
      const response = await fetch(`${API_BASE_URL}/download/zip/batch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ directories: directoryPaths })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }
      
      // 获取文件名
      const contentDisposition = response.headers.get('Content-Disposition')
      let filename = 'batch_download.zip'
      if (contentDisposition) {
        const match = contentDisposition.match(/filename="(.+)"/)
        if (match) {
          filename = match[1]
        }
      }
      
      // 创建Blob并下载
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      
      return true
    } catch (error) {
      console.error('下载批量压缩包失败:', error)
      throw error
    }
  }

  // ===========================================================================
  // 网页文章下载相关方法
  // ===========================================================================

  // 添加网页下载任务
  const addWebTasks = (urls: string[]) => {
    urls.forEach(url => {
      const task: DownloadTask = {
        id: Date.now().toString() + Math.random().toString(36).substr(2, 5),
        url: url.trim(),
        status: 'pending',
        progress: 0
      }
      webTasks.value.push(task)
    })
  }

  // 更新网页任务状态
  const updateWebTaskStatus = (id: string, status: DownloadTask['status'], result?: any, errorMessage?: string) => {
    const task = webTasks.value.find(t => t.id === id)
    if (task) {
      task.status = status
      if (status === 'downloading' && !task.startTime) {
        task.startTime = new Date()
      }
      if (status === 'completed' || status === 'error') {
        task.endTime = new Date()
        task.progress = 100
      }
      if (errorMessage) {
        task.errorMessage = errorMessage
      }
      if (result) {
        task.result = result
        if (result.markdown_file) {
          const filePath = result.markdown_file
          task.fileName = filePath.split('/').pop() || 'article.md'
        }
      }
    }
  }

  // 删除网页任务
  const removeWebTask = (id: string) => {
    const index = webTasks.value.findIndex(t => t.id === id)
    if (index !== -1) {
      webTasks.value.splice(index, 1)
    }
  }

  // 清空所有网页任务
  const clearWebTasks = () => {
    webTasks.value = []
  }

  // 清除已完成的网页任务
  const clearWebCompletedTasks = () => {
    webTasks.value = webTasks.value.filter(task => task.status !== 'completed' && task.status !== 'error')
  }

  // 获取网页任务
  const getWebTaskById = (id: string) => {
    return webTasks.value.find(t => t.id === id)
  }

  // 获取待下载的网页任务
  const getWebPendingTasks = () => {
    return webTasks.value.filter(task => task.status === 'pending')
  }

  // 获取下载中的网页任务
  const getWebDownloadingTasks = () => {
    return webTasks.value.filter(task => task.status === 'downloading')
  }

  // 获取已完成的网页任务
  const getWebCompletedTasks = () => {
    return webTasks.value.filter(task => task.status === 'completed')
  }

  // 获取错误的网页任务
  const getWebErrorTasks = () => {
    return webTasks.value.filter(task => task.status === 'error')
  }

  // 更新网页批量下载进度
  const updateWebBatchProgress = (batchData: any) => {
    webBatchProgress.value = Math.round((batchData.completed / batchData.total) * 100)
  }

  // 从批量任务更新网页任务状态
  const updateWebTasksFromBatch = (batchTasks: any[]) => {
    batchTasks.forEach(apiTask => {
      const taskId = apiTask.task_id
      const task = webTasks.value.find(t => t.apiTaskId === taskId)
      if (task) {
        task.status = apiTask.status
        task.progress = apiTask.progress
        if (apiTask.status === 'error') {
          task.errorMessage = apiTask.error_message
        }
        if (apiTask.status === 'completed' && apiTask.result) {
          task.result = apiTask.result
          if (apiTask.result.markdown_file) {
            const filePath = apiTask.result.markdown_file
            task.fileName = filePath.split('/').pop() || 'article.md'
          }
        }
      }
    })
  }

  // 加载网页任务（从本地存储）
  const loadWebTasks = () => {
    try {
      const saved = localStorage.getItem('web_download_tasks')
      if (saved) {
        webTasks.value = JSON.parse(saved)
      }
    } catch (error) {
      console.error('加载网页任务失败:', error)
    }
  }

  // 保存网页任务到本地存储
  const saveWebTasks = () => {
    try {
      localStorage.setItem('web_download_tasks', JSON.stringify(webTasks.value))
    } catch (error) {
      console.error('保存网页任务失败:', error)
    }
  }

  // 监听网页任务变化，自动保存
  watch(webTasks, saveWebTasks, { deep: true })

  return {
    // 微信文章下载相关
    tasks,
    isBatchDownloading,
    batchProgress,
    addTask,
    updateTaskStatus,
    removeTask,
    clearCompletedTasks,
    startBatchDownload,
    updateBatchProgress,
    endBatchDownload,
    getPendingTasks,
    getDownloadingTasks,
    getCompletedTasks,
    getErrorTasks,
    downloadSingleArticle,
    downloadBatchArticles,
    checkTaskStatus,
    healthCheck,
    downloadDirectoryZip,
    downloadBatchZip,
    
    // 网页文章下载相关
    webTasks,
    isWebBatchDownloading,
    webBatchProgress,
    addWebTasks,
    updateWebTaskStatus,
    removeWebTask,
    clearWebTasks,
    clearWebCompletedTasks,
    getWebTaskById,
    getWebPendingTasks,
    getWebDownloadingTasks,
    getWebCompletedTasks,
    getWebErrorTasks,
    updateWebBatchProgress,
    updateWebTasksFromBatch,
    loadWebTasks
  }
})