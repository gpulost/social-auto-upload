<template>
  <div class="sms-verification">
    <div class="page-header">
      <h1>短信验证码</h1>
      <p class="page-desc">
        发布任务（如抖音）需要短信验证时，在此页面输入验证码，服务将自动填充并继续发布
      </p>
    </div>

    <el-card class="sms-card">
      <template #header>
        <div class="card-header">
          <el-icon><ChatDotRound /></el-icon>
          <span>输入验证码</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="sms-form"
      >
        <el-form-item label="平台" prop="platform">
          <el-select v-model="form.platform" placeholder="选择平台" style="width: 100%">
            <el-option label="抖音" value="douyin" />
            <el-option label="快手" value="kuaishou" />
            <el-option label="视频号" value="tencent" />
          </el-select>
        </el-form-item>

        <el-form-item label="验证码" prop="code">
          <el-input
            v-model="form.code"
            placeholder="请输入手机收到的短信验证码"
            maxlength="8"
            show-word-limit
            clearable
            @keyup.enter="handleSubmit"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            提交
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-alert
        type="info"
        :closable="false"
        show-icon
        class="sms-tip"
      >
        <template #title>
          <span>使用说明</span>
        </template>
        <ul>
          <li>当发布视频时弹出「接收短信验证码」弹窗，请在此页面输入收到的验证码并提交</li>
          <li>提交后，发布任务将自动获取验证码并填充，无需手动操作浏览器</li>
          <li>验证码一次性有效，使用后即清除</li>
        </ul>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { ChatDotRound } from '@element-plus/icons-vue'
import { smsApi } from '@/api/sms'

const formRef = ref(null)
const submitting = ref(false)

const form = reactive({
  platform: 'douyin',
  code: ''
})

const rules = {
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { min: 4, max: 8, message: '验证码长度 4-8 位', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    submitting.value = true
    try {
      await smsApi.submitCode({
        platform: form.platform,
        code: form.code
      })
      ElMessage.success('验证码已提交，发布任务将自动填充')
      form.code = ''
    } catch (e) {
      ElMessage.error(e?.response?.data?.msg || '提交失败')
    } finally {
      submitting.value = false
    }
  })
}

const handleReset = () => {
  form.code = ''
  formRef.value?.resetFields()
}
</script>

<style lang="scss" scoped>
.sms-verification {
  .page-header {
    margin-bottom: 20px;

    h1 {
      margin: 0 0 8px 0;
      font-size: 24px;
      font-weight: 600;
    }

    .page-desc {
      margin: 0;
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }
  }

  .sms-card {
    max-width: 520px;

    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;

      .el-icon {
        font-size: 18px;
      }
    }

    .sms-form {
      margin-bottom: 20px;
    }

    .sms-tip {
      ul {
        margin: 8px 0 0 0;
        padding-left: 18px;

        li {
          margin-bottom: 4px;
          line-height: 1.5;
        }
      }
    }
  }
}
</style>
