import { defineStore } from 'pinia'
import { ref } from 'vue'

// API配置
const API_BASE_URL = 'http://localhost:5000/api'

export interface User {
  id: number
  username: string
  email: string
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface CreateUserRequest {
  username: string
  email: string
  password: string
}

export interface UpdateUserRequest {
  username?: string
  email?: string
  password?: string
}

export const useUserStore = defineStore('user', () => {
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])
  const isAuthenticated = ref(false)
  const isLoading = ref(false)

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

  // 用户登录
  const login = async (credentials: LoginRequest) => {
    isLoading.value = true
    try {
      const response = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify(credentials)
      })

      if (response.success) {
        currentUser.value = response.data
        isAuthenticated.value = true
        return { success: true, message: '登录成功' }
      } else {
        return { success: false, message: response.error || '登录失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 用户注册
  const register = async (userData: CreateUserRequest) => {
    isLoading.value = true
    try {
      const response = await apiRequest('/users', {
        method: 'POST',
        body: JSON.stringify(userData)
      })

      if (response.success) {
        return { success: true, message: '用户创建成功' }
      } else {
        return { success: false, message: response.error || '注册失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户列表
  const fetchUsers = async () => {
    isLoading.value = true
    try {
      const response = await apiRequest('/users')

      if (response.success) {
        users.value = response.data || []
        return { success: true }
      } else {
        return { success: false, message: response.error || '获取用户列表失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户详情
  const fetchUser = async (userId: number) => {
    isLoading.value = true
    try {
      const response = await apiRequest(`/users/${userId}`)

      if (response.success) {
        return { success: true, user: response.data }
      } else {
        return { success: false, message: response.error || '获取用户详情失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 更新用户信息
  const updateUser = async (userId: number, userData: UpdateUserRequest) => {
    isLoading.value = true
    try {
      const response = await apiRequest(`/users/${userId}`, {
        method: 'PUT',
        body: JSON.stringify(userData)
      })

      if (response.success) {
        // 更新本地用户列表
        const index = users.value.findIndex(user => user.id === userId)
        if (index !== -1) {
          users.value[index] = { ...users.value[index], ...userData }
        }
        
        // 如果更新的是当前用户，也更新当前用户信息
        if (currentUser.value && currentUser.value.id === userId) {
          currentUser.value = { ...currentUser.value, ...userData }
        }
        
        return { success: true, message: '用户信息更新成功' }
      } else {
        return { success: false, message: response.error || '更新用户信息失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 删除用户
  const deleteUser = async (userId: number) => {
    isLoading.value = true
    try {
      const response = await apiRequest(`/users/${userId}`, {
        method: 'DELETE'
      })

      if (response.success) {
        // 从本地用户列表中移除
        users.value = users.value.filter(user => user.id !== userId)
        
        // 如果删除的是当前用户，则登出
        if (currentUser.value && currentUser.value.id === userId) {
          logout()
        }
        
        return { success: true, message: '用户删除成功' }
      } else {
        return { success: false, message: response.error || '删除用户失败' }
      }
    } catch (error) {
      return { success: false, message: error instanceof Error ? error.message : '网络请求失败' }
    } finally {
      isLoading.value = false
    }
  }

  // 用户登出
  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    users.value = []
  }

  // 检查登录状态
  const checkAuth = async () => {
    try {
      const response = await apiRequest('/auth/me')
      
      if (response.success && response.data) {
        currentUser.value = response.data
        isAuthenticated.value = true
        return true
      }
    } catch (error) {
      console.error('检查登录状态失败:', error)
    }
    
    currentUser.value = null
    isAuthenticated.value = false
    return false
  }

  return {
    currentUser,
    users,
    isAuthenticated,
    isLoading,
    login,
    register,
    fetchUsers,
    fetchUser,
    updateUser,
    deleteUser,
    logout,
    checkAuth
  }
})