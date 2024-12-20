const env = import.meta.env.MODE || 'production'
const EnvConfig = {
    development: {
        baseApi: import.meta.env.VITE_BASE_API_dev,
        mockApi: import.meta.env.VITE_MOCK_API_dev,
    },
    test: {
        baseApi: import.meta.env.VITE_BASE_API_dev,
        mockApi: import.meta.env.VITE_MOCK_API_dev,
    },
    production: {
        baseApi: import.meta.env.VITE_BASE_API_prod,
        mockApi: import.meta.env.VITE_MOCK_API_prod,
    }
}

export default {
    env,
    ...EnvConfig[env],
    //mock
    mock: false,  // 远程的关了，可以在本地mock.js的方式使用本地的
    // mock: true,  // 远程的开了，然后关掉main.js:   import "@/api/mock.js"
}