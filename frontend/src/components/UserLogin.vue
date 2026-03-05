<template>
  <div class="user-login">
    <!-- 如果已登录，显示欢迎信息 -->
    <div v-if="userStore.isAuthenticated" class="logged-in-container">
      <a-result
        status="success"
        title="登录成功"
        :sub-title="`欢迎回来，${userStore.currentUser?.username}！`"
      >
        <template #extra>
          <a-space>
            <a-button type="primary" @click="navigateTo('/')">
              返回首页
            </a-button>
            <a-button @click="navigateTo('/users')">
              用户管理
            </a-button>
            <a-button @click="handleLogout">
              退出登录
            </a-button>
          </a-space>
        </template>
      </a-result>
    </div>

    <!-- 如果未登录，显示登录表单 -->
    <div v-else class="login-form-container">
      <a-card title="用户登录" :bordered="false" style="max-width: 400px; margin: 0 auto">
        <a-form
          :model="formState"
          name="login"
          autocomplete="off"
          @finish="onFinish"
          @finishFailed="onFinishFailed"
        >
          <a-form-item
            label="用户名"
            name="username"
            :rules="[{ required: true, message: '请输入用户名!' }]"
          >
            <a-input v-model:value="formState.username" placeholder="请输入用户名" />
          </a-form-item>

          <a-form-item
            label="密码"
            name="password"
            :rules="[{ required: true, message: '请输入密码!' }]"
          >
            <a-input-password v-model:value="formState.password" placeholder="请输入密码" />
          </a-form-item>

          <a-form-item>
            <a-button 
              type="primary" 
              html-type="submit" 
              :loading="userStore.isLoading"
              style="width: 100%"
            >
              登录
            </a-button>
          </a-form-item>

          <a-form-item>
            <div style="text-align: center">
              <a-button type="link" @click="showRegister = true">
                没有账号？立即注册
              </a-button>
            </div>
          </a-form-item>
        </a-form>
      </a-card>

      <!-- 注册模态框 -->
      <a-modal
        v-model:open="showRegister"
        title="用户注册"
        :footer="null"
        @cancel="showRegister = false"
      >
        <UserRegister @success="handleRegisterSuccess" />
      </a-modal>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'
import UserRegister from './UserRegister.vue'

interface FormState {
  username: string
  password: string
}

const router = useRouter()
const userStore = useUserStore()
const formState = reactive<FormState>({
  username: '',
  password: ''
})

const showRegister = ref(false)

const navigateTo = (path: string) => {
  router.push(path)
}

const handleLogout = () => {
  userStore.logout()
  message.success('退出登录成功')
}

const onFinish = async (values: FormState) => {
  const result = await userStore.login(values)
  
  if (result.success) {
    message.success(result.message)
    
    // 登录成功后根据来源页面或默认跳转
    const redirectPath = router.currentRoute.value.query.redirect as string || '/'
    
    // 延迟跳转，让用户看到成功消息
    setTimeout(() => {
      navigateTo(redirectPath)
    }, 1000)
  } else {
    message.error(result.message)
  }
}

const onFinishFailed = (errorInfo: any) => {
  console.log('登录失败:', errorInfo)
}

const handleRegisterSuccess = () => {
  showRegister.value = false
  message.success('注册成功，请登录')
}

// 页面加载时检查登录状态
onMounted(async () => {
  await userStore.checkAuth()
})
</script>

<style scoped>
.user-login {
  padding: 40px 20px;
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logged-in-container {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.login-form-container {
  width: 100%;
}

@media (max-width: 768px) {
  .user-login {
    padding: 20px 10px;
  }
  
  .logged-in-container {
    max-width: 100%;
  }
}
</style>