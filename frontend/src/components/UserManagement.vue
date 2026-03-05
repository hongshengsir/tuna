<template>
  <div class="user-management">
    <!-- 用户信息头部 -->
    <a-card title="用户管理" :bordered="false" style="margin-bottom: 24px">
      <template #extra>
        <a-space>
          <span v-if="userStore.currentUser">
            当前用户: {{ userStore.currentUser.username }}
          </span>
          <a-button type="primary" @click="showCreateUser = true">
            <template #icon><UserAddOutlined /></template>
            创建用户
          </a-button>
          <a-button @click="handleLogout" danger>
            <template #icon><LogoutOutlined /></template>
            退出登录
          </a-button>
        </a-space>
      </template>

      <a-space direction="vertical" style="width: 100%">
        <a-alert
          message="用户管理功能"
          description="您可以查看、编辑和删除系统用户。只有管理员可以管理所有用户。"
          type="info"
          show-icon
        />
      </a-space>
    </a-card>

    <!-- 用户列表 -->
    <a-card title="用户列表" :bordered="false">
      <template #extra>
        <a-button @click="refreshUsers" :loading="userStore.isLoading">
          <template #icon><ReloadOutlined /></template>
          刷新
        </a-button>
      </template>

      <a-table
        :data-source="userStore.users"
        :columns="columns"
        :loading="userStore.isLoading"
        :pagination="{ pageSize: 10, showSizeChanger: true }"
        row-key="id"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'actions'">
            <a-space>
              <a-button type="link" size="small" @click="handleEdit(record)">
                编辑
              </a-button>
              <a-popconfirm
                title="确定要删除这个用户吗？"
                ok-text="确定"
                cancel-text="取消"
                @confirm="handleDelete(record.id)"
              >
                <a-button type="link" size="small" danger>
                  删除
                </a-button>
              </a-popconfirm>
            </a-space>
          </template>
          
          <template v-else-if="column.key === 'created_at'">
            {{ formatDate(record.created_at) }}
          </template>
          
          <template v-else-if="column.key === 'updated_at'">
            {{ formatDate(record.updated_at) }}
          </template>
        </template>

        <template #emptyText>
          <a-empty description="暂无用户数据">
            <template #image>
              <UserOutlined style="font-size: 48px; color: #d9d9d9" />
            </template>
          </a-empty>
        </template>
      </a-table>
    </a-card>

    <!-- 创建用户模态框 -->
    <a-modal
      v-model:open="showCreateUser"
      title="创建用户"
      :footer="null"
      @cancel="showCreateUser = false"
    >
      <UserRegister @success="handleCreateSuccess" />
    </a-modal>

    <!-- 编辑用户模态框 -->
    <a-modal
      v-model:open="showEditUser"
      :title="`编辑用户 - ${editingUser?.username}`"
      :footer="null"
      @cancel="handleEditCancel"
    >
      <UserEdit 
        v-if="editingUser" 
        :user="editingUser" 
        @success="handleEditSuccess" 
        @cancel="handleEditCancel"
      />
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { 
  UserAddOutlined, 
  LogoutOutlined, 
  ReloadOutlined, 
  UserOutlined 
} from '@ant-design/icons-vue'
import { useUserStore, type User } from '@/stores/user'
import UserRegister from './UserRegister.vue'
import UserEdit from './UserEdit.vue'

const userStore = useUserStore()
const showCreateUser = ref(false)
const showEditUser = ref(false)
const editingUser = ref<User | null>(null)

const columns = [
  {
    title: 'ID',
    dataIndex: 'id',
    key: 'id',
    width: 80
  },
  {
    title: '用户名',
    dataIndex: 'username',
    key: 'username'
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    key: 'email'
  },
  {
    title: '创建时间',
    dataIndex: 'created_at',
    key: 'created_at'
  },
  {
    title: '更新时间',
    dataIndex: 'updated_at',
    key: 'updated_at'
  },
  {
    title: '操作',
    key: 'actions',
    width: 150
  }
]

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('zh-CN')
}

const refreshUsers = async () => {
  const result = await userStore.fetchUsers()
  if (result.success) {
    message.success('用户列表刷新成功')
  } else {
    message.error(result.message || '刷新失败')
  }
}

const handleEdit = (user: User) => {
  editingUser.value = { ...user }
  showEditUser.value = true
}

const handleDelete = async (userId: number) => {
  const result = await userStore.deleteUser(userId)
  if (result.success) {
    message.success(result.message)
  } else {
    message.error(result.message || '删除失败')
  }
}

const handleCreateSuccess = () => {
  showCreateUser.value = false
  refreshUsers()
}

const handleEditSuccess = () => {
  showEditUser.value = false
  editingUser.value = null
  refreshUsers()
}

const handleEditCancel = () => {
  showEditUser.value = false
  editingUser.value = null
}

const handleLogout = () => {
  userStore.logout()
  message.success('已退出登录')
}

onMounted(async () => {
  // 检查登录状态
  const isAuthenticated = await userStore.checkAuth()
  if (!isAuthenticated) {
    message.warning('请先登录')
    return
  }
  
  // 加载用户列表
  await refreshUsers()
})
</script>

<style scoped>
.user-management {
  padding: 0;
}
</style>