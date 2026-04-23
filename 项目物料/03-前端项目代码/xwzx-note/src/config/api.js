/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: 'http://127.0.0.1:8000',
}

// AI 聊天后端接口配置
export const aiChatConfig = {
  // 后端 AI 聊天接口地址
  chatEndpoint: `${apiConfig.baseURL}/api/ai/chat`,
  // 后端聊天记录接口地址
  historyEndpoint: `${apiConfig.baseURL}/api/ai/history`
}
