<template>
  <div class="user-register">
    <a-form
      :model="formState"
      name="register"
      autocomplete="off"
      @finish="onFinish"
      @finishFailed="onFinishFailed"
    >
      <a-form-item
        label="用户名"
        name="username"
        :rules="[
          { required: true, message: '请输入用户名!' },
          { min: 3, message: '用户名至少3个字符!' },
          { max: 20, message: '用户名最多20个字符!' }
        ]"
      >
        <a-input v-model:value="formState.username" />
      </a-form-item>

      <a-form-item
        label="邮箱"
        name="email"
        :rules="[
          { required: true, message: '请输入邮箱!' },
          { type: 'email', message: '请输入有效的邮箱地址!' }
        ]"
      >
        <a-input v-model:value="formState.email" />
      </a-form-item>

      <a-form-item
        label="密码"
        name="password"
        :rules="[
          { required: true, message: '请输入密码!' },
          { min: 6, message: '密码至少6个字符!' }
        ]"
      >
        <a-input-password v-model:value="formState.password" />
      </a-form-item>

      <a-form-item
        label="确认密码"
        name="confirmPassword"
        :rules="[
          { required: true, message: '请确认密码!' },
          { validator: validatePassword }
        ]"
      >
        <a-input-password v-model:value="formState.confirmPassword" />
      </a-form-item>

      <a-form-item>
        <a-button 
          type="primary" 
          html-type="submit" 
          :loading="userStore.isLoading"
          style="width: 100%"
        >
          注册
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import { message } from 'ant-design-vue'
import { useUserStore } from '@/stores/user'

interface FormState {
  username: string
  email: string
  password: string
  confirmPassword: string
}

const userStore = useUserStore()
const emit = defineEmits<{
  success: []
}>()

const formState = reactive<FormState>({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePassword = async (_rule: any, value: string) => {
  if (value !== formState.password) {
    throw new Error('两次输入的密码不一致!')
  }
}

const onFinish = async (values: FormState) => {
  const { confirmPassword, ...userData } = values
  const result = await userStore.register(userData)
  
  if (result.success) {
    message.success(result.message)
    emit('success')
    // 重置表单
    Object.assign(formState, {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
  } else {
    message.error(result.message)
  }
}

const onFinishFailed = (errorInfo: any) => {
  console.log('注册失败:', errorInfo)
}
</script>

<style scoped>
.user-register {
  padding: 20px 0;
}
</style>