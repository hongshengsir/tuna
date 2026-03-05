<template>
  <div class="user-edit">
    <a-form
      :model="formState"
      name="editUser"
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
        label="新密码"
        name="password"
        :help="passwordHelp"
      >
        <a-input-password 
          v-model:value="formState.password" 
          placeholder="留空则不修改密码"
        />
      </a-form-item>

      <a-form-item
        label="确认密码"
        name="confirmPassword"
        :rules="[{ validator: validatePassword }]"
      >
        <a-input-password 
          v-model:value="formState.confirmPassword" 
          placeholder="留空则不修改密码"
        />
      </a-form-item>

      <a-form-item>
        <a-space style="width: 100%; justify-content: flex-end">
          <a-button @click="handleCancel">
            取消
          </a-button>
          <a-button 
            type="primary" 
            html-type="submit" 
            :loading="userStore.isLoading"
          >
            保存
          </a-button>
        </a-space>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { message } from 'ant-design-vue'
import { useUserStore, type User } from '@/stores/user'

interface FormState {
  username: string
  email: string
  password: string
  confirmPassword: string
}

interface Props {
  user: User
}

const props = defineProps<Props>()
const emit = defineEmits<{
  success: []
  cancel: []
}>()

const userStore = useUserStore()

const formState = reactive<FormState>({
  username: props.user.username,
  email: props.user.email,
  password: '',
  confirmPassword: ''
})

const passwordHelp = computed(() => {
  if (formState.password && formState.password.length < 6) {
    return '密码至少需要6个字符'
  }
  return '留空则不修改密码'
})

const validatePassword = async (_rule: any, value: string) => {
  if (formState.password && value !== formState.password) {
    throw new Error('两次输入的密码不一致!')
  }
}

const onFinish = async (values: FormState) => {
  const updateData: any = {}
  
  // 只更新有变化的字段
  if (values.username !== props.user.username) {
    updateData.username = values.username
  }
  
  if (values.email !== props.user.email) {
    updateData.email = values.email
  }
  
  if (values.password) {
    updateData.password = values.password
  }
  
  // 如果没有变化，直接返回
  if (Object.keys(updateData).length === 0) {
    message.info('没有检测到任何修改')
    emit('success')
    return
  }
  
  const result = await userStore.updateUser(props.user.id, updateData)
  
  if (result.success) {
    message.success(result.message)
    emit('success')
  } else {
    message.error(result.message || '更新失败')
  }
}

const onFinishFailed = (errorInfo: any) => {
  console.log('表单验证失败:', errorInfo)
}

const handleCancel = () => {
  emit('cancel')
}
</script>

<style scoped>
.user-edit {
  padding: 20px 0;
}
</style>