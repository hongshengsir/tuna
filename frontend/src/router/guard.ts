import { RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由守卫
const authGuard = async (
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) => {
  const userStore = useUserStore()
  
  // 如果目标路由需要登录保护
  if (to.meta.requiresAuth) {
    // 检查用户是否已登录
    if (!userStore.isAuthenticated) {
      // 尝试检查登录状态
      const isAuthenticated = await userStore.checkAuth()
      
      if (!isAuthenticated) {
        // 未登录，跳转到登录页面，并记录来源页面
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      }
    }
  }
  
  // 如果用户已登录但访问登录页面，重定向到首页
  if (to.path === '/login' && userStore.isAuthenticated) {
    next('/')
    return
  }
  
  // 允许导航
  next()
}

export default authGuard