import { http } from '@/utils/request'

// 短信验证码相关 API
export const smsApi = {
  // 提交短信验证码
  submitCode(data) {
    return http.post('/api/sms-code', data)
  }
}
