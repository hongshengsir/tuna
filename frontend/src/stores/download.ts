import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface DownloadTask {
  id: string
  url: string
  status: 'pending' | 'downloading' | 'completed' | 'error'
  progress: number
  errorMessage?: string
  fileName?: string
  startTime?: Date
  endTime?: Date
}

export const useDownloadStore = defineStore('download', () => {
  const tasks = ref<DownloadTask[]>([])
  const isBatchDownloading = ref(false)
  const batchProgress = ref(0)

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

  return {
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
    getErrorTasks
  }
})