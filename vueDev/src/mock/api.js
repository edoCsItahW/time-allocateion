/*
 Copyright (c) 2024. All rights reserved.
 This source code is licensed under the CC BY-NC-ND
 (Creative Commons Attribution-NonCommercial-NoDerivatives) License, By Xiao Songtao.
 This software is protected by copyright law. Reproduction, distribution, or use for commercial
 purposes is prohibited without the author's permission. If you have any questions or require
 permission, please contact the author: 2207150234@st.sziit.edu.cn
 */
export default [
  {
    url: '/mock/api/test', //请求地址
    method: 'get', //请求方式
    response: () => {
      return {
        code: 200,
        msg: 'ok',
        data: ''
      }
    },
  },
]
