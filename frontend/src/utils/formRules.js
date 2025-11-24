// 表单验证规则
// 通用验证规则函数
const createRequiredRule = (message = '此项为必填项') => ({
  required: true,
  message,
  trigger: 'blur'
})

// 通用验证规则
const commonRules = {
  // 必填验证
  required: createRequiredRule,

  // 邮箱验证
  email: {
    type: 'email',
    message: '请输入正确的邮箱格式',
    trigger: 'blur'
  },

  // 手机号验证
  phone: {
    pattern: /^1[3-9]\d{9}$/,
    message: '请输入正确的手机号码',
    trigger: 'blur'
  },

  // 密码验证（6-20位，包含字母和数字）
  password: {
    pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{6,20}$/,
    message: '密码必须包含字母和数字，长度6-20位',
    trigger: 'blur'
  },

  // 身份证号验证
  idCard: {
    pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/,
    message: '请输入正确的身份证号码',
    trigger: 'blur'
  },

  // 护照号验证
  passport: {
    pattern: /^[a-zA-Z0-9]{5,17}$/,
    message: '请输入正确的护照号码',
    trigger: 'blur'
  },

  // 港澳通行证验证
  hkMacaoPass: {
    pattern: /^[HMhm]{1}([0-9]{10}|[0-9]{8})$/,
    message: '请输入正确的港澳通行证号码',
    trigger: 'blur'
  },

  // 台湾通行证验证
  taiwanPass: {
    pattern: /^[Tt]{1}[0-9]{8}$/,
    message: '请输入正确的台湾通行证号码',
    trigger: 'blur'
  },

  // 用户名验证（6-30位字母或数字，与API schema一致）
  username: {
    pattern: /^[a-zA-Z0-9]{6,30}$/,
    message: '用户名只能包含字母和数字，长度6-30位',
    trigger: 'blur'
  },

  // 真实姓名验证（2-50位，与API schema一致）
  realName: {
    pattern: /^[\u4e00-\u9fa5a-zA-Z\s]{2,50}$/,
    message: '请输入正确的姓名（2-50位）',
    trigger: 'blur'
  }
}

// 登录表单验证规则
const loginRules = {
  username: [
    createRequiredRule('请输入用户名或手机号'),
    {
      min: 4,
      max: 20,
      message: '用户名长度应为4-20位',
      trigger: 'blur'
    }
  ],
  password: [
    createRequiredRule('请输入密码'),
    {
      min: 6,
      max: 20,
      message: '密码长度应为6-20位',
      trigger: 'blur'
    }
  ],
  captcha: [
    createRequiredRule('请输入验证码'),
    {
      len: 4,
      message: '验证码长度为4位',
      trigger: 'blur'
    }
  ]
}

// 注册表单验证规则
const registerRules = {
  userType: [createRequiredRule('请选择用户类型')],
  loginName: [createRequiredRule('请输入登录名'), commonRules.username],
  email: [createRequiredRule('请输入邮箱'), commonRules.email],
  realName: [createRequiredRule('请输入真实姓名'), commonRules.realName],
  phone: [createRequiredRule('请输入手机号'), commonRules.phone],
  password: [createRequiredRule('请输入密码'), commonRules.password],
  confirmPassword: [
    createRequiredRule('请确认密码'),
    {
      validator: (rule, value, callback, source) => {
        if (value && value !== source.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  agreement: [
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请阅读并同意用户协议'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

// 车票搜索表单验证规则
const ticketSearchRules = {
  fromStation: [createRequiredRule('请选择出发站')],
  toStation: [createRequiredRule('请选择到达站')],
  departureDate: [createRequiredRule('请选择出发日期')],
  returnDate: [
    {
      validator: (rule, value, callback, source) => {
        if (source.tripType === 'round-trip' && !value) {
          callback(new Error('往返票请选择返程日期'))
        } else if (
          value &&
          source.departureDate &&
          new Date(value) <= new Date(source.departureDate)
        ) {
          callback(new Error('返程日期应晚于出发日期'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

// 乘客信息验证规则
const passengerRules = {
  name: [createRequiredRule('请输入乘客姓名'), commonRules.realName],
  id_type: [createRequiredRule('请选择证件类型')],
  id_number: [
    createRequiredRule('请输入证件号码'),
    {
      validator: (rule, value, callback, source) => {
        if (!value) {
          callback()
          return
        }

        const idType = source.id_type
        let pattern
        let message

        switch (idType) {
          case 'ID_CARD':
            pattern = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/
            message = '请输入正确的身份证号码'
            break
          case 'PASSPORT':
            pattern = /^[a-zA-Z0-9]{5,17}$/
            message = '请输入正确的护照号码'
            break
          case 'HK_MACAO_PASS':
            pattern = /^[HMhm]{1}([0-9]{10}|[0-9]{8})$/
            message = '请输入正确的港澳通行证号码'
            break
          case 'TAIWAN_PASS':
            pattern = /^[Tt]{1}[0-9]{8}$/
            message = '请输入正确的台湾通行证号码'
            break
          default:
            callback()
            return
        }

        if (!pattern.test(value)) {
          callback(new Error(message))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ],
  phone: [createRequiredRule('请输入手机号'), commonRules.phone],
  passenger_type: [createRequiredRule('请选择乘客类型')]
}

// 订单相关验证规则
const orderRules = {
  contactName: [createRequiredRule('请输入联系人姓名'), commonRules.realName],
  contactPhone: [createRequiredRule('请输入联系人手机号'), commonRules.phone],
  contactEmail: [commonRules.email]
}

// 支付相关验证规则
const paymentRules = {
  paymentMethod: [createRequiredRule('请选择支付方式')],
  paymentPassword: [
    createRequiredRule('请输入支付密码'),
    {
      min: 6,
      max: 6,
      message: '支付密码为6位数字',
      trigger: 'blur'
    },
    {
      pattern: /^\d{6}$/,
      message: '支付密码只能包含数字',
      trigger: 'blur'
    }
  ]
}

// 导出所有规则
export const formRules = {
  common: commonRules,
  login: loginRules,
  register: registerRules,
  ticketSearch: ticketSearchRules,
  passenger: passengerRules,
  order: orderRules,
  payment: paymentRules
}
