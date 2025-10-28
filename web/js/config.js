/**
 * 前端配置文件
 * 可以根据部署环境修改此文件中的配置
 */

// 自动检测 API 基础 URL
// 如果需要指定特定的 API 地址，可以设置 window.API_BASE_URL
// 否则默认使用相对路径 '/api/v1'，会自动使用当前域名

// 开发环境示例：
// window.API_BASE_URL = 'http://localhost:8000/api/v1';

// 生产环境示例（使用相对路径，自动适配当前域名）：
// window.API_BASE_URL = '/api/v1';

// 如果后端部署在不同的域名或端口，可以指定完整 URL：
// window.API_BASE_URL = 'https://api.yourdomain.com/api/v1';

// 默认使用相对路径（推荐）
window.API_BASE_URL = window.API_BASE_URL || '/api/v1';

// 其他前端配置
window.APP_CONFIG = {
    // API 配置
    apiBaseURL: window.API_BASE_URL,
    
    // 请求超时时间（毫秒）
    requestTimeout: 30000,
    
    // 分页配置
    defaultPageSize: 20,
    maxPageSize: 100,
    
    // 调试模式
    debug: false
};
