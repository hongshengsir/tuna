import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

/**
 * API基础配置
 * 后端服务运行在localhost:5000，通过代理进行通信
 */
const API_BASE_URL = 'http://localhost:5000/api'

/**
 * 下载任务接口定义
 * 用于管理单个下载任务的状态和信息
 */
export interface DownloadTask {
  /** 任务唯一标识符 */
  id: string
  /** 要下载的文章URL */
  url: string
  /** 任务状态：等待下载、下载中、已完成、错误 */
  status: 'pending' | 'downloading' | 'completed' | 'error'
  /** 下载进度百分比 (0-100) */
  progress: number
  /** 错误信息（仅在状态为error时存在） */
  errorMessage?: string
  /** 下载后的文件名 */
  fileName?: string
  /** 任务开始时间 */
  startTime?: Date
  /** 任务结束时间 */
  endTime?: Date
  /** 后端API返回的任务ID */
  apiTaskId?: string
  /** 下载结果数据（包含markdown文件路径等信息） */
  result?: any
}

/**
 * 下载状态管理存储
 * 管理微信文章和网页文章两种类型的下载任务
 */
export const useDownloadStore = defineStore('download', () => {
  // ==================== 微信文章下载相关状态 ====================
  
  /** 微信文章下载任务列表 */
  const tasks = ref<DownloadTask[]>([])
  /** 是否正在进行批量下载 */
  const isBatchDownloading = ref(false)
  /** 批量下载进度百分比 */
  const batchProgress = ref(0)
  
  // ==================== 网页文章下载相关状态 ====================
  
  /** 网页文章下载任务列表 */
  const webTasks = ref<DownloadTask[]>([])
  /** 是否正在进行网页批量下载 */
  const isWebBatchDownloading = ref(false)
  /** 网页批量下载进度百分比 */
  const webBatchProgress = ref(0)

  // ==================== 通用工具函数 ====================

  /**
   * 统一的API请求函数
   * @param endpoint API端点路径
   * @param options 请求选项
   * @returns Promise解析后的JSON响应
   */
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

  // ==================== 微信文章下载管理函数 ====================

  /**
   * 添加新的微信文章下载任务
   * @param url 要下载的文章URL
   * @returns 新创建任务的ID
   */
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

  /**
   * 更新微信文章下载任务状态
   * @param id 任务ID
   * @param status 新的状态
   * @param progress 进度百分比（可选）
   * @param errorMessage 错误信息（可选）
   */
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

  /**
   * 删除指定的微信文章下载任务
   * @param id 要删除的任务ID
   */
  const removeTask = (id: string) => {
    const index = tasks.value.findIndex(t => t.id === id)
    if (index !== -1) {
      tasks.value.splice(index, 1)
    }
  }

  /**
   * 清除所有已完成的微信文章下载任务（包括成功和失败的任务）
   */
  const clearCompletedTasks = () => {
    tasks.value = tasks.value.filter(task => task.status !== 'completed' && task.status !== 'error')
  }

  /**
   * 开始微信文章批量下载
   */
  const startBatchDownload = () => {
    isBatchDownloading.value = true
    batchProgress.value = 0
  }

  /**
   * 更新微信文章批量下载进度
   * @param progress 新的进度百分比
   */
  const updateBatchProgress = (progress: number) => {
    batchProgress.value = progress
  }

  /**
   * 结束微信文章批量下载
   */
  const endBatchDownload = () => {
    isBatchDownloading.value = false
  }

  /**
   * 获取所有待下载的微信文章任务
   * @returns 待下载任务列表
   */
  const getPendingTasks = () => {
    return tasks.value.filter(task => task.status === 'pending')
  }

  /**
   * 获取所有下载中的微信文章任务
   * @returns 下载中任务列表
   */
  const getDownloadingTasks = () => {
    return tasks.value.filter(task => task.status === 'downloading')
  }

  /**
   * 获取所有已完成的微信文章任务
   * @returns 已完成任务列表
   */
  const getCompletedTasks = () => {
    return tasks.value.filter(task => task.status === 'completed')
  }

  /**
   * 获取所有失败的微信文章任务
   * @returns 失败任务列表
   */
  const getErrorTasks = () => {
    return tasks.value.filter(task => task.status === 'error')
  }

  // ==================== 微信文章API调用函数 ====================

  /**
   * 调用后端API下载单个微信文章
   * @param taskId 要下载的任务ID
   */
  const downloadSingleArticle = async (taskId: string) => {
    const task = tasks.value.find(t => t.id === taskId)
    if (!task) {
      throw new Error('任务不存在')
    }

    try {
      // 调用后端微信文章下载API
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

  /**
   * 调用后端API批量下载微信文章
   * @param taskIds 要下载的任务ID列表
   */
  const downloadBatchArticles = async (taskIds: string[]) => {
    const pendingTasks = taskIds.map(id => tasks.value.find(t => t.id === id)).filter(Boolean)
    
    if (pendingTasks.length === 0) {
      throw new Error('没有待下载的任务')
    }

    try {
      const urls = pendingTasks.map(task => task!.url)
      
      // 调用后端微信文章批量下载API
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

  /**
   * 检查微信文章任务状态（通过后端API）
   * @param taskId 要检查的任务ID
   */
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

  /**
   * 后端API健康检查
   * @returns 后端服务是否正常运行
   */
  const healthCheck = async () => {
    try {
      const response = await apiRequest('/health')
      return response.status === 'ok'
    } catch (error) {
      console.error('API健康检查失败:', error)
      return false
    }
  }

  /**
   * 下载单个目录的压缩包
   * @param directoryPath 要下载的目录路径
   * @returns 下载是否成功
   */
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

  /**
   * 下载多个目录的批量压缩包
   * @param directoryPaths 要下载的目录路径列表
   * @returns 下载是否成功
   */
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

  /**
   * 添加多个网页文章下载任务
   * @param urls 要下载的网页URL列表
   */
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

  /**
   * 更新网页文章下载任务状态
   * @param id 任务ID
   * @param status 新的状态
   * @param result 下载结果数据（可选）
   * @param errorMessage 错误信息（可选）
   */
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

  /**
   * 删除指定的网页文章下载任务
   * @param id 要删除的任务ID
   */
  const removeWebTask = (id: string) => {
    const index = webTasks.value.findIndex(t => t.id === id)
    if (index !== -1) {
      webTasks.value.splice(index, 1)
    }
  }

  /**
   * 清空所有网页文章下载任务
   */
  const clearWebTasks = () => {
    webTasks.value = []
  }

  /**
   * 清除所有已完成的网页文章下载任务（包括成功和失败的任务）
   */
  const clearWebCompletedTasks = () => {
    webTasks.value = webTasks.value.filter(task => task.status !== 'completed' && task.status !== 'error')
  }

  /**
   * 根据ID获取网页文章下载任务
   * @param id 任务ID
   * @returns 对应的任务对象或undefined
   */
  const getWebTaskById = (id: string) => {
    return webTasks.value.find(t => t.id === id)
  }

  /**
   * 获取所有待下载的网页文章任务
   * @returns 待下载任务列表
   */
  const getWebPendingTasks = () => {
    return webTasks.value.filter(task => task.status === 'pending')
  }

  /**
   * 获取所有下载中的网页文章任务
   * @returns 下载中任务列表
   */
  const getWebDownloadingTasks = () => {
    return webTasks.value.filter(task => task.status === 'downloading')
  }

  /**
   * 获取所有已完成的网页文章任务
   * @returns 已完成任务列表
   */
  const getWebCompletedTasks = () => {
    return webTasks.value.filter(task => task.status === 'completed')
  }

  /**
   * 获取所有失败的网页文章任务
   * @returns 失败任务列表
   */
  const getWebErrorTasks = () => {
    return webTasks.value.filter(task => task.status === 'error')
  }

  /**
   * 更新网页文章批量下载进度
   * @param batchData 批量下载数据（包含已完成数量和总数）
   */
  const updateWebBatchProgress = (batchData: any) => {
    webBatchProgress.value = Math.round((batchData.completed / batchData.total) * 100)
  }

  /**
   * 从后端批量任务数据更新前端网页任务状态
   * @param batchTasks 后端返回的批量任务数据
   */
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

  /**
   * 从本地存储加载网页文章下载任务
   */
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

  /**
   * 保存网页文章下载任务到本地存储
   */
  const saveWebTasks = () => {
    try {
      localStorage.setItem('web_download_tasks', JSON.stringify(webTasks.value))
    } catch (error) {
      console.error('保存网页任务失败:', error)
    }
  }

  // 监听网页任务变化，自动保存到本地存储
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